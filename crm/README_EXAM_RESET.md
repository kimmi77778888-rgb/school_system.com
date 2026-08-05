# 🔄 Exam & Promotion System Reset

## Overview | ទិដ្ឋភាពទូទៅ

This package contains scripts and documentation to **completely reset** and **rebuild** your exam, exam result, and student promotion system.

---

## 📦 Files Included

### 1. **reset_exam_promotion_system.py** 
🗑️ **Main Reset Script**
- Deletes all Exam, ExamResult, Score, and StudentHistory records
- Resets student promotion fields
- Preserves core data (students, classrooms, subjects, academic years)
- Interactive with confirmation prompts
- Shows statistics before and after

**Usage:**
```bash
python reset_exam_promotion_system.py
```

---

### 2. **NEW_EXAM_PROMOTION_GUIDE.md** 
📚 **Complete Guide**
- Step-by-step instructions for rebuilding the system
- API endpoints and examples
- Python scripts for automation
- Troubleshooting tips
- Best practices
- Complete checklist

**Read this first!**

---

### 3. **quick_setup_exams.py** 
⚡ **Quick Exam Creation**
- Interactive wizard for creating exams
- Bulk create exams for multiple classrooms
- Automatically creates exams for all subjects
- Saves time when setting up new academic year

**Usage:**
```bash
python quick_setup_exams.py
```

**Features:**
- ✅ Interactive wizard (recommended)
- ✅ Single classroom setup
- ✅ Multiple classrooms at once
- ✅ All subjects included automatically

---

### 4. **bulk_import_exam_results.py** 
📥 **Import from CSV**
- Import exam results from Excel/CSV files
- Import scores in bulk
- Create sample CSV templates
- Update or skip existing records
- Error reporting

**Usage:**
```bash
python bulk_import_exam_results.py
```

**Supports:**
- ✅ ExamResult model (exam-specific results)
- ✅ Score model (general student scores)
- ✅ CSV templates provided
- ✅ Validation and error handling

---

## 🚀 Quick Start

### Step 1: Backup Your Database
```bash
python manage.py dumpdata > backup_$(date +%Y%m%d).json
```

### Step 2: Run the Reset Script
```bash
python reset_exam_promotion_system.py
```
- Choose option 1 to reset
- Type `DELETE` to confirm
- Wait for completion

### Step 3: Create New Exams
```bash
python quick_setup_exams.py
```
- Choose option 1 (Interactive Wizard)
- Select exam type (e.g., Midterm)
- Select classrooms
- Set exam date and scores
- Confirm and create

### Step 4: Import Exam Results
```bash
python bulk_import_exam_results.py
```
- Choose option 1 to create CSV template
- Fill in the CSV with student results
- Choose option 3 to import
- Verify results in web interface

### Step 5: Check Promotion Eligibility
```bash
# Using API or Django shell
POST /api/students/check_promotion_eligibility/
{
  "classroom_id": 1,
  "passing_percentage": 50.0
}
```

### Step 6: Promote Students
```bash
POST /api/students/bulk_promote/
{
  "student_ids": [1, 2, 3, 4, 5],
  "next_classroom_id": 6,
  "passing_percentage": 50.0
}
```

---

## 📊 What Gets Deleted

### ❌ Deleted:
- All Exam records
- All ExamResult records
- All Score records
- All StudentHistory records
- Student promotion dates and notes

### ✅ Preserved:
- ExamType (exam types)
- Students (with promotion fields reset)
- Classrooms
- Subjects
- Academic Years
- Teachers
- Attendance records
- User accounts

---

## 🔐 Safety Features

1. **Confirmation Required**: Must type 'DELETE' to proceed
2. **Transaction Safety**: All changes in a single database transaction
3. **Statistics Display**: Shows before/after counts
4. **Rollback on Error**: Automatic rollback if anything fails
5. **Backup Recommended**: Always backup before running

---

## 📖 Documentation

### Full Guide
Read `NEW_EXAM_PROMOTION_GUIDE.md` for:
- Complete API documentation
- Python script examples
- Troubleshooting guide
- Best practices
- Promotion rules and validation

### Quick Reference

**Promotion Rules:**
- ✅ Average score ≥ 50%
- ✅ Attendance rate ≥ 80%
- ✅ Must have at least one score
- ✅ Can only promote to next grade (+1)
- ✅ Must respect level transitions:
  - Grade 6 → Grade 7 (Primary → Lower Secondary)
  - Grade 9 → Grade 10 (Lower Secondary → Upper Secondary)
  - Grade 12 → Graduation

---

## 🛠️ API Endpoints

### Exams
- `GET /api/exams/` - List all exams
- `POST /api/exams/` - Create exam
- `GET /api/exams/{id}/` - Get exam details
- `PUT /api/exams/{id}/` - Update exam
- `DELETE /api/exams/{id}/` - Delete exam

### Exam Results
- `POST /api/exam-results/` - Create result
- `GET /api/exam-results/` - List results

### Scores
- `POST /api/scores/` - Create score
- `GET /api/scores/` - List scores

### Promotion
- `POST /api/students/check_promotion_eligibility/` - Check eligibility
- `POST /api/students/bulk_promote/` - Promote students

---

## ⚠️ Common Issues & Solutions

### Issue 1: "មិនអាចរំលងថ្នាក់បានទេ" (Cannot skip grades)
**Solution:** Only promote to next grade (Grade 7 → Grade 8, not 7 → 9)

### Issue 2: "មិនមានពិន្ទុ" (No scores)
**Solution:** Add exam results or scores first

### Issue 3: "វត្តមាន < 80%" (Low attendance)
**Solution:** Need at least 80% attendance to promote

### Issue 4: Foreign key constraint errors
**Solution:** Ensure classroom has academic_year assigned

---

## 📞 Support & Help

### Check System Status
```bash
python reset_exam_promotion_system.py
# Choose option 2 (Show statistics only)
```

### Verify Data
```bash
# Django shell
python manage.py shell

from school.models import Exam, ExamResult, Score, StudentHistory

print(f"Exams: {Exam.objects.count()}")
print(f"ExamResults: {ExamResult.objects.count()}")
print(f"Scores: {Score.objects.count()}")
print(f"StudentHistory: {StudentHistory.objects.count()}")
```

---

## ✅ Checklist

Before starting:
- [ ] Backup database
- [ ] Inform teachers and staff
- [ ] Plan exam schedule
- [ ] Prepare student data

After reset:
- [ ] Verify core data intact
- [ ] Create exam types (if needed)
- [ ] Create exams for all classrooms
- [ ] Record exam results
- [ ] Verify results in web interface
- [ ] Check promotion eligibility
- [ ] Promote eligible students
- [ ] Generate reports
- [ ] Test with production data

---

## 🎯 Recommended Workflow

1. **Test Environment First**: Run on test database before production
2. **One Classroom at a Time**: Test with one classroom first
3. **Verify Each Step**: Check data after each major step
4. **Backup Regularly**: Backup after each successful stage
5. **Monitor Logs**: Check for errors and warnings
6. **User Training**: Train staff on new system

---

## 📈 Performance Tips

- Use bulk operations when possible
- Import large datasets via CSV
- Create indexes if slow (Django handles this)
- Monitor database size
- Archive old data if needed

---

## 🔄 Updates & Versions

**Version:** 1.0  
**Date:** 2026-08-06  
**Compatibility:** Django 3.2+

---

## 📝 License & Credits

Created for the CRM School Management System.  
ប្រព័ន្ធគ្រប់គ្រងសាលារៀន

---

## 🙏 Support

For questions or issues:
1. Check `NEW_EXAM_PROMOTION_GUIDE.md` first
2. Review error messages carefully
3. Test on small dataset first
4. Contact system administrator

---

**Good luck with your new exam system! 🎓**
