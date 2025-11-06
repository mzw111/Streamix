-- ============================================
-- DROP TRIGGERS SCRIPT
-- ============================================
-- This script removes the rating update triggers

-- Drop Movie Rating Trigger
DROP TRIGGER IF EXISTS trg_UpdateMovieRating;

-- Drop TV Show Rating Trigger
DROP TRIGGER IF EXISTS trg_UpdateTVShowRating;

-- Verify triggers are dropped
SHOW TRIGGERS;
