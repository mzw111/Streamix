-- ============================================================================
-- TRIGGER DEMONSTRATION SCRIPT FOR TEACHER
-- ============================================================================
-- Purpose: Demonstrate the trg_UpdateMovieRating trigger that automatically
--          updates the Average_Rating in the movie table when ratings are added
-- ============================================================================

-- STEP 1: Check current state of a movie BEFORE adding ratings
SELECT Movie_Id, Title, Average_Rating, 
       'BEFORE adding ratings' AS Status
FROM movie 
WHERE Movie_Id = 26;

-- STEP 2: Insert some rating data to trigger the automatic update
-- (These ratings will trigger trg_UpdateMovieRating automatically)
INSERT INTO rating_review (Profile_Id, Content_Type, Content_Id, Rating, Review_Text, Review_Date)
VALUES 
    (15, 'Movie', 26, 5.0, 'Masterpiece! Best superhero movie ever!', NOW()),
    (14, 'Movie', 26, 4.5, 'Excellent performance by Heath Ledger', DATE_SUB(NOW(), INTERVAL 1 DAY)),
    (13, 'Movie', 26, 4.0, 'Great action sequences', DATE_SUB(NOW(), INTERVAL 2 DAY));

-- STEP 3: Check the movie AFTER ratings were added
-- The Average_Rating should now be automatically calculated by the trigger!
SELECT Movie_Id, Title, Average_Rating, 
       'AFTER adding ratings - Updated by TRIGGER!' AS Status
FROM movie 
WHERE Movie_Id = 26;

-- STEP 4: Show all ratings for this movie to verify the calculation
SELECT r.Rating_Id, r.Profile_Id, r.Rating, r.Review_Text, r.Review_Date
FROM rating_review r
WHERE r.Content_Type = 'Movie' AND r.Content_Id = 26
ORDER BY r.Review_Date DESC;

-- Expected Result: Average_Rating should be (5.0 + 4.5 + 4.0) / 3 = 4.5
-- This proves the trigger trg_UpdateMovieRating is working automatically!

-- ============================================================================
-- BONUS: Add some viewing history for profile to show complete functionality
-- ============================================================================
INSERT INTO viewing_history (Profile_Id, Content_Type, Content_Id, Watch_Duration, Watch_Date)
VALUES 
    (15, 'Movie', 26, 152, DATE_SUB(NOW(), INTERVAL 5 DAY)),
    (15, 'Movie', 27, 148, DATE_SUB(NOW(), INTERVAL 3 DAY)),
    (15, 'Movie', 28, 142, DATE_SUB(NOW(), INTERVAL 1 DAY)),
    (15, 'TV_Show', 11, 60, NOW());

-- ============================================================================
-- HOW TO DEMONSTRATE TO TEACHER:
-- ============================================================================
-- 1. Run "STEP 1" query - Show current Average_Rating (probably NULL or old value)
-- 2. Run "STEP 2" INSERT - Add 3 ratings for Movie ID 26
-- 3. Run "STEP 3" query - Show Average_Rating is NOW 4.5 (automatically calculated!)
-- 4. Run "STEP 4" query - Show the 3 ratings that were inserted
-- 5. Explain: "The trigger trg_UpdateMovieRating automatically calculated 
--              the average (5.0 + 4.5 + 4.0) / 3 = 4.5 without any manual update!"
-- ============================================================================
