-- ============================================
-- NEW TRIGGER: Check Profile Limit
-- ============================================
-- Prevents users from creating more than 3 profiles

DELIMITER $$

DROP TRIGGER IF EXISTS trg_CheckProfileLimit$$

CREATE TRIGGER trg_CheckProfileLimit
BEFORE INSERT ON profile
FOR EACH ROW
BEGIN
    DECLARE existing_profile_count INT;

    -- Count how many profiles this user (NEW.User_Id) already has
    SELECT COUNT(*) 
    INTO existing_profile_count 
    FROM profile 
    WHERE User_Id = NEW.User_Id;

    -- If the user already has 3 (or more) profiles, block the insert
    IF existing_profile_count >= 3 THEN
        -- '45000' is a generic error state you can use
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Error: Maximum profile limit (3) reached for this user.';
    END IF;

END$$

DELIMITER ;

