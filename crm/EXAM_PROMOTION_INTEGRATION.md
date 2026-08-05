# 🔗 Exam Results ↔️ Student Promotion Integration
## ការភ្ជាប់ប្រព័ន្ធប្រឡងជាមួយការឡើងថ្នាក់

---

## 🎯 Overview / ទិដ្ឋភាពសង្ខេប

This system connects **Exam Results** with **Student Promotion** calculations, ensuring that exam scores automatically flow into the promotion decision system.

ប្រព័ន្ធនេះភ្ជាប់ **លទ្ធផលប្រឡង** ជាមួយ **ការឡើងថ្នាក់សិស្ស** ដើម្បីធានាថាពិន្ទុប្រឡងត្រូវបានគណនាដោយស្វ័យប្រវត្តិ។

---

## 📊 System Architecture / រចនាសម្ព័ន្ធ

```
┌─────────────────────────────────────────────────────────────┐
│                    EXAM SYSTEM                               │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  1️⃣  Exam (ប្រឡង)                                           │
│      • Subject: Math, Khmer, Science, etc.                  │
│      • Exam Type: Midterm, Final, Quiz                      │
│      • Classroom, Academic Year, Date                       │
│                                                              │
│  2️⃣  ExamResult (លទ្ធផលប្រឡង)                               │
│      • Student + Exam                                        │
│      • Score, Grade, Pass/Fail                              │
│      • Attendance, Remarks                                  │
│                                                              │
│      ↓  AUTO-SYNC  ↓                                        │
│                                                              │
│  3️⃣  Score (ពិន្ទុ) - Used by Promotion                      │
│      • Student + Subject + Exam Type                        │
│      • Academic Year                                        │
│      • Linked to Exam (optional)                            │
│                                                              │
└─────────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────────┐
│              STUDENT PROMOTION SYSTEM                        │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Reads Scores to determine if student can promote:          │
│  • Must pass ALL subjects (≥ 50%)                           │
│  • Attendance ≥ 80%                                          │
│  • Follows Cambodia education system rules                  │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔄 Auto-Sync Process / ដំណើរការស្វ័យប្រវត្តិ

### When Exam Result is Created/Updated:

```python
ExamResult Saved
      ↓
Auto-triggered Signal
      ↓
Create/Update Score
      ↓
✅ Ready for Promotion Calculation
```

### Example:

```
📝 Teacher enters exam result:
   Student: សុផារ៉ា តន
   Exam: Math Midterm
   Score: 75/100
   
🔄 System automatically:
   1. Creates Score record
   2. Links to student, subject, exam type
   3. Makes available for promotion

✅ When checking promotion:
   System sees: Math = 75% ✅ Pass
```

---

## 🛠️ Setup & Usage / ការដំឡើងនិងប្រើប្រាស់

### 1. Initial Sync (First Time Setup)

If you already have exam results but no scores:

```bash
# Preview what will be synced (dry run)
python manage.py sync_exam_results_to_scores --dry-run

# Actually sync all results
python manage.py sync_exam_results_to_scores

# Sync specific academic year only
python manage.py sync_exam_results_to_scores --academic-year "2026-2027"
```

### 2. Automatic Sync (Ongoing)

After setup, syncing happens **automatically**:

- ✅ Teacher enters exam result → Score created automatically
- ✅ Teacher updates exam result → Score updated automatically  
- ✅ Teacher deletes exam result → Score deleted automatically

**No manual intervention needed!**

---

## 📝 Workflow Example / ឧទាហរណ៍លំហូរការងារ

### Scenario: Grade 1 Math Midterm

#### Step 1: Create Exam
```
Go to: Exams → Add Exam
- Name: Math Midterm
- Subject: គណិតវិទ្យា (Math)
- Exam Type: កណ្តាលឆមាស (Midterm)
- Classroom: ថ្នាក់ទី១ A
- Date: 2026-12-15
- Max Score: 100
- Passing Score: 50
```

#### Step 2: Enter Results
```
Go to: Exams → View Results → Add Results
- Student: សុផារ៉ា តន → Score: 75/100 ✅
- Student: ដារ៉ា សុខ → Score: 45/100 ❌
- Student: រដ្ឋា ចាន់ → Score: 85/100 ✅
```

**🔄 Auto-Sync Happens:**
```
✅ Score created for សុផារ៉ា: Math/Midterm = 75% (Pass)
✅ Score created for ដារ៉ា: Math/Midterm = 45% (Fail)
✅ Score created for រដ្ឋា: Math/Midterm = 85% (Pass)
```

#### Step 3: Check Promotion
```
Go to: Student Promotion
Select: ថ្នាក់ទី១ A

Results shown:
┌──────────────┬────────┬────┬──────────────┐
│ Student      │ Passed │Fail│ Status       │
├──────────────┼────────┼────┼──────────────┤
│ សុផារ៉ា តន   │   4    │ 0  │ ✅ Can promote│
│ ដារ៉ា សុខ    │   3    │ 1  │ ❌ Cannot    │
│ រដ្ឋា ចាន់   │   4    │ 0  │ ✅ Can promote│
└──────────────┴────────┴────┴──────────────┘
```

---

## 🔍 Verification / ការផ្ទៀងផ្ទាត់

### Check if Sync is Working:

```bash
# Method 1: Check via shell
python manage.py shell

>>> from school.models import ExamResult, Score
>>> exam_results_count = ExamResult.objects.filter(was_present=True).count()
>>> scores_count = Score.objects.filter(exam__isnull=False).count()
>>> print(f"Exam Results: {exam_results_count}")
>>> print(f"Synced Scores: {scores_count}")
```

### Method 2: Check in Admin

1. Go to `/admin/school/examresult/`
2. Count total results
3. Go to `/admin/school/score/`
4. Filter by "Has Exam"
5. Compare numbers

---

## 📋 Data Models / ទម្រង់ទិន្នន័យ

### ExamResult Model:
```python
{
    'exam': Exam (FK),
    'student': Student (FK),
    'score': Decimal,
    'grade_letter': 'A' | 'B' | 'C' | 'D' | 'F',
    'is_passed': Boolean,
    'was_present': Boolean,
    'remarks': Text,
    'recorded_at': DateTime
}
```

### Score Model:
```python
{
    'student': Student (FK),
    'subject': Subject (FK),
    'exam_type': ExamType (FK),
    'exam': Exam (FK) - **Links to ExamResult**,
    'academic_year': AcademicYear (FK),
    'score': Decimal,
    'max_score': Decimal,
    'date_recorded': Date
}
```

### Key Connection:
```python
Score.exam → Exam ← ExamResult.exam
```

---

## 🎓 Promotion Logic / ទំនៀមទម្លាប់ឡើងថ្នាក់

### Requirements (Must meet ALL):

```
✅ Pass ALL subjects (ជាប់គ្រប់មុខវិជ្ជា)
   - Score ≥ 50% in EVERY subject
   - Even 1 failed subject = Cannot promote

✅ Attendance ≥ 80% (វត្តមាន)

✅ Sequential promotion only (រៀងគ្នា)
   - Grade 1 → Grade 2 only
   - Cannot skip grades
```

### Example Scenarios:

#### ✅ Can Promote:
```
Student A:
- Math: 75% ✅
- Khmer: 80% ✅
- Science: 85% ✅
- English: 70% ✅
- Attendance: 90% ✅
→ Result: Can promote to next grade
```

#### ❌ Cannot Promote (Failed 1 subject):
```
Student B:
- Math: 90% ✅
- Khmer: 45% ❌  ← Failed!
- Science: 85% ✅
- English: 78% ✅
- Attendance: 95% ✅
→ Result: Cannot promote (must repeat grade)
```

#### ❌ Cannot Promote (Poor attendance):
```
Student C:
- Math: 80% ✅
- Khmer: 75% ✅
- Science: 85% ✅
- English: 70% ✅
- Attendance: 75% ❌  ← Too low!
→ Result: Cannot promote (poor attendance)
```

---

## 🔧 Troubleshooting / ការដោះស្រាយបញ្ហា

### Problem 1: Exam results exist but promotion shows "no scores"

**Solution:**
```bash
# Run sync command
python manage.py sync_exam_results_to_scores
```

**Check:**
- Are exam results marked as "was_present = True"?
- Are results linked to correct academic year?

---

### Problem 2: Score not updating when exam result changes

**Check:**
1. Signals are loaded:
   ```python
   # In school/apps.py
   def ready(self):
       import school.signals
   ```

2. Check logs:
   ```bash
   tail -f logs/django.log
   ```

**Manual fix:**
```bash
python manage.py sync_exam_results_to_scores --academic-year "2026-2027"
```

---

### Problem 3: Student shows as "cannot promote" but has good scores

**Check:**
1. **All subjects passed?**
   - Must pass EVERY subject (≥ 50%)
   - Check each subject individually

2. **Attendance ≥ 80%?**
   - Check attendance records
   - Must have at least 80% attendance

3. **Scores in correct academic year?**
   - Promotion uses scores from selected academic year
   - Verify year matches

---

## 📊 Reports & Analytics / របាយការណ៍

### Available Data:

1. **Exam Performance:**
   - Individual exam results
   - Class averages
   - Pass rates

2. **Subject Performance:**
   - Aggregated scores by subject
   - Identify weak subjects

3. **Promotion Readiness:**
   - Who can promote
   - Why students cannot promote
   - Required actions

### Useful Queries:

```python
# Students who failed at least one subject
from school.models import Student, Score

students = Student.objects.filter(
    scores__score__lt=50,
    is_active=True
).distinct()

# Subject with most failures
from django.db.models import Count

Subject.objects.annotate(
    fail_count=Count('scores', filter=Q(scores__score__lt=50))
).order_by('-fail_count')
```

---

## 🚀 Best Practices / អនុវត្តន៍ល្អ

### 1. Enter Results Promptly
```
✅ Enter exam results as soon as marked
✅ Scores sync immediately to promotion system
✅ Real-time promotion readiness tracking
```

### 2. Mark Attendance Correctly
```
✅ was_present=True → Creates score
❌ was_present=False → No score created
   (Student was absent, should not count)
```

### 3. Use Consistent Exam Types
```
✅ Midterm, Final, Quiz (standardized)
❌ Avoid: "test1", "exam 2", etc.
```

### 4. Verify Before Promotion
```
✅ Run sync command before promotion period
✅ Check all exams have results entered
✅ Verify attendance is up to date
```

### 5. Backup Before Mass Promotion
```bash
# Backup database
python manage.py dbbackup

# Then promote
```

---

## 📚 Commands Reference / ជំនួយ Command

```bash
# Sync all exam results to scores
python manage.py sync_exam_results_to_scores

# Sync specific year
python manage.py sync_exam_results_to_scores --academic-year "2026-2027"

# Dry run (preview only)
python manage.py sync_exam_results_to_scores --dry-run

# Check what needs syncing
python manage.py sync_exam_results_to_scores --dry-run --academic-year "2026-2027"
```

---

## ✅ Integration Checklist / បញ្ជីពិនិត្យ

Before promotion period:

- [ ] All exams created and scheduled
- [ ] All exam results entered
- [ ] Attendance records up to date
- [ ] Run sync command: `python manage.py sync_exam_results_to_scores`
- [ ] Verify scores in promotion page
- [ ] Check promotion criteria met
- [ ] Backup database
- [ ] Ready to promote! 🎉

---

## 🔗 Related Documentation

- [Student Promotion Guide](STUDENT_PROMOTION_GUIDE.md)
- [Promotion Fixes](PROMOTION_FIXES.md)
- [Classroom Setup](CLASSROOM_FIX_SUMMARY.md)
- [Cambodia Education System](CAMBODIA_PROMOTION_SYSTEM.md)

---

**Last Updated:** 2026-08-05  
**Version:** 1.0  
**Author:** Kiro AI Assistant

**Status:** 🟢 **ACTIVE - Auto-sync enabled**
