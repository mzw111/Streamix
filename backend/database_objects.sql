-- ============================================
-- STREAMIX DATABASE OBJECTS
-- Stored Procedures, Triggers, and Functions
-- ============================================

USE streamingdb;

-- ============================================
-- 1. STORED PROCEDURE: Add to Watchlist
-- ============================================
DROP PROCEDURE IF EXISTS sp_AddToWatchlist;

DELIMITER //
CREATE PROCEDURE sp_AddToWatchlist(
    IN p_profile_id INT,
    IN p_content_type ENUM('Movie', 'TV_Show'),
    IN p_content_id INT
)
BEGIN
    DECLARE v_exists INT;
    
    -- Check if item already exists in watchlist
    SELECT COUNT(*) INTO v_exists
    FROM watchlist
    WHERE Profile_Id = p_profile_id 
    AND Content_Type = p_content_type 
    AND Content_Id = p_content_id;
    
    -- Only insert if not already in watchlist
    IF v_exists = 0 THEN
        INSERT INTO watchlist (Profile_Id, Content_Type, Content_Id, Date_Added)
        VALUES (p_profile_id, p_content_type, p_content_id, CURDATE());
    END IF;
END //
DELIMITER ;

-- ============================================
-- 2. STORED PROCEDURE: Remove from Watchlist
-- ============================================
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

-- ============================================
-- 3. STORED PROCEDURE: Get User Watch History
-- ============================================
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

-- ============================================
-- 4. FUNCTION: Get User's Subscription Status
-- ============================================
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

-- ============================================
-- 5. FUNCTION: Calculate Total Watch Time
-- ============================================
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

-- ============================================
-- 6. TRIGGER: Update Average Rating on Movie
-- ============================================
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

-- ============================================
-- 7. TRIGGER: Update Average Rating on TV Show
-- ============================================
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

-- ============================================
-- 8. TRIGGER: Log Viewing History
-- ============================================
DROP TRIGGER IF EXISTS trg_LogViewingHistory;

DELIMITER //
CREATE TRIGGER trg_LogViewingHistory
AFTER INSERT ON viewing_history
FOR EACH ROW
BEGIN
    -- This trigger can be used to perform additional actions
    -- For example, updating user statistics or recommendations
    -- Currently acts as a logging point for future enhancements
    SELECT CONCAT('View logged for Profile ', NEW.Profile_Id) AS log_message;
END //
DELIMITER ;

-- ============================================
-- 9. STORED PROCEDURE: Get Content Recommendations
-- ============================================
DROP PROCEDURE IF EXISTS sp_GetRecommendations;

DELIMITER //
CREATE PROCEDURE sp_GetRecommendations(
    IN p_profile_id INT,
    IN p_limit INT
)
BEGIN
    -- Get recommendations based on viewing history and ratings
    SELECT DISTINCT 
        'Movie' AS content_type,
        m.Movie_Id AS content_id,
        m.Title,
        m.average_rating,
        m.Release_Date
    FROM movie m
    INNER JOIN movie_genre mg ON m.Movie_Id = mg.Movie_Id
    WHERE mg.Genre_Id IN (
        -- Get genres from user's viewing history
        SELECT DISTINCT mg2.Genre_Id
        FROM viewing_history vh
        INNER JOIN movie_genre mg2 ON vh.Content_Id = mg2.Movie_Id
        WHERE vh.Profile_Id = p_profile_id 
        AND vh.Content_Type = 'Movie'
    )
    AND m.Movie_Id NOT IN (
        -- Exclude already watched movies
        SELECT Content_Id FROM viewing_history 
        WHERE Profile_Id = p_profile_id AND Content_Type = 'Movie'
    )
    ORDER BY m.average_rating DESC
    LIMIT p_limit;
END //
DELIMITER ;

-- ============================================
-- 10. STORED PROCEDURE: Process Payment
-- ============================================
DROP PROCEDURE IF EXISTS sp_ProcessPayment;

DELIMITER //
CREATE PROCEDURE sp_ProcessPayment(
    IN p_user_id INT,
    IN p_plan_id INT,
    IN p_amount DECIMAL(10,2),
    IN p_payment_method VARCHAR(50)
)
BEGIN
    DECLARE v_payment_id INT;
    DECLARE v_end_date DATE;
    
    -- Calculate subscription end date (30 days from now)
    SET v_end_date = DATE_ADD(CURDATE(), INTERVAL 30 DAY);
    
    -- Insert payment record
    INSERT INTO payment (User_Id, Amount, Payment_Date, Payment_Method, Status)
    VALUES (p_user_id, p_amount, NOW(), p_payment_method, 'Completed');
    
    SET v_payment_id = LAST_INSERT_ID();
    
    -- Update or create subscription
    INSERT INTO subscription (User_Id, Plan_Id, Start_Date, End_Date, Status, Payment_Id)
    VALUES (p_user_id, p_plan_id, CURDATE(), v_end_date, 'Active', v_payment_id)
    ON DUPLICATE KEY UPDATE
        Plan_Id = p_plan_id,
        End_Date = v_end_date,
        Status = 'Active',
        Payment_Id = v_payment_id;
        
    SELECT 'Payment processed successfully' AS message, v_payment_id AS payment_id;
END //
DELIMITER ;

-- ============================================
-- Test the database objects
-- ============================================

-- Test subscription function
SELECT fn_GetSubscriptionStatus(1) AS subscription_status;

-- Show all created procedures
SHOW PROCEDURE STATUS WHERE Db = 'streamingdb';

-- Show all created functions
SHOW FUNCTION STATUS WHERE Db = 'streamingdb';

-- Show all created triggers
SHOW TRIGGERS FROM streamingdb;

SELECT 'Database objects created successfully!' AS status;
