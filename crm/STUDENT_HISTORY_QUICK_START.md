# Student History System - Quick Start Guide
# ការចាប់ផ្តើមរហ័ស - ប្រព័ន្ធប្រវត្តិសិស្ស

## ✅ What Was Implemented | អ្វីដែលត្រូវបានអនុវត្ត

### 1. **StudentHistory Model** 📚
A new database table that stores one record per student per academic year containing:
- Academic performance (average scores, pass/fail counts)
- Attendance data (present/absent days)
- Classroom and grade information
- Promotion dates and notes

### 2. **Automatic History Creation** 🔄
When you promote students using `/school/students/promote/`, the system:
- ✅ Creates a StudentHistory record for the completed year
- ✅ Saves all scores, attendance, and classroom data
- ✅ Updates student to new grade (status stays ACTIVE)
- ✅ Maintains same student_id across all years

### 3. **Admin Interface** 🖥️
View student history at: `/admin/school/studenthistory/`
- Filter by academic year, grade, status
- Search by student ID or name
- See complete progression for each student

---

## 🚀 How to Use

### Promoting Students

**Step 1**: Go to student promotion page
```
URL: /school/students/promote/
```

**Step 2**: Select filters
- Current classroom
- Academic year
- Passing percentage (default: 50%)

**Step 3**: Review students
The system shows which students can be promoted based on their scores.

**Step 4**: Promote
- Select students to promote
- Choose destination classroom
- Click "Promote Students"

**Result**: 
- ✅ StudentHistory record created automatically
- ✅ Student moved to new classroom
- ✅ Status remains ACTIVE
- ✅ All historical data preserved

### Viewing Student History

**Method 1: Student Detail Page**
```
URL: /school/students/<id>/
Section: "Student History" or "ប្រវត្តិសិស្ស"
```

**Method 2: Django Admin**
```
URL: /admin/school/studenthistory/
Filter by: Student, Academic Year, Grade
```

**Method 3: Python Code**
```python
# Get all history for a student
student = Student.objects.get(student_id='STU-0001')
history = student.history_records.all()

# Get specific year
history_2024 = student.history_records.get(
    academic_year__year='2024-2025'
)

# Loop through history
for record in student.history_records.all():
    print(f"{record.academic_year.year}: {record.grade_name}")
    print(f"Average: {record.average_score}%")
    print(f"Attendance: {record.attendance_percentage()}%")
```

---

## 📊 Data Structure

### Before Promotion
```
Student: STU-0001 "John Doe"
├─ Classroom: Grade 1-A (2024-2025)
├─ Status: ACTIVE
├─ Scores: Math 85, Khmer 90, Science 78
└─ Attendance: 180/185 days present
```

### After Promotion
```
Student: STU-0001 "John Doe"
├─ Current Record:
│   ├─ Classroom: Grade 2-A (2025-2026)
│   └─ Status: ACTIVE (ready for new year)
│
└─ History Records:
    └─ 2024-2025: Grade 1-A
        ├─ Status: PROMOTED
        ├─ Average Score: 84.3
        ├─ Subjects: 8 total, 8 passed, 0 failed
        ├─ Attendance: 180 present, 5 absent (97.3%)
        └─ Note: "ឡើងថ្នាក់ទៅ Grade 2 នៅថ្ងៃទី 03/08/2026"
```

---

## 🎯 Key Features

### ✅ Benefits

1. **Complete History** 
   - Every academic year preserved forever
   - Never lose student data when promoting

2. **Single Student Record**
   - One student_id across all years
   - Easy to track individual progression

3. **Automatic Processing**
   - No manual data entry needed
   - Calculations done automatically

4. **Audit Trail**
   - When promoted
   - From which grade
   - Academic performance
   - Attendance records

5. **Flexible Reporting**
   - Multi-year reports
   - Year-over-year comparison
   - Progress tracking

### ✅ Data Preserved

Each StudentHistory record includes:
- 📊 **Academic**: average_score, total_subjects, passed_subjects, failed_subjects
- 📅 **Attendance**: total_days, present_days, absent_days
- 🏫 **Classroom**: grade_name, classroom reference
- 📝 **Status**: ACTIVE, PROMOTED, GRADUATED, etc.
- 📆 **Dates**: start_date, end_date, promotion_date
- 💬 **Notes**: Any additional information

---

## 🔧 Configuration

### Student Status Options
```python
STATUS_CHOICES = [
    ('ACTIVE', 'សកម្ម (Active)'),           # Currently enrolled
    ('PROMOTED', 'ឡើងថ្នាក់ (Promoted)'),    # In history records
    ('GRADUATED', 'បញ្ចប់ (Graduated)'),     # Finished school
    ('TRANSFERRED', 'ផ្ទេរ (Transferred)'),  # Moved schools
    ('WITHDRAWN', 'ឈប់រៀន (Withdrawn)'),    # Stopped studying
    ('SUSPENDED', 'ផ្អាក (Suspended)'),      # Temporarily stopped
]
```

**Important**: 
- Current student record: `status = 'ACTIVE'`
- History records: `status = 'PROMOTED'` (or other appropriate status)

### Passing Percentage
Default: 50%
- Can be adjusted in promotion page
- Used to determine if student passed each subject

---

## 📈 Example Queries

### Get Student's Complete Academic Journey
```python
student = Student.objects.get(student_id='STU-0001')

# Current info
print(f"Current Grade: {student.classroom.grade}")
print(f"Status: {student.get_status_display()}")

# Historical progression
for record in student.history_records.order_by('academic_year__year'):
    print(f"\n{record.academic_year.year}:")
    print(f"  Grade: {record.grade_name}")
    print(f"  Average: {record.average_score}%")
    print(f"  Pass Rate: {record.passed_subjects}/{record.total_subjects}")
    print(f"  Attendance: {record.attendance_percentage()}%")
```

### Find All Students Who Repeated a Grade
```python
# Students with multiple history records for different years
from django.db.models import Count

students_with_history = Student.objects.annotate(
    history_count=Count('history_records')
).filter(history_count__gt=1)
```

### Generate Year-End Report
```python
year = AcademicYear.objects.get(year='2024-2025')
histories = StudentHistory.objects.filter(academic_year=year)

for history in histories:
    print(f"{history.student.student_id}: {history.grade_name}")
    print(f"  Average: {history.average_score}")
    print(f"  Status: {history.get_status_display()}")
```

---

## ⚠️ Important Notes

### DO ✅
- Use the promotion page to promote students (automatic history creation)
- Keep student status as ACTIVE for currently enrolled students
- Use history records to view past academic years
- Regularly backup database (history is valuable!)

### DON'T ❌
- Don't manually change student classroom without using promotion
- Don't delete StudentHistory records (permanent data loss)
- Don't set current students to PROMOTED status (only for history)
- Don't modify historical records after creation (audit integrity)

---

## 🛠️ Troubleshooting

### Issue: History not created during promotion
**Solution**: Check that:
- Student has an old_classroom with academic_year
- Student has scores for that academic year
- Promotion was done through `/school/students/promote/`

### Issue: Can't see history in student detail
**Solution**: 
- Check if history_records exist in database
- Verify template includes history section
- Check that student has been promoted at least once

### Issue: Wrong academic year data in history
**Solution**:
- History is created based on old_classroom.academic_year
- Ensure classroom has correct academic_year assigned
- Scores must be linked to same academic_year

---

## 📝 Summary

### What Changed
1. **New Model**: StudentHistory (migration 0015)
2. **Updated Views**: student_promote, student_detail
3. **New Admin**: StudentHistory admin interface
4. **Status Logic**: Students stay ACTIVE after promotion

### What Stays the Same
- Student model structure (added history relation)
- Student IDs remain constant
- Promotion workflow (UI unchanged)
- Score and attendance tracking

### Next Steps
- Test promotion with sample data
- Update templates if needed to show history
- Train staff on new history features
- Consider reports based on historical data

---

## 📞 Support

**Documentation**: See `STUDENT_HISTORY_SYSTEM.md` for complete details

**Database**: Migration `0015_studenthistory.py`

**Code Changes**:
- `school/models.py` - StudentHistory model
- `school/views.py` - Promotion logic
- `school/admin.py` - Admin interface

**Git Branch**: `feature/teacher-student-promotion`
**Commit**: "Add StudentHistory model to track student progression across grades"

---

**Status**: ✅ **Deployed & Ready to Use**  
**Date**: August 3, 2026  
**Version**: 1.0
