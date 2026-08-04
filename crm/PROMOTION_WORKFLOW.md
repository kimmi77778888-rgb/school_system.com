# ទំនាក់ទំនងរវាង Exams, Exam Results និង Student Promotion
# Relationship Between 3 Options: Exams → Results → Promotion

## 🔗 ទំនាក់ទំនងនៃប្រព័ន្ធ | System Relationship

```
┌─────────────────────────────────────────────────────────────┐
│                  STEP 1: CREATE EXAMS                       │
│                  📄 ការប្រឡង (Exams)                       │
├─────────────────────────────────────────────────────────────┤
│  • បង្កើតការប្រឡង (Create Exam)                            │
│  • កំណត់: មុខវិជ្ជា, ថ្នាក់, ឆ្នាំសិក្សា                   │
│  • ឧទាហរណ៍: Midterm Exam - Math - Grade 2 - 2026          │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│               STEP 2: ENTER EXAM RESULTS                    │
│            📊 លទ្ធផលប្រឡង (Exam Results)                  │
├─────────────────────────────────────────────────────────────┤
│  • បញ្ចូលពិន្ទុក្នុង Grade Book                              │
│  • រក្សាទុកជា Score model                                   │
│  • Score.exam = Exam (FK relationship)                      │
│  • Score.student, subject, exam_type, academic_year         │
│  • ឧទាហរណ៍:                                                 │
│    - សុខ សុផល: រូបវិទ្យា 85/100 (Midterm)                   │
│    - សុខ សុផល: គណិតវិទ្យា 90/100 (Midterm)                 │
│    - សុខ សុផល: វិទ្យាសាស្រ្ត 78/100 (Midterm)               │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│            STEP 3: PROMOTE STUDENTS                         │
│               🔼 ឡើងថ្នាក់ (Promotion)                      │
├─────────────────────────────────────────────────────────────┤
│  • អាន Score ពីគ្រប់ Exam                                   │
│  • គណនាពិន្ទុមធ្យម (Average from all scores)                │
│  • ពិនិត្យវត្តមាន (Check attendance)                          │
│  • កំណត់សិទ្ធិឡើងថ្នាក់:                                    │
│    ✅ ពិន្ទុមធ្យម ≥ 50%                                      │
│    ✅ វត្តមាន ≥ 80%                                          │
│    ✅ មានពិន្ទុយ៉ាងហោចណាស់ 1 មុខ                            │
│  • បង្កើត StudentHistory (preserve data)                   │
│  • ផ្លាស់ប្តូរថ្នាក់សិស្ស                                     │
└─────────────────────────────────────────────────────────────┘
```

## 📊 Database Relationships

```sql
Exam (ការប្រឡង)
├── id
├── name
├── exam_type_id (FK → ExamType)
├── subject_id (FK → Subject)
├── classroom_id (FK → Classroom)
├── academic_year_id (FK → AcademicYear)
└── date

     ↓ (One-to-Many)

Score (លទ្ធផល)
├── id
├── student_id (FK → Student)
├── subject_id (FK → Subject)
├── exam_type_id (FK → ExamType)
├── exam_id (FK → Exam) ⭐ THIS IS THE CONNECTION
├── academic_year_id (FK → AcademicYear)
├── score
└── max_score

     ↓ (Aggregation in Promotion Logic)

Promotion System (ឡើងថ្នាក់)
├── Reads all Score records for student
├── Groups by student and academic_year
├── Calculates average: SUM(score)/COUNT(*)
├── Checks eligibility
└── Creates StudentHistory
```

## 💡 How They Work Together

### Example: Student "សុខ សុផល" Promotion

#### Step 1: Teacher Creates Exams
```
Exam 1: Midterm - រូបវិទ្យា - ថ្នាក់ទី២ - 2026
Exam 2: Midterm - គណិតវិទ្យា - ថ្នាក់ទី២ - 2026  
Exam 3: Midterm - វិទ្យាសាស្រ្ត - ថ្នាក់ទី២ - 2026
Exam 4: Midterm - ភាសាខ្មែរ - ថ្នាក់ទី២ - 2026
```

#### Step 2: Teacher Enters Scores (in Grade Book)
```
Score 1: សុខ សុផល - រូបវិទ្យា - 85/100 - Exam 1
Score 2: សុខ សុផល - គណិតវិទ្យា - 90/100 - Exam 2
Score 3: សុខ សុផល - វិទ្យាសាស្រ្ត - 78/100 - Exam 3  
Score 4: សុខ សុផល - ភាសាខ្មែរ - 82/100 - Exam 4
```

#### Step 3: Promotion System Calculates
```python
# Get all scores for student
scores = Score.objects.filter(
    student=student,
    academic_year=academic_year
)

# Calculate average
total_subjects = scores.count()  # = 4
avg_percentage = sum(score.percentage() for score in scores) / total_subjects

# Calculation:
# (85 + 90 + 78 + 82) / 4 = 335 / 4 = 83.75%

# Check eligibility
can_promote = (
    avg_percentage >= 50 and      # ✅ 83.75% >= 50%
    total_subjects > 0 and         # ✅ 4 > 0
    attendance_rate >= 80.0        # ✅ Need to check attendance
)
```

#### Result: ✅ សុខ សុផល អាចឡើងថ្នាក់បាន!

## 🔄 Complete Workflow

### For Teachers:

1. **ចូលទៅ "ការប្រឡង" (Exams)**
   - បង្កើតការប្រឡងថ្មី
   - កំណត់មុខវិជ្ជា, ថ្នាក់, ឆ្នាំ

2. **ចូលទៅ "លទ្ធផលប្រឡង" (Exam Results)**
   - ចុច "បញ្ជីពិន្ទុតារាង" (Grade Book Grid)
   - ជ្រើសថ្នាក់, ឆ្នាំ, ប្រភេទប្រឡង
   - បញ្ចូលពិន្ទុគ្រប់មុខវិជ្ជា
   - រក្សាទុក

3. **ចូលទៅ "ឡើងថ្នាក់" (Promotion)**
   - ជ្រើសថ្នាក់បច្ចុប្បន្ន
   - ប្រព័ន្ធបង្ហាញសិស្សដែលអាចឡើងថ្នាក់ (based on scores from step 2)
   - ជ្រើសថ្នាក់ថ្មី
   - ដាក់ឡើងថ្នាក់

## 🎯 Key Points

### ✅ Relationships Exist:
1. **Exam → Score**: `Score.exam` is a ForeignKey to `Exam`
2. **Score → Promotion**: Promotion reads all `Score` records
3. **Score.exam** preserves which exam the score came from

### ✅ Data Flow:
```
Exam (created first)
  ↓
Score (linked to exam)
  ↓  
Promotion (reads all scores)
  ↓
StudentHistory (preserves everything)
```

### ✅ What Gets Calculated in Promotion:
- **Average** = (Score1% + Score2% + Score3% + ...) / Total Subjects
- **Attendance** = Present Days / Total Days × 100%
- **Eligibility** = Average ≥ 50% AND Attendance ≥ 80% AND Has Scores

## 📝 Code Implementation

### In views.py (student_promote function):

```python
# Get scores for student
if academic_year_id:
    scores = student.scores.filter(academic_year=academic_year)
else:
    scores = student.scores.filter(academic_year=current_classroom.academic_year)

# Calculate average
total_subjects = scores.count()
avg_percentage = sum(score.percentage() for score in scores) / total_subjects

# These scores can come from ANY exam
# The relationship is: Score → Exam (via exam_id)
# So promotion uses scores from ALL exams automatically
```

## 🎓 Summary

**The 3 options ARE connected:**

1. 📄 **Exams** - Create exam definitions
2. 📊 **Exam Results** - Enter scores (linked to exams via `Score.exam`)
3. 🔼 **ឡើងថ្នាក់** - Uses ALL scores to calculate promotion eligibility

**The relationship works automatically** - when you enter scores in the Grade Book, they're saved with the exam reference, and when you promote students, the system reads all those scores regardless of which exam they came from.

---

**Created:** 04/08/2026  
**Status:** ✅ Fully Connected and Working
