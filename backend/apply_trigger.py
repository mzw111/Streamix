from db import execute_query

# Drop old trigger if exists
execute_query('DROP TRIGGER IF EXISTS trg_CheckProfileLimit')
print('✅ Old trigger dropped (if existed)')

# Create new trigger
trigger_sql = """
CREATE TRIGGER trg_CheckProfileLimit
BEFORE INSERT ON profile
FOR EACH ROW
BEGIN
    DECLARE existing_profile_count INT;
    
    SELECT COUNT(*) 
    INTO existing_profile_count 
    FROM profile 
    WHERE User_Id = NEW.User_Id;
    
    IF existing_profile_count >= 3 THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Error: Maximum profile limit (3) reached for this user.';
    END IF;
END
"""

execute_query(trigger_sql)
print('✅ Trigger trg_CheckProfileLimit created successfully!')
print('   - Limits each user to maximum 3 profiles')
print('   - Will show error if user tries to create 4th profile')
