# Parent Registration Fix - Allow Multiple Parents Per Child

## Problem
The error: `duplicate key value violates unique constraint "school_userprofile_student_id_key"`

This occurred because the database had a **UNIQUE constraint** on the `student_id` field in the `UserProfile` table, which prevented both mom and dad from creating separate accounts for the same child.

## Root Cause
- `UserProfile.student` was a `OneToOneField` (only 1 profile per student)
- Database enforced this with a unique constraint on `student_id`

## Solution Applied

### 1. Model Changes
Changed `UserProfile.student` from `OneToOneField` to `ForeignKey`:

**Before:**
```python
student = models.OneToOneField('Student', on_delete=models.SET_NULL, 
                               null=True, blank=True, related_name='user_profile')
```

**After:**
```python
student = models.ForeignKey('Student', on_delete=models.SET_NULL, 
                            null=True, blank=True, related_name='parent_profiles')
```

### 2. Form & View Updates
- Removed validation that blocked multiple parents
- Added transaction safety (`transaction.atomic()`)
- Added error handling in view

### 3. Database Migration
Created migration file: `0008_change_userprofile_student_to_foreignkey.py`

## How to Fix Your Database

### Option 1: Run the Python Script (Recommended)
```bash
python fix_parent_database.py
```

This script will:
- ✅ Remove the unique constraint on `student_id`
- ✅ Create a performance index
- ✅ Verify the changes
- ✅ Show you exactly what changed

### Option 2: Run Django Migration (If you have virtual env)
```bash
python manage.py migrate school 0008
```

### Option 3: Manual SQL (Advanced)
If you need to do it manually in your database:

```sql
-- For PostgreSQL
ALTER TABLE school_userprofile DROP CONSTRAINT IF EXISTS school_userprofile_student_id_key;
CREATE INDEX IF NOT EXISTS school_userprofile_student_id_idx ON school_userprofile(student_id);

-- For SQLite (in db.sqlite3)
-- Note: SQLite doesn't support DROP CONSTRAINT directly
-- You'll need to recreate the table without the constraint
```

## After Fixing

Once the database constraint is removed, the parent registration will work correctly:

1. **First parent (Mom)** registers with child's student_id → ✅ Success
2. **Second parent (Dad)** registers with same student_id → ✅ Success (no more error!)

## Related Files Changed

- `school/models.py` - Changed `student` field type
- `school/forms.py` - Removed blocking validation, added transaction
- `school/views.py` - Added error handling
- `school/migrations/0008_change_userprofile_student_to_foreignkey.py` - Migration file

## Testing

After fixing the database, test:

1. Register first parent (mom) with a student_id
2. Register second parent (dad) with the SAME student_id
3. Both should succeed without errors

## Notes

- Each parent gets their own separate User account
- Both parents link to the same Student via `UserProfile.student`
- Student can now have multiple parents via `student.parent_profiles.all()`
- The `relationship` field in the form tracks if it's mom or dad

## Support

If you still see errors after running the fix:
1. Check that the database constraint was actually removed
2. Verify the migration was applied: `python manage.py showmigrations school`
3. Check for any remaining unique constraints: See `fix_parent_database.py` output
