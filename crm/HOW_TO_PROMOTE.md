# 🎯 របៀបដាក់សិស្សឡើងថ្នាក់ - How to Promote Students

## 🚀 វិធីងាយស្រួលបំផុត (Easiest Way)

### ជំហាន ១: បើក Command Prompt
```cmd
Win + R
cmd
Enter
```

### ជំហាន ២: ចូលទៅកាន់ Project
```bash
cd d:\Monday-Friday-Year3S1\Monday\python
env\Scripts\activate
cd crm
```

### ជំហាន ៣: ដំណើរការ Script
```bash
python promote_students.py
```

### ជំហាន ៤: ធ្វើតាមមីនុយ

```
STUDENT PROMOTION TOOL
ឧបករណ៍ដាក់សិស្សឡើងថ្នាក់
======================================================================

OPTIONS:
1. List all classrooms         <-- មើលថ្នាក់ទាំងអស់
2. Preview students            <-- មើលសិស្សមុន
3. Promote students (DRY RUN)  <-- សាកល្បង (មិនផ្លាស់ប្តូរ)
4. Promote students (LIVE)     <-- ដាក់ឡើងថ្នាក់ពិតប្រាកដ
5. Exit                        <-- ចេញ

Select option (1-5):
```

---

## 📝 ឧទាហរណ៍ពិតប្រាកដ (Real Example)

### ករណី: ដាក់សិស្សថ្នាក់ទី២ឡើងថ្នាក់ទី៣

#### 1️⃣ មើលថ្នាក់ទាំងអស់
```
Select option: 1

AVAILABLE CLASSROOMS
======================================================================
ID    Grade      Classroom Name                 Year           
----------------------------------------------------------------------
1     Grade 1    ទី១ | 2026                     2026           
2     Grade 2    ទី២ | 2026                     2026           
3     Grade 3    ទី៣ | 2026                     2026           
4     Grade 4    ទី៤ | 2026                     2026           
======================================================================
```

#### 2️⃣ មើលសិស្ស (Preview)
```
Select option: 2
Enter classroom ID: 2

STUDENTS IN: ទី២ | 2026
======================================================================
Total: 5 students
Eligible for promotion: 3 students
======================================================================
```

#### 3️⃣ សាកល្បងដាក់ឡើងថ្នាក់ (Dry Run)
```
Select option: 3
Enter FROM classroom ID: 2
Enter TO classroom ID: 3
Passing score % (default 50): [Enter]
Minimum attendance % (default 80): [Enter]

PROMOTION PROCESS
======================================================================
From: ទី២ | 2026
To:   ទី៣ | 2026
Year: 2026
Mode: DRY RUN (no changes)
======================================================================

No   ID           Name                      Avg%     Att%     Status
----------------------------------------------------------------------
1    STU-0001     សោម សុខា                   75.8%   85.0%   ✅ ELIGIBLE
2    STU-0002     ចាន់ សុភា                  72.5%   72.5%   ❌ Attendance 72.5% < 80%
3    STU-0003     ពេជ្រ ស្រីនាង              88.0%   90.0%   ✅ ELIGIBLE
4    STU-0004     ម៉េង វិទ្យា                45.0%   82.0%   ❌ Average 45.0% < 50%
5    STU-0005     ហ៊ុង រដ្ឋា                  80.5%   95.0%   ✅ ELIGIBLE

======================================================================
SUMMARY
======================================================================
Total students:     5
Eligible:           3
======================================================================
```

#### 4️⃣ ដាក់ឡើងថ្នាក់ពិតប្រាកដ (Live)
```
Select option: 4
Enter FROM classroom ID: 2
Enter TO classroom ID: 3
Passing score % (default 50): [Enter]
Minimum attendance % (default 80): [Enter]

⚠️  WARNING: This will make permanent changes!
Type 'YES' to confirm: YES

[Processing...]

======================================================================
SUMMARY
======================================================================
Total students:     5
Eligible:           3
Successfully promoted: 3
Failed:             2
======================================================================

✅ Promotion completed!
```

---

## ⚡ វិធីរហ័ស (Quick Commands)

### មើលថ្នាក់ទាំងអស់
```bash
python promote_students.py
# ជ្រើសរើស: 1
```

### សាកល្បងឡើងថ្នាក់
```bash
python process_promotion.py --from-classroom 2 --to-classroom 3 --dry-run
```

### ដាក់ឡើងថ្នាក់
```bash
python process_promotion.py --from-classroom 2 --to-classroom 3
```

### ប្តូរលក្ខខណ្ឌ
```bash
python process_promotion.py --from-classroom 2 --to-classroom 3 --passing-score 60 --min-attendance 85
```

---

## ❓ សំណួរញឹកញាប់ (FAQ)

### Q: ត្រូវបង្កើតថ្នាក់ថ្មីឬអត់?
**A:** បាទ/ចាស! មុននឹងឡើងថ្នាក់ ត្រូវមានថ្នាក់ថ្មីជាមុន។

### Q: របៀបបង្កើតថ្នាក់?
**A:** 
```bash
python manage.py create_missing_classrooms --year "2026"
```

### Q: ប្រសិនបើវត្តមានមិនគ្រប់?
**A:** សិស្សនឹងមិនអាចឡើងថ្នាក់។ អាចប្តូរលក្ខខណ្ឌបាន:
```bash
--min-attendance 75  # ប្តូរទៅ 75%
```

### Q: ប្រសិនបើពិន្ទុមិនគ្រប់?
**A:** សិស្សនឹងមិនអាចឡើងថ្នាក់។ អាចប្តូរលក្ខខណ្ឌបាន:
```bash
--passing-score 45  # ប្តូរទៅ 45%
```

### Q: អាចមើលមុនមិនដាក់ឡើងថ្នាក់បានទេ?
**A:** បាទ/ចាស! ប្រើ `--dry-run`:
```bash
python process_promotion.py --from-classroom 2 --to-classroom 3 --dry-run
```

---

## 🆘 ជំនួយ (Help)

ប្រសិនបើមានបញ្ហា:

1. **មើលឯកសារ:**
   - `PROMOTION_TOOL_README.md` (English)
   - `មគ្គុទ្ទេសន៍ប្រព័ន្ធឡើងថ្នាក់.md` (Khmer)

2. **ពិនិត្យ Error:**
   - Read error messages carefully
   - Check classroom IDs
   - Verify student has scores

3. **ប្រើ Dry Run:**
   - Always test with `--dry-run` first
   - Check the preview
   - Then run live

---

**រីករាយក្នុងការប្រើប្រាស់!** 🎉
