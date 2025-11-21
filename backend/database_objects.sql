
USE streamingdb;
-- procedures
-- added to watchlist
DROP PROCEDURE IF EXISTS sp_AddToWatchlist;

DELIMITER //
CREATE PROCEDURE sp_AddToWatchlist(
    IN p_profile_id INT,
    IN p_content_type ENUM('Movie', 'TV_Show'),
    IN p_content_id INT
)
BEGIN
    DECLARE v_exists INT;
    
    
    SELECT COUNT(*) INTO v_exists
    FROM watchlist
    WHERE Profile_Id = p_profile_id 
    AND Content_Type = p_content_type 
    AND Content_Id = p_content_id;
   
    IF v_exists = 0 THEN
        INSERT INTO watchlist (Profile_Id, Content_Type, Content_Id, Date_Added)
        VALUES (p_profile_id, p_content_type, p_content_id, CURDATE());
    END IF;
END //
DELIMITER ;

--removed from watchlist
DROP PROCEDURE IF EXISTS sp_RemoveFromWatchlist;

DELIMITER //
CREATE PROCEDURE sp_RemoveFromWatchlist(
    IN p_profile_id INT,
    IN p_content_type ENUM('Movie', 'TV_Show'),
    IN p_content_id INT
)
BEGIN
    DELETE FROM watchlist
    WHERE Profile_Id = p_profile_id 
    AND Content_Type = p_content_type 
    AND Content_Id = p_content_id;
END //
DELIMITER ;


--user history
DROP PROCEDURE IF EXISTS sp_GetWatchHistory;

DELIMITER //
CREATE PROCEDURE sp_GetWatchHistory(
    IN p_profile_id INT
)
BEGIN
    SELECT vh.*, 
           CASE 
               WHEN vh.Content_Type = 'Movie' THEN m.Title
               WHEN vh.Content_Type = 'TV_Show' THEN t.Title
           END AS Title,
           CASE 
               WHEN vh.Content_Type = 'Movie' THEN m.Duration
               ELSE NULL
           END AS Duration
    FROM viewing_history vh
    LEFT JOIN movie m ON vh.Content_Type = 'Movie' AND vh.Content_Id = m.Movie_Id
    LEFT JOIN tv_show t ON vh.Content_Type = 'TV_Show' AND vh.Content_Id = t.Show_Id
    WHERE vh.Profile_Id = p_profile_id
    ORDER BY vh.Watch_Date DESC;
END //
DELIMITER ;

-- functions
--- subscription status
DROP FUNCTION IF EXISTS fn_GetSubscriptionStatus;

DELIMITER //
CREATE FUNCTION fn_GetSubscriptionStatus(p_user_id INT)
RETURNS VARCHAR(20)
DETERMINISTIC
READS SQL DATA
BEGIN
    DECLARE v_status VARCHAR(20);
    
    SELECT Status INTO v_status
    FROM subscription
    WHERE User_Id = p_user_id
    AND End_Date >= CURDATE()
    ORDER BY End_Date DESC
    LIMIT 1;
    
    IF v_status IS NULL THEN
        SET v_status = 'Inactive';
    END IF;
    
    RETURN v_status;
END //
DELIMITER ;

-- watch time
DROP FUNCTION IF EXISTS fn_GetTotalWatchTime;

DELIMITER //
CREATE FUNCTION fn_GetTotalWatchTime(p_profile_id INT)
RETURNS INT
DETERMINISTIC
READS SQL DATA
BEGIN
    DECLARE v_total_time INT DEFAULT 0;
    
    
    SELECT COALESCE(SUM(
        CASE 
            WHEN vh.Content_Type = 'Movie' THEN m.Duration
            ELSE 0
        END
    ), 0) INTO v_total_time
    FROM viewing_history vh
    LEFT JOIN movie m ON vh.Content_Type = 'Movie' AND vh.Content_Id = m.Movie_Id
    WHERE vh.Profile_Id = p_profile_id;
    
    RETURN v_total_time;
END //
DELIMITER ;

-- triggers
-- update movie rating avg
DROP TRIGGER IF EXISTS trg_UpdateMovieRating;

DELIMITER //
CREATE TRIGGER trg_UpdateMovieRating
AFTER INSERT ON rating
FOR EACH ROW
BEGIN
    IF NEW.Content_Type = 'Movie' THEN
        UPDATE movie
        SET average_rating = (
            SELECT AVG(Rating_Value)
            FROM rating
            WHERE Content_Type = 'Movie' AND Content_Id = NEW.Content_Id
        )
        WHERE Movie_Id = NEW.Content_Id;
    END IF;
END //
DELIMITER ;

-- update tv rating avg
DROP TRIGGER IF EXISTS trg_UpdateTVShowRating;

DELIMITER //
CREATE TRIGGER trg_UpdateTVShowRating
AFTER INSERT ON rating
FOR EACH ROW
BEGIN
    IF NEW.Content_Type = 'TV_Show' THEN
        UPDATE tv_show
        SET average_rating = (
            SELECT AVG(Rating_Value)
            FROM rating
            WHERE Content_Type = 'TV_Show' AND Content_Id = NEW.Content_Id
        )
        WHERE Show_Id = NEW.Content_Id;
    END IF;
END //
DELIMITER ;

--log viewing history
DROP TRIGGER IF EXISTS trg_LogViewingHistory;

DELIMITER //
CREATE TRIGGER trg_LogViewingHistory
AFTER INSERT ON viewing_history
FOR EACH ROW
BEGIN
   
    SELECT CONCAT('View logged for Profile ', NEW.Profile_Id) AS log_message;
END //
DELIMITER ;


--  (max 3 profiles per user)
DROP TRIGGER IF EXISTS trg_CheckProfileLimit;

DELIMITER //
CREATE TRIGGER trg_CheckProfileLimit
BEFORE INSERT ON profile
FOR EACH ROW
BEGIN
    DECLARE existing_profile_count INT;
    
    -- Count existing profiles for this user
    SELECT COUNT(*) 
    INTO existing_profile_count 
    FROM profile 
    WHERE User_Id = NEW.User_Id;
    
    
    IF existing_profile_count >= 3 THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Error: Maximum profile limit (3) reached for this user.';
    END IF;
END //
DELIMITER ;



SELECT fn_GetSubscriptionStatus(1) AS subscription_status;

-- Show all created procedures
SHOW PROCEDURE STATUS WHERE Db = 'streamingdb';

-- Show all created functions
SHOW FUNCTION STATUS WHERE Db = 'streamingdb';

-- Show all created triggers
SHOW TRIGGERS FROM streamingdb;

SELECT 'Database objects created successfully!' AS status;
