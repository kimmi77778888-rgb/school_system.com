# ប្រព័ន្ធឡើងថ្នាក់និងរក្សាប្រវត្តិកាសិក្សាតាមជំហាននៃកម្ពុជា
# Cambodia Student Promotion and History System

## 📚 ប្រព័ន្ធអប់រំកម្ពុជា | Cambodia Education System

### ជំហាននៃការសិក្សា | Education Levels

```
បឋមសិក្សា (Primary Education)
├── ថ្នាក់ទី១ (Grade 1)
├── ថ្នាក់ទី២ (Grade 2)
├── ថ្នាក់ទី៣ (Grade 3)
├── ថ្នាក់ទី៤ (Grade 4)
├── ថ្នាក់ទី៥ (Grade 5)
└── ថ្នាក់ទី៦ (Grade 6) → ផ្ទេរទៅបឋមភូមិ

បឋមភូមិ (Lower Secondary Education)
├── ថ្នាក់ទី៧ (Grade 7)
├── ថ្នាក់ទី៨ (Grade 8)
└── ថ្នាក់ទី៩ (Grade 9) → ផ្ទេរទៅមធ្យមភូមិ

មធ្យមភូមិ (Upper Secondary Education)
├── ថ្នាក់ទី១០ (Grade 10)
├── ថ្នាក់ទី១១ (Grade 11)
└── ថ្នាក់ទី១២ (Grade 12) → បញ្ចប់ការសិក្សា
```

## 🎯 លក្ខណៈពិសេសនៃប្រព័ន្ធ | System Features

### 1. **Grade Model** - បានកែលម្អ
- `level`: កម្រិតថ្នាក់ (primary, lower_secondary, upper_secondary)
- `grade_number`: លេខថ្នាក់ពី 1-12
- `get_next_grade_level()`: function កំណត់កម្រិតបន្ទាប់

### 2. **StudentHistory Model** - បានពង្រីក
រក្សាទុកព័ត៌មានពេញលេញសម្រាប់ម្យួឆ្នាំសិក្សា:

#### ព័ត៌មានថ្នាក់រៀន | Grade Information
- `grade_name`: ឈ្មោះថ្នាក់ (សម្រាប់ history)
- `grade_number`: លេខថ្នាក់ (1-12)
- `grade_level`: កម្រិតថ្នាក់

#### ព័ត៌មានពិន្ទុ | Academic Performance
- `average_score`: ពិន្ទុមធ្យម
- `total_subjects`: ចំនួនមុខវិជ្ជាសរុប
- `passed_subjects`: ចំនួនមុខជាប់
- `failed_subjects`: ចំនួនមុខធ្លាក់

#### ព័ត៌មានវត្តមាន | Attendance
- `total_days`: ថ្ងៃសរុប
- `present_days`: ថ្ងៃមកវត្តមាន
- `absent_days`: ថ្ងៃអវត្តមាន

#### ព័ត៌មានការឡើងថ្នាក់ | Promotion Details
- `promoted_to`: ឡើងថ្នាក់ទៅណា
- `promotion_note`: កំណត់សំគាល់ពិសេស (រួមទាំងការផ្ទេរកម្រិត)

### 3. **Student Promotion Logic** - កែតម្រូវពេញលេញ

#### តក្កវិធីឡើងថ្នាក់ | Promotion Logic
```python
# ជាប់/ធ្លាក់ផ្អែកលើពិន្ទុមធ្យម
can_promote = avg_percentage >= passing_percentage and total_subjects > 0

# លំនាំដើម: 50%
passing_percentage = 50
```

#### ការផ្ទេរកម្រិត | Level Transition Detection
```python
# ថ្នាក់ទី៦ → ថ្នាក់ទី៧ (បឋមសិក្សា → បឋមភូមិ)
if old_grade_number == 6 and new_grade_number == 7:
    level_transition = "ផ្ទេរពីបឋមសិក្សាទៅបឋមភូមិ"

# ថ្នាក់ទី៩ → ថ្នាក់ទី១០ (បឋមភូមិ → មធ្យមភូមិ)
if old_grade_number == 9 and new_grade_number == 10:
    level_transition = "ផ្ទេរពីបឋមភូមិទៅមធ្យមភូមិ"

# ថ្នាក់ទី១២ (បញ្ចប់ការសិក្សា)
if old_grade_number == 12:
    level_transition = "បញ្ចប់ការសិក្សា"
```

#### Strict Grade Progression
```python
# អនុញ្ញាតឡើងតែថ្នាក់បន្ទាប់ប៉ុណ្ណោះ
# Only allow promotion to immediate next grade
if classroom.grade.grade_number == current_grade_num + 1:
    next_classrooms.append(classroom)
```

## 📝 របៀបប្រើប្រាស់ | Usage Guide

### ជំហានទី១: រៀបចំថ្នាក់រៀន | Setup Grades

```python
# ឧទាហរណ៍: បង្កើតថ្នាក់បឋមសិក្សា
Grade.objects.create(
    name="Grade 1",
    level="primary",
    grade_number=1
)

Grade.objects.create(
    name="Grade 6", 
    level="primary",
    grade_number=6
)

# ថ្នាក់បឋមភូមិ
Grade.objects.create(
    name="Grade 7",
    level="lower_secondary", 
    grade_number=7
)
```

### ជំហានទី២: ឡើងថ្នាក់សិស្ស | Promote Students

1. ចូលទៅ **School → Students → Promote Students** (ឡើងថ្នាក់)
2. ជ្រើសរើស **Current Classroom** (ថ្នាក់បច្ចុប្បន្ន)
3. ជ្រើសរើស **Academic Year** (ឆ្នាំសិក្សា) - optional
4. កំណត់ **Passing Percentage** (ពិន្ទុជាប់) - default 50%
5. ចុច **ពិនិត្យលទ្ធផល** ដើម្បីមើលបញ្ជីសិស្ស
6. ជ្រើសរើស **Next Classroom** (ថ្នាក់ថ្មី)
7. ធីកសិស្សដែលចង់ឡើងថ្នាក់
8. ចុច **ដាក់ឡើងថ្នាក់**

### ជំហានទី៣: មើលប្រវត្តិ | View History

រក្សាប្រវត្តិកាសិក្សាដោយស្វ័យប្រវត្តិនៅក្នុង `StudentHistory`:
- មួយកំណត់ត្រាសម្រាប់មួយឆ្នាំសិក្សា
- រក្សាទុកពិន្ទុ, វត្តមាន, ថ្នាក់រៀន
- សិស្សរក្សា status `ACTIVE` តែមានប្រវត្តិពេញលេញ

## 🔍 ការផ្ទេរកម្រិតពិសេស | Special Level Transitions

### ពីបឋមសិក្សាទៅបឋមភូមិ | Primary → Lower Secondary
```
ថ្នាក់ទី៦ (Grade 6) → ថ្នាក់ទី៧ (Grade 7)
- ប្រព័ន្ធនឹងកត់ត្រា: "ផ្ទេរពីបឋមសិក្សាទៅបឋមភូមិ"
- សិស្សនឹងមាន note: "(ចូលបឋមភូមិ)"
```

### ពីបឋមភូមិទៅមធ្យមភូមិ | Lower Secondary → Upper Secondary
```
ថ្នាក់ទី៩ (Grade 9) → ថ្នាក់ទី១០ (Grade 10)
- ប្រព័ន្ធនឹងកត់ត្រា: "ផ្ទេរពីបឋមភូមិទៅមធ្យមភូមិ"
- សិស្សនឹងមាន note: "(ចូលមធ្យមភូមិ)"
```

### បញ្ចប់ការសិក្សា | Graduation
```
ថ្នាក់ទី១២ (Grade 12)
- ប្រព័ន្ធនឹងកត់ត្រា: "បញ្ចប់ការសិក្សា (Graduated)"
- សិស្សអាចប្តូរ status ជា "GRADUATED"
```

## 💾 ទិន្នន័យដែលរក្សាទុក | Data Preserved

សម្រាប់មួយឆ្នាំសិក្សា, ប្រព័ន្ធរក្សា:

### ✅ ពិន្ទុ | Scores
- មធ្យមភាគពិន្ទុ
- ចំនួនមុខជាប់/ធ្លាក់
- ភាគរយជាប់

### ✅ វត្តមាន | Attendance  
- ថ្ងៃសរុប
- ថ្ងៃមកវត្តមាន/អវត្តមាន
- ភាគរយវត្តមាន

### ✅ ថ្នាក់រៀន | Grade Info
- ឈ្មោះថ្នាក់
- លេខថ្នាក់
- កម្រិតថ្នាក់

### ✅ ការឡើងថ្នាក់ | Promotion
- ឡើងថ្នាក់ទៅណា
- ថ្ងៃឡើងថ្នាក់
- កំណត់សំគាល់ពិសេស

## 🎓 ឧទាហរណ៍ History Record

```python
StudentHistory:
  student: "STU-0001 - សុខ សុផល"
  academic_year: "2024-2025"
  grade_name: "Grade 6"
  grade_number: 6
  grade_level: "primary"
  average_score: 75.5
  total_subjects: 8
  passed_subjects: 8
  failed_subjects: 0
  total_days: 180
  present_days: 175
  absent_days: 5
  promoted_to: "Grade 7 A | 2025-2026"
  promotion_note: "ឡើងថ្នាក់ទៅ Grade 7 នៅថ្ងៃទី 15/06/2025 | ផ្ទេរពីបឋមសិក្សាទៅបឋមភូមិ"
  notes: "ពិន្ទុមធ្យម: 75.5 | វត្តមាន: 175/180 ថ្ងៃ (97.2%)"
```

## 🔧 Technical Details

### Database Schema
```sql
-- Grade table
ALTER TABLE school_grade ADD COLUMN level VARCHAR(20) DEFAULT 'primary';
ALTER TABLE school_grade ADD COLUMN grade_number INTEGER NULL;

-- StudentHistory table  
ALTER TABLE school_studenthistory ADD COLUMN grade_number INTEGER NULL;
ALTER TABLE school_studenthistory ADD COLUMN grade_level VARCHAR(20) DEFAULT '';
ALTER TABLE school_studenthistory ADD COLUMN promoted_to VARCHAR(200) DEFAULT '';
ALTER TABLE school_studenthistory ADD COLUMN promotion_note TEXT DEFAULT '';
```

### Migration
```bash
python manage.py makemigrations school
python manage.py migrate school
```

File: `school/migrations/0016_alter_grade_options_grade_grade_number_grade_level_and_more.py`

## 📊 Reports & Analytics

### សិស្សឡើងថ្នាក់ | Promotion Statistics
```python
# ចំនួនសិស្សឡើងថ្នាក់ក្នុងមួយឆ្នាំ
promoted_students = StudentHistory.objects.filter(
    academic_year__year="2024-2025",
    status="PROMOTED"
).count()

# អត្រាការឡើងថ្នាក់
promotion_rate = (promoted_students / total_students) * 100
```

### ការផ្ទេរកម្រិត | Level Transitions
```python
# សិស្សផ្ទេរពីបឋមទៅបឋមភូមិ
primary_to_lower = StudentHistory.objects.filter(
    grade_number=6,
    promotion_note__contains="ផ្ទេរពីបឋមសិក្សាទៅបឋមភូមិ"
).count()

# សិស្សផ្ទេរពីបឋមភូមិទៅមធ្យមភូមិ  
lower_to_upper = StudentHistory.objects.filter(
    grade_number=9,
    promotion_note__contains="ផ្ទេរពីបឋមភូមិទៅមធ្យមភូមិ"
).count()
```

## 🌟 Best Practices

### 1. កំណត់ grade_number ឱ្យត្រឹមត្រូវ
```python
# ត្រឹមត្រូវ
Grade(name="Grade 1", grade_number=1, level="primary")
Grade(name="Grade 7", grade_number=7, level="lower_secondary")

# មិនត្រឹមត្រូវ  
Grade(name="Grade 1", grade_number=None)  # ❌
```

### 2. ពិនិត្យការផ្ទេរកម្រិត
- ថ្នាក់ទី៦ → ថ្នាក់ទី៧: ត្រូវផ្ទេរកម្រិត ✅
- ថ្នាក់ទី៦ → ថ្នាក់ទី៨: មិនគួរអនុញ្ញាត ❌

### 3. រក្សាប្រវត្តិពេញលេញ
- រក្សាទុកពិន្ទុមុននឹងឡើងថ្នាក់
- រក្សាទុកវត្តមានមុននឹងឡើងថ្នាក់
- កត់ត្រាកាលបរិច្ឆេទត្រឹមត្រូវ

## 🔗 Related Files

- `school/models.py` - Grade, StudentHistory models
- `school/views.py` - student_promote function
- `school/templates/school/student_promote.html` - UI template
- `school/migrations/0016_*.py` - Database migration

## 📞 Support

សម្រាប់ជំនួយបន្ថែម សូមពិនិត្យ:
- [Student Promotion Guide](STUDENT_PROMOTION_GUIDE.md)
- [API Documentation](API_DOCUMENTATION.md)
- GitHub Issues: https://github.com/kimmi77778888-rgb/school_system.com/issues

---

**ចុងក្រោយធ្វើបច្ចុប្បន្នភាព:** ថ្ងៃទី 04/08/2026  
**កំណែ:** 2.0 - Cambodia Education System Aligned
