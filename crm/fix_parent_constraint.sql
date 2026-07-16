-- This SQL script removes the unique constraint on student_id in UserProfile
-- to allow multiple parents (mom and dad) to register for the same child

-- Step 1: Drop the unique constraint on student_id
ALTER TABLE school_userprofile DROP CONSTRAINT IF EXISTS school_userprofile_student_id_key;

-- Step 2: Create a regular index (optional, for performance)
CREATE INDEX IF NOT EXISTS school_userprofile_student_id_idx ON school_userprofile(student_id);

-- Verify the change
SELECT 
    constraint_name, 
    constraint_type 
FROM information_schema.table_constraints 
WHERE table_name = 'school_userprofile';
