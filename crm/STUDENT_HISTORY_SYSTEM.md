# Student History & Promotion System
# ប្រព័ន្ធប្រវត្តិសិស្ស និងការឡើងថ្នាក់

## Overview | ទិដ្ឋភាពទូទៅ

This system tracks complete student history across academic years while maintaining a single active student record. When students are promoted to a new grade, the system:

1. **Creates a historical record** (StudentHistory) for the completed academic year
2. **Preserves all academic data**: scores, attendance, classroom info
3. **Updates the student record** to the new grade (status remains ACTIVE)
4. **Maintains continuity** with the same student_id across all years

ប្រព័ន្ធនេះតាមដានប្រវត្តិសិស្សពេញលេញតាមឆ្នាំសិក្សា ខណៈពេលរក្សាកំណត់ត្រាសិស្សសកម្មមួយ។ នៅពេលសិស្សឡើងថ្នាក់ថ្មី ប្រព័ន្ធនឹង៖
1. បង្កើតកំណត់ត្រាប្រវត្តិសម្រាប់ឆ្នាំសិក្សាដែលបានបញ្ចប់
2. រក្សាទុកទិន្នន័យសិក្សាទាំងអស់៖ ពិន្ទុ វត្តមាន ព័ត៌មានថ្នាក់រៀន
3. ធ្វើបច្ចុប្បន្នភាពកំណត់ត្រាសិស្សទៅថ្នាក់ថ្មី (status នៅតែជា ACTIVE)
4. រក្សាទំនាក់ទំនងជាមួយ student_id តែមួយគត់

---

## Database Schema | ស្ថាបត្យកម្មទិន្នន័យ

### StudentHistory Model

```python
class StudentHistory(models.Model):
    # Links
    student        = ForeignKey(Student)          # Link to main student record
    academic_year  = ForeignKey(AcademicYear)     # Which year this record is for
    classroom      = ForeignKey(Classroom)        # Which classroom they were in
    grade_name     = CharField                     # Grade name (stored for reference)
    status         = CharField                     # ACTIVE, PROMOTED, GRADUATED, etc.
    
    # Academic Performance
    average_score  = DecimalField                  # Average score for the year
    total_subjects = IntegerField                  # How many subjects
    passed_subjects = IntegerField                 # How many passed
    failed_subjects = IntegerField                 # How many failed
    
    # Attendance
    total_days     = IntegerField                  # Total school days
    present_days   = IntegerField                  # Days present
    absent_days    = IntegerField                  # Days absent
    
    # Dates
    start_date     = DateField                     # When started this grade
    end_date       = DateField                     # When completed/promoted
    
    # Notes
    notes          = TextField                     # Additional notes
```

### Key Features | លក្ខណៈពិសេស
- **Unique constraint**: One history record per student per academic year
- **Automatic calculation**: Attendance percentage computed on the fly
- **Preserves deleted data**: Even if classroom is deleted, grade_name is stored

---

## How Promotion Works | របៀបដំណើរការឡើងថ្នាក់

### Before Promotion | មុនពេលឡើងថ្នាក់
```
Student: STU-0001
├─ classroom: Grade 1-A (2024-2025)
├─ status: ACTIVE
└─ student_id: STU-0001
```

### During Promotion | ក្នុងពេលឡើងថ្នាក់
1. **Create StudentHistory record**:
   ```
   StudentHistory:
   ├─ student: STU-0001
   ├─ academic_year: 2024-2025
   ├─ classroom: Grade 1-A
   ├─ grade_name: "Grade 1 A"
   ├─ status: PROMOTED
   ├─ average_score: 85.5
   ├─ total_subjects: 8
   ├─ passed_subjects: 8
   ├─ failed_subjects: 0
   ├─ present_days: 180
   ├─ absent_days: 5
   └─ notes: "ឡើងថ្នាក់ទៅ Grade 2 នៅថ្ងៃទី 03/08/2026"
   ```

2. **Update Student record**:
   ```
   Student: STU-0001
   ├─ classroom: Grade 2-A (2025-2026)  ← Updated
   ├─ status: ACTIVE                     ← Stays active
   ├─ previous_classroom: "Grade 1-A"   ← Updated
   ├─ promotion_date: 2026-08-03        ← Updated
   └─ student_id: STU-0001              ← Unchanged
   ```

### After Promotion | បន្ទាប់ពីឡើងថ្នាក់
```
Student: STU-0001
├─ Current: Grade 2-A (2025-2026) - ACTIVE
└─ History:
    └─ 2024-2025: Grade 1-A - PROMOTED (85.5% avg)
```

---

## Code Implementation | ការអនុវត្តកូដ

### Promotion View Enhancement

The `student_promote` view now:

1. **Calculates academic performance** for the year:
   ```python
   year_scores = student.scores.filter(academic_year=year)
   avg_score = sum(s.score for s in year_scores) / total_subjects
   passed = sum(1 for s in year_scores if s.is_passing())
   ```

2. **Calculates attendance** for the year:
   ```python
   year_attendance = student.attendances.filter(date__range=[start, end])
   total_days = year_attendance.count()
   present_days = year_attendance.filter(status='P').count()
   ```

3. **Creates history record**:
   ```python
   StudentHistory.objects.update_or_create(
       student=student,
       academic_year=year,
       defaults={
           'classroom': old_classroom,
           'grade_name': str(old_classroom.grade),
           'status': 'PROMOTED',
           'average_score': avg_score,
           # ... other fields
       }
   )
   ```

4. **Updates student** to new grade (status = ACTIVE)

### Student Detail View Enhancement

The `student_detail` view now includes:
```python
history_records = student.history_records.order_by('-academic_year__year')
```

---

## Admin Interface | ចំណុចប្រទាក់រដ្ឋបាល

### StudentHistory Admin
- **List display**: Student ID, Grade, Year, Status, Scores, Attendance
- **Filters**: Status, Academic Year, Grade
- **Search**: By student ID or name
- **Readonly**: Created/Updated timestamps
- **Organized fieldsets**: Basic info, Academic, Attendance, Dates, Notes

### Accessing History
1. Go to Django Admin: `/admin/school/studenthistory/`
2. View all historical records
3. Filter by academic year or student
4. See complete progression of each student

---

## Benefits | អត្ថប្រយោជន៍

### For Administrators | សម្រាប់អ្នកគ្រប់គ្រង
✅ **Complete audit trail** - Full history of every student's academic journey
✅ **Data integrity** - Historical data preserved even if current records change
✅ **Reporting** - Easy to generate multi-year reports
✅ **Analytics** - Track student progression and performance trends

### For Teachers | សម្រាប់គ្រូបង្រៀន
✅ **Student background** - See previous year performance
✅ **Identify patterns** - Spot improving or declining students
✅ **Informed decisions** - Better understanding of student capabilities

### For Parents | សម្រាប់ឪពុកម្តាយ
✅ **Progress tracking** - See child's growth across years
✅ **Historical comparison** - Compare performance year-over-year
✅ **Transparency** - Full academic record available

---

## Usage Examples | ឧទាហរណ៍ការប្រើប្រាស់

### Promote Students
1. Go to: `/school/students/promote/`
2. Select classroom and academic year
3. System shows eligible students
4. Select students to promote
5. Choose destination classroom
6. Click "Promote" → History automatically created

### View Student History
1. Go to student detail page
2. History records displayed in table
3. Shows: Year, Grade, Status, Scores, Attendance

### Query Student History (API/Code)
```python
# Get all history for a student
history = student.history_records.all()

# Get specific year
history_2024 = student.history_records.get(academic_year__year='2024-2025')

# Get promoted records only
promoted = student.history_records.filter(status='PROMOTED')

# Calculate total years
years_in_school = student.history_records.count()
```

---

## Future Enhancements | ការកែលម្អនាពេលអនាគត

### Planned Features
- 📊 **Multi-year reports**: Generate reports spanning multiple academic years
- 📈 **Progress graphs**: Visual charts showing student improvement
- 🏆 **Achievement tracking**: Badges/awards across years
- 📄 **Transcript generation**: Official academic transcripts from history
- 🔄 **Grade repetition**: Handle students who repeat a grade
- 📤 **Export history**: CSV/PDF export of complete student history

### API Integration
- RESTful API endpoints for history access
- Bulk history creation/updates
- Historical data analytics endpoints

---

## Database Migration | ការផ្លាស់ប្តូរមូលដ្ឋានទិន្នន័យ

**Migration file**: `school/migrations/0015_studenthistory.py`

**Applied**: ✅ Successfully migrated

**Rollback**: To rollback, run:
```bash
python manage.py migrate school 0014
```

---

## Testing Checklist | បញ្ជីពិនិត្យសាកល្បង

- [x] StudentHistory model created
- [x] Migration generated and applied
- [x] Admin interface configured
- [x] Promotion view updated with history creation
- [x] Student detail view shows history
- [x] Status remains ACTIVE after promotion
- [x] History preserves complete academic data
- [ ] Template updated to display history (if needed)
- [ ] Test promotion with real data
- [ ] Verify history records are created correctly

---

## Support | ជំនួយ

For questions or issues:
- Review this documentation
- Check Django admin for history records
- Examine migration file for database changes
- Test in development before production use

---

**Created**: August 3, 2026  
**Version**: 1.0  
**Status**: ✅ Implemented & Migrated
