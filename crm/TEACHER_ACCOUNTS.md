# Teacher Account Management

## Overview
This document explains how teacher accounts work in the school management system.

## How It Works

### When Creating a New Teacher (Admin)

1. **Go to**: Add Teacher form
2. **Check**: "បង្កើតគណនីអ្នកប្រើ (Create User Account)" checkbox (checked by default)
3. **Optional**: Enter custom username and password
   - If left blank, username will be auto-generated from teacher's name
   - Default password: `teacher123`
4. **Save**: Teacher record is created AND user account is created automatically

### Teacher Login Credentials

**Existing Teachers:**
- Username: `lensophara` | Password: `teacher123`
- Username: `taki` | Password: `teacher123`

**New Teachers:**
- Username: Auto-generated or custom
- Password: `teacher123` (default) or custom

### Relationships

```
User Account (username/password)
    ↓
UserProfile (role: teacher)
    ↓
Teacher Record (teacher info)
    ↓
Classroom (homeroom_teacher)
    ↓
Students (in that classroom)
```

### What Teachers Can See

When a teacher logs in:
1. **Dashboard**: Shows their classrooms and students
2. **Student List**: Only students in their classrooms
3. **Attendance**: Only for their students
4. **Scores**: Only for their students

### Linking Existing Teachers

If you have existing teachers without user accounts, run:

```bash
python link_existing_teachers.py
```

This will:
- Create user accounts for all teachers
- Link UserProfile to Teacher records
- Set default password: `teacher123`

### Testing Teacher Access

Run the test script to verify teacher can see students:

```bash
python test_teacher_login.py
```

## Important Notes

1. **Classroom Assignment**: Teachers must be assigned as homeroom teacher to a classroom to see students
2. **Student Assignment**: Students must be assigned to a classroom to appear in teacher's view
3. **Password Security**: Teachers should change their password after first login
4. **Admin Rights**: Only admin can create/edit teacher records

## Database Relationships

- `User` → `UserProfile` (one-to-one)
- `UserProfile` → `Teacher` (one-to-one via `teacher` field)
- `Teacher` → `Classroom` (one-to-many via `homeroom_teacher`)
- `Classroom` → `Student` (one-to-many via `classroom`)

## Troubleshooting

### Teacher Can't See Students

**Check:**
1. Teacher has user account? → Run `link_existing_teachers.py`
2. Teacher assigned to classroom? → Edit classroom and set homeroom teacher
3. Students assigned to classroom? → Edit student and set classroom
4. Student is active? → Check `is_active` field

### Teacher Can't Login

**Check:**
1. User account exists? → Run `check_relationships.py`
2. UserProfile linked to Teacher? → Run `test_teacher_login.py`
3. Password correct? → Default is `teacher123`
4. UserProfile role is 'teacher'? → Check in admin panel

## Scripts

- `check_relationships.py` - View all relationships
- `link_existing_teachers.py` - Create accounts for existing teachers
- `test_teacher_login.py` - Test teacher access to students
