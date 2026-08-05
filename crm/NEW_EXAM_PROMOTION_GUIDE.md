# 📚 New Exam & Promotion System Guide
## ណែនាំប្រព័ន្ធប្រឡងនិងការឡើងថ្នាក់ថ្មី

---

## 🎯 Overview

This guide will help you rebuild the exam and promotion system from scratch after running the reset script.

### System Components:
1. **Exam Types** (ប្រភេទប្រឡង) - Kept from old system
2. **Exams** (ប្រឡង) - Need to create new
3. **Exam Results** (លទ្ធផលប្រឡង) - Need to record new
4. **Scores** (ពិន្ទុ) - Need to add new
5. **Student Promotion** (ការឡើងថ្នាក់) - Based on new data

---

## 📋 Step-by-Step Process

### Step 1: Run the Reset Script

```bash
# Navigate to project directory
cd d:\Monday-Friday-Year3S1\Monday\python\crm

# Activate virtual environment (if using one)
# On Windows:
env\Scripts\activate
# On Linux/Mac:
# source env/bin/activate

# Run the reset script
python reset_exam_promotion_system.py
```

**What this does:**
- ❌ Deletes all ExamResult records
- ❌ Deletes all Exam records  
- ❌ Deletes all Score records
- ❌ Deletes all StudentHistory records
- 🔄 Resets student promotion fields
- ✅ Keeps ExamType, Students, Classrooms, Subjects, Academic Years

---

### Step 2: Create Exam Types (if needed)

**Option A: Web Interface**
1. Navigate to `/exams/types/`
2. Click "Add Exam Type"
3. Fill in:
   - Name (e.g., "Midterm Exam", "Final Exam")
   - Code (e.g., "MID", "FINAL")
   - Weight percentage (e.g., 30% for midterm, 70% for final)

**Option B: API**
```bash
POST /api/exam-types/
{
  "name": "Midterm Exam",
  "code": "MID",
  "weight_percentage": 30.00,
  "is_active": true
}
```

**Common Exam Types:**
- Midterm (កណ្តាលឆមាស) - 30%
- Final (ចុងឆមាស) - 70%
- Quiz (តេស្តតូច) - 10%
- Assignment (កិច្ចការផ្ទះ) - 20%

---

### Step 3: Create Exams

**Option A: Web Interface**
1. Navigate to `/exams/`
2. Click "Add Exam"
3. Fill in:
   - Name (e.g., "Math Midterm 2026")
   - Exam Type (select from dropdown)
   - Subject (select subject)
   - Classroom (select classroom)
   - Academic Year (select year)
   - Date (exam date)
   - Max Score (e.g., 100)
   - Passing Score (e.g., 50)

**Option B: API**
```bash
POST /api/exams/
{
  "name": "Math Midterm 2026",
  "exam_type": 1,
  "subject": 1,
  "classroom": 1,
  "academic_year": 1,
  "date": "2026-08-15",
  "exam_time": "08:00:00",
  "duration_minutes": 120,
  "max_score": 100.00,
  "passing_score": 50.00,
  "status": "scheduled",
  "description": "Midterm examination for Mathematics"
}
```

**Example: Create exams for all subjects in a classroom**
```python
# Python script example
import requests

API_URL = "http://localhost:8000/api/exams/"
TOKEN = "your-auth-token"

headers = {
    "Authorization": f"Token {TOKEN}",
    "Content-Type": "application/json"
}

subjects = [1, 2, 3, 4, 5]  # Subject IDs
classroom_id = 1
academic_year_id = 1

for subject_id in subjects:
    data = {
        "name": f"Midterm Exam - Subject {subject_id}",
        "exam_type": 1,  # Midterm
        "subject": subject_id,
        "classroom": classroom_id,
        "academic_year": academic_year_id,
        "date": "2026-08-15",
        "max_score": 100.00,
        "passing_score": 50.00,
        "status": "scheduled"
    }
    response = requests.post(API_URL, json=data, headers=headers)
    print(f"Created exam for subject {subject_id}: {response.status_code}")
```

---

### Step 4: Record Exam Results

**Option A: Web Interface**
1. Navigate to exam detail page
2. Click "Record Results"
3. Enter scores for each student

**Option B: API - Individual Result**
```bash
POST /api/exam-results/
{
  "exam": 1,
  "student": 1,
  "score": 85.00,
  "was_present": true,
  "remarks": "Good performance"
}
```

**Option C: API - Bulk Results**
```python
# Python script for bulk exam results
import requests

API_URL = "http://localhost:8000/api/exam-results/"
TOKEN = "your-auth-token"

headers = {
    "Authorization": f"Token {TOKEN}",
    "Content-Type": "application/json"
}

# Example: Record results for all students
exam_id = 1
results = [
    {"student": 1, "score": 85.00, "was_present": True},
    {"student": 2, "score": 92.00, "was_present": True},
    {"student": 3, "score": 45.00, "was_present": True},
    {"student": 4, "score": 0.00, "was_present": False, "absent_reason": "Sick"},
]

for result in results:
    data = {
        "exam": exam_id,
        "student": result["student"],
        "score": result["score"],
        "was_present": result.get("was_present", True),
        "absent_reason": result.get("absent_reason", "")
    }
    response = requests.post(API_URL, json=data, headers=headers)
    print(f"Student {result['student']}: {response.status_code}")
```

---

### Step 5: Add Student Scores (Alternative Method)

If you want to use the Score model instead of ExamResult:

```bash
POST /api/scores/
{
  "student": 1,
  "subject": 1,
  "exam_type": 1,
  "exam": 1,
  "academic_year": 1,
  "score": 85.00,
  "max_score": 100.00,
  "remarks": "Excellent work"
}
```

**Bulk Score Import Script:**
```python
# bulk_import_scores.py
import os
import django
import csv

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crm.settings')
django.setup()

from school.models import Score, Student, Subject, ExamType, AcademicYear

def import_scores_from_csv(csv_file):
    """Import scores from CSV file
    
    CSV format:
    student_id,subject_id,exam_type_id,score,max_score
    STU-0001,1,1,85,100
    STU-0002,1,1,92,100
    """
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                student = Student.objects.get(student_id=row['student_id'])
                subject = Subject.objects.get(id=row['subject_id'])
                exam_type = ExamType.objects.get(id=row['exam_type_id'])
                academic_year = AcademicYear.objects.first()  # or specify
                
                Score.objects.create(
                    student=student,
                    subject=subject,
                    exam_type=exam_type,
                    academic_year=academic_year,
                    score=float(row['score']),
                    max_score=float(row['max_score'])
                )
                print(f"✅ Added score for {student}")
            except Exception as e:
                print(f"❌ Error for {row['student_id']}: {e}")

if __name__ == '__main__':
    import_scores_from_csv('scores.csv')
```

---

### Step 6: Check Promotion Eligibility

Before promoting students, check who is eligible:

**API Request:**
```bash
POST /api/students/check_promotion_eligibility/
{
  "classroom_id": 1,
  "academic_year_id": 1,
  "passing_percentage": 50.0
}
```

**Response:**
```json
{
  "classroom": "Grade 7A - 2025-2026",
  "classroom_id": 1,
  "total_students": 30,
  "eligible_count": 25,
  "students": [
    {
      "student_id": 1,
      "student_name": "STU-0001 - Sok Sophea",
      "student_code": "STU-0001",
      "current_classroom": "Grade 7A - 2025-2026",
      "current_grade_number": 7,
      "total_subjects": 8,
      "passed_subjects": 8,
      "failed_subjects": 0,
      "avg_percentage": 85.5,
      "attendance_rate": 95.2,
      "total_days": 180,
      "present_days": 171,
      "can_promote": true,
      "promotion_status": "✅ អាចឡើងថ្នាក់",
      "reasons": []
    },
    {
      "student_id": 2,
      "student_name": "STU-0002 - Chan Dara",
      "student_code": "STU-0002",
      "current_classroom": "Grade 7A - 2025-2026",
      "current_grade_number": 7,
      "total_subjects": 8,
      "passed_subjects": 5,
      "failed_subjects": 3,
      "avg_percentage": 45.0,
      "attendance_rate": 75.0,
      "total_days": 180,
      "present_days": 135,
      "can_promote": false,
      "promotion_status": "❌ មិនអាចឡើងថ្នាក់",
      "reasons": [
        "ពិន្ទុមធ្យម 45.0% < 50.0%",
        "វត្តមាន 75.0% < 80%"
      ]
    }
  ]
}
```

**Python Script to Check All Classrooms:**
```python
# check_all_promotions.py
import requests

API_URL = "http://localhost:8000/api/students/check_promotion_eligibility/"
TOKEN = "your-auth-token"

headers = {
    "Authorization": f"Token {TOKEN}",
    "Content-Type": "application/json"
}

classrooms = [1, 2, 3, 4, 5]  # Classroom IDs to check

for classroom_id in classrooms:
    data = {
        "classroom_id": classroom_id,
        "passing_percentage": 50.0
    }
    response = requests.post(API_URL, json=data, headers=headers)
    
    if response.status_code == 200:
        result = response.json()
        print(f"\n📊 {result['classroom']}")
        print(f"   Total: {result['total_students']}")
        print(f"   Eligible: {result['eligible_count']}")
        print(f"   Not Eligible: {result['total_students'] - result['eligible_count']}")
    else:
        print(f"❌ Error checking classroom {classroom_id}")
```

---

### Step 7: Promote Students

**Promotion Rules:**
1. ✅ Average score ≥ 50%
2. ✅ Attendance rate ≥ 80%
3. ✅ Must have scores in at least 1 subject
4. ✅ Can only promote to next grade (+1)
5. ✅ Must respect education level transitions:
   - Grade 6 → Grade 7 (Primary → Lower Secondary)
   - Grade 9 → Grade 10 (Lower Secondary → Upper Secondary)
   - Grade 12 → Graduation (no further promotion)

**API Request:**
```bash
POST /api/students/bulk_promote/
{
  "student_ids": [1, 2, 3, 4, 5],
  "next_classroom_id": 6,
  "academic_year_id": 1,
  "passing_percentage": 50.0
}
```

**Response:**
```json
{
  "success": true,
  "message": "Promoted 4 out of 5 students successfully",
  "promoted_count": 4,
  "failed_count": 1,
  "promoted_students": [
    {
      "student_id": 1,
      "student_name": "STU-0001 - Sok Sophea",
      "old_classroom": "Grade 7A - 2025-2026",
      "new_classroom": "Grade 8A - 2026-2027",
      "promotion_date": "2026-08-06"
    }
  ],
  "failed_promotions": [
    {
      "student_id": 5,
      "student_name": "STU-0005 - Pen Srey",
      "reason": "ពិន្ទុមធ្យម 45.0% < 50.0%"
    }
  ]
}
```

**Python Script to Promote All Eligible Students:**
```python
# promote_eligible_students.py
import requests

CHECK_API = "http://localhost:8000/api/students/check_promotion_eligibility/"
PROMOTE_API = "http://localhost:8000/api/students/bulk_promote/"
TOKEN = "your-auth-token"

headers = {
    "Authorization": f"Token {TOKEN}",
    "Content-Type": "application/json"
}

# Mapping of current classroom to next classroom
promotion_map = {
    1: 6,   # Grade 7A → Grade 8A
    2: 7,   # Grade 7B → Grade 8B
    3: 8,   # Grade 8A → Grade 9A
    # Add more mappings...
}

for current_classroom_id, next_classroom_id in promotion_map.items():
    # Check eligibility
    check_data = {
        "classroom_id": current_classroom_id,
        "passing_percentage": 50.0
    }
    check_response = requests.post(CHECK_API, json=check_data, headers=headers)
    
    if check_response.status_code == 200:
        result = check_response.json()
        eligible_ids = [s['student_id'] for s in result['students'] if s['can_promote']]
        
        if eligible_ids:
            # Promote eligible students
            promote_data = {
                "student_ids": eligible_ids,
                "next_classroom_id": next_classroom_id,
                "passing_percentage": 50.0
            }
            promote_response = requests.post(PROMOTE_API, json=promote_data, headers=headers)
            
            if promote_response.status_code == 200:
                promo_result = promote_response.json()
                print(f"✅ Classroom {current_classroom_id}: Promoted {promo_result['promoted_count']}")
            else:
                print(f"❌ Error promoting classroom {current_classroom_id}")
        else:
            print(f"⚠️  Classroom {current_classroom_id}: No eligible students")
```

---

## 🔧 Troubleshooting

### Issue 1: "មិនអាចរំលងថ្នាក់បានទេ" (Cannot skip grades)
**Solution:** You can only promote students to the immediate next grade (e.g., Grade 7 → Grade 8, not Grade 7 → Grade 9).

### Issue 2: "មិនមានពិន្ទុ" (No scores)
**Solution:** Students need at least one score record before they can be promoted. Add exam results or scores first.

### Issue 3: "វត្តមាន < 80%" (Attendance too low)
**Solution:** Student attendance must be at least 80%. Either:
- Add more attendance records
- Lower the attendance requirement (not recommended)
- Student repeats the grade

### Issue 4: Level transition errors
**Solution:** Respect the education system transitions:
- Primary (Grade 1-6) → Lower Secondary (Grade 7-9)
- Lower Secondary (Grade 7-9) → Upper Secondary (Grade 10-12)

---

## 📊 Monitoring & Reports

### Check System Status
```python
# status_check.py
python reset_exam_promotion_system.py
# Choose option 2 (Show statistics only)
```

### Generate Promotion Report
```python
# promotion_report.py
import os
import django
import csv

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crm.settings')
django.setup()

from school.models import StudentHistory, AcademicYear

def generate_promotion_report(academic_year_id):
    year = AcademicYear.objects.get(id=academic_year_id)
    histories = StudentHistory.objects.filter(
        academic_year=year,
        status='PROMOTED'
    ).select_related('student', 'classroom')
    
    with open(f'promotion_report_{year.year}.csv', 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            'Student ID', 'Student Name', 'Grade', 'Average Score',
            'Passed Subjects', 'Failed Subjects', 'Attendance Rate',
            'Promoted To', 'Promotion Date'
        ])
        
        for hist in histories:
            writer.writerow([
                hist.student.student_id,
                str(hist.student),
                hist.grade_name,
                hist.average_score,
                hist.passed_subjects,
                hist.failed_subjects,
                hist.attendance_percentage(),
                hist.promoted_to,
                hist.end_date
            ])
    
    print(f"✅ Report generated: promotion_report_{year.year}.csv")

if __name__ == '__main__':
    generate_promotion_report(1)  # Change to your academic year ID
```

---

## 🎓 Best Practices

1. **Regular Backups**: Before running reset script, backup your database
   ```bash
   python manage.py dumpdata > backup.json
   ```

2. **Gradual Rollout**: Test the new system with one classroom first

3. **Data Validation**: Always check eligibility before promoting

4. **Communication**: Inform teachers and staff about the new system

5. **Documentation**: Keep records of promotion dates and reasons

6. **Monitoring**: Regularly check system statistics

---

## 📞 Support

If you encounter issues:
1. Check the error logs
2. Review this guide
3. Test with a single student/classroom first
4. Contact system administrator

---

## ✅ Checklist

- [ ] Backup database
- [ ] Run reset script
- [ ] Verify core data preserved (students, classrooms, etc.)
- [ ] Create/verify exam types
- [ ] Create new exams for all subjects
- [ ] Record exam results
- [ ] Check promotion eligibility
- [ ] Promote eligible students
- [ ] Verify StudentHistory records created
- [ ] Generate reports
- [ ] Test with production data

---

**Last Updated:** 2026-08-06
**Version:** 1.0
