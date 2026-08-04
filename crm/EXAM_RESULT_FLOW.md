# Exam Result System - Navigation Flow
## ប្រព័ន្ធលទ្ធផលប្រឡង - លំហូរការប្រើប្រាស់

## 🗺️ Navigation Map

```
┌─────────────────────────────────────────────────────────────────┐
│                      EXAM LIST PAGE                              │
│                    /exams/                                       │
│                                                                  │
│  ┌──────────┬──────────┬──────────┬──────────┬──────────┐     │
│  │ Exam 1   │ Exam 2   │ Exam 3   │ Exam 4   │ Exam 5   │     │
│  │ [👁️][✏️][🗑️]│ [👁️][✏️][🗑️]│ [👁️][✏️][🗑️]│ [👁️][✏️][🗑️]│ [👁️][✏️][🗑️]│     │
│  └──────────┴──────────┴──────────┴──────────┴──────────┘     │
│                                                                  │
│  Click 👁️ to view exam details ──────────────────────┐         │
└──────────────────────────────────────────────────────┼─────────┘
                                                        │
                                                        ▼
┌─────────────────────────────────────────────────────────────────┐
│                   EXAM DETAIL PAGE                               │
│                /exams/<exam_id>/                                 │
│                                                                  │
│  ┌─────────────────────────────────────────────────────┐       │
│  │ 📋 Exam Information                                  │       │
│  │ Name: Midterm Math Exam                             │       │
│  │ Subject: Mathematics | Class: Grade 7A              │       │
│  │ Date: 2026-07-15 | Max Score: 100                   │       │
│  └─────────────────────────────────────────────────────┘       │
│                                                                  │
│  ┌───────────┬───────────┬───────────┬───────────┐             │
│  │📊 Total   │📝 Results │✅ Passed  │📈 Average │             │
│  │ Students  │ Submitted │ Students  │ Score     │             │
│  │    30     │ 28 (93%)  │ 25 (89%) │ 78.5/100  │             │
│  └───────────┴───────────┴───────────┴───────────┘             │
│                                                                  │
│  ┌─────────────────────────────────────────────────────┐       │
│  │ 📊 Grade Distribution                                │       │
│  │  A: 8  |  B: 10  |  C: 7  |  D: 2  |  F: 1          │       │
│  └─────────────────────────────────────────────────────┘       │
│                                                                  │
│  ┌──────────────────┬──────────────────┐                       │
│  │ 🏆 Top Performers│ ⚠️ Need Help     │                       │
│  │ #1 Sokha (95%)   │ Dara (48%)       │                       │
│  │ #2 Veasna (92%)  │ Bopha (45%)      │                       │
│  │ #3 Pisey (90%)   │                  │                       │
│  └──────────────────┴──────────────────┘                       │
│                                                                  │
│  ┌─────────────────────────────────────────────────────┐       │
│  │ 📋 All Student Results                               │       │
│  │ ┌────┬────────┬──────┬─────┬──────┬────┬──────┐    │       │
│  │ │#   │ID      │Name  │Score│%     │Grad│Action│    │       │
│  │ ├────┼────────┼──────┼─────┼──────┼────┼──────┤    │       │
│  │ │1   │STU-001 │Sokha │95   │95%   │A   │ 👁️   │ ──┼───┐   │
│  │ │2   │STU-002 │Veasna│92   │92%   │A   │ 👁️   │    │   │   │
│  │ │... │...     │...   │...  │...   │... │...   │    │   │   │
│  │ └────┴────────┴──────┴─────┴──────┴────┴──────┘    │   │   │
│  └─────────────────────────────────────────────────────┘   │   │
│                                                              │   │
│  Click 👁️ next to student name ─────────────────────────────┤   │
└──────────────────────────────────────────────────────────────┼───┘
                                                                │
                                                                ▼
┌─────────────────────────────────────────────────────────────────┐
│              INDIVIDUAL EXAM RESULT DETAIL                       │
│              /exam-results/<result_id>/                          │
│                                                                  │
│  ┌──────────────────┬─────────────────────────────────┐        │
│  │ 👤 Student Info  │ 📋 Exam Info                     │        │
│  │ ┌──────────┐     │ Name: Midterm Math Exam          │        │
│  │ │  Photo   │     │ Subject: Mathematics             │        │
│  │ └──────────┘     │ Date: 2026-07-15                 │        │
│  │ Sokha            │ Max Score: 100                   │        │
│  │ STU-001          │ Passing: 50                      │        │
│  │ Grade 7A         │                                  │        │
│  └──────────────────┴─────────────────────────────────┘        │
│                                                                  │
│  ┌─────────────────────────────────────────────────────┐       │
│  │ 🎯 RESULT                                            │       │
│  │ ┌──────────┬──────────┬──────────┬──────────┐       │       │
│  │ │  Score   │ Percent  │  Grade   │  Status  │       │       │
│  │ │   95     │   95%    │    A     │   ✅     │       │       │
│  │ │  /100    │          │          │   ជាប់    │       │       │
│  │ └──────────┴──────────┴──────────┴──────────┘       │       │
│  │                                                       │       │
│  │ ┌──────────────────┬──────────────────┐             │       │
│  │ │ 📊 Class Rank    │ 📈 Class Average │             │       │
│  │ │ #1 out of 28     │ 78.5/100         │             │       │
│  │ │                  │ ⬆️ Above average │             │       │
│  │ └──────────────────┴──────────────────┘             │       │
│  │                                                       │       │
│  │ 🎫 Attendance: ✅ Present                            │       │
│  └─────────────────────────────────────────────────────┘       │
│                                                                  │
│  ┌─────────────────────────────────────────────────────┐       │
│  │ 💬 Teacher Feedback                                  │       │
│  │ General: Excellent work! Shows strong understanding  │       │
│  │ Strengths: Problem-solving, clear explanations      │       │
│  │ To Improve: Speed up calculations                   │       │
│  └─────────────────────────────────────────────────────┘       │
│                                                                  │
│  ┌─────────────────────────────────────────────────────┐       │
│  │ 📊 Performance History - Mathematics                 │       │
│  │ ┌────────────┬─────┬────┬─────┬────────┐            │       │
│  │ │ Date       │Type │Scor│%    │Grade   │            │       │
│  │ ├────────────┼─────┼────┼─────┼────────┤            │       │
│  │ │ 2026-05-10 │Quiz │48/5│96%  │A       │            │       │
│  │ │ 2026-04-15 │Test │42/5│84%  │B       │            │       │
│  │ │ ...        │...  │... │...  │...     │            │       │
│  │ └────────────┴─────┴────┴─────┴────────┘            │       │
│  └─────────────────────────────────────────────────────┘       │
│                                                                  │
│  [⬅️ Back to Exam]  [👤 View Student Profile]                  │
└──────────────────────────────────────────────────────────────────┘
```

## 🔄 Data Flow

```
Exam Model                ExamResult Model              Student Model
───────────               ────────────────              ─────────────
- exam_id                 - exam (FK → Exam)           - student_id
- name                    - student (FK → Student)     - first_name
- subject                 - score                      - last_name
- classroom               - grade_letter               - classroom
- date                    - percentage()               - photo
- max_score               - is_passed                  
- passing_score           - rank_in_class              
                          - was_present                
                          - remarks                    
                          - strengths                  
                          - areas_to_improve           
```

## 📊 Statistics Calculation

### Exam Detail Level
```python
total_students = exam.classroom.students.filter(is_active=True).count()
total_results = exam.exam_results.count()
completion_rate = (total_results / total_students) * 100

avg_score = exam.exam_results.aggregate(Avg('score'))['score__avg']
passed_count = exam.exam_results.filter(is_passed=True).count()
pass_rate = (passed_count / total_results) * 100

grade_distribution = {
    'A': exam.exam_results.filter(grade_letter='A').count(),
    'B': exam.exam_results.filter(grade_letter='B').count(),
    # ... etc
}
```

### Individual Result Level
```python
percentage = (result.score / result.exam.max_score) * 100

# Grade letter assignment (auto-calculated on save)
if percentage >= 90: grade = 'A'
elif percentage >= 80: grade = 'B'
elif percentage >= 70: grade = 'C'
elif percentage >= 60: grade = 'D'
else: grade = 'F'

# Rank calculation
better_results = ExamResult.objects.filter(
    exam=result.exam, 
    score__gt=result.score
).count()
rank = better_results + 1
```

## 🎨 UI Components

### Cards Used
- **Info Cards**: Exam/student information
- **Stat Cards**: Numbers with icons
- **Alert Cards**: Warnings/messages
- **List Group Items**: Clickable result lists
- **Tables**: Detailed data display

### Colors & Badges
- **Primary (Blue)**: General information
- **Success (Green)**: Pass, A grade
- **Info (Light Blue)**: B grade, statistics
- **Warning (Yellow)**: D grade, needs attention
- **Danger (Red)**: Fail, F grade, absent

### Icons (Bootstrap Icons)
- 📊 `bi-clipboard-data` - Exam detail
- 📝 `bi-file-earmark-text` - Individual result
- 👁️ `bi-eye` - View action
- ✏️ `bi-pencil` - Edit action
- 🗑️ `bi-trash` - Delete action
- 🏆 `bi-trophy` - Top performers
- ⚠️ `bi-exclamation-triangle` - Warning
- ✅ `bi-check-circle` - Success/pass
- ❌ `bi-x-circle` - Fail
- 📈 `bi-graph-up` - Statistics

## 🚦 Access Control

```
User Role Check
├── Admin
│   └── ✅ Can view all exams and results
├── Teacher
│   └── ✅ Can view exams for their assigned classrooms
├── Parent
│   └── ❌ Use parent portal instead
└── Student
    └── ❌ Use student portal instead
```

## 💾 Database Relationships

```
ExamResult
├── exam (FK) ──────→ Exam
│                     ├── subject (FK) ─→ Subject
│                     ├── classroom (FK) → Classroom
│                     ├── exam_type (FK) → ExamType
│                     └── academic_year (FK) → AcademicYear
│
└── student (FK) ───→ Student
                      └── classroom (FK) → Classroom
```

---

**This visual guide helps understand:**
- How pages connect to each other
- What data is displayed on each page
- How statistics are calculated
- UI component organization
- Access control flow
