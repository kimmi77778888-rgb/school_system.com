# 🚀 Quick Reference - Student Promotion
## មគ្គុទ្ទេសន៍រហ័ស - ការឡើងថ្នាក់សិស្ស

---

## 📋 Basic Steps / ជំហានមូលដ្ឋាន

```
1. ជ្រើសរើសថ្នាក់ → 2. ពិនិត្យលទ្ធផល → 3. ជ្រើសរើសថ្នាក់ថ្មី → 4. ឡើងថ្នាក់
   Select Class    Check Results   Select New Class   Promote
```

---

## ✅ Promotion Criteria / លក្ខខណ្ឌឡើងថ្នាក់

| Requirement | Value | Icon |
|------------|-------|------|
| Average Score | ≥ 50% | 📊 |
| Attendance | ≥ 80% | 📅 |
| Subjects | ≥ 1 | 📚 |

---

## 🎨 Status Colors / ពណ៌ស្ថានភាព

| Status | Color | Meaning |
|--------|-------|---------|
| 🟢 Green | អាចឡើងថ្នាក់ | Can promote |
| 🔴 Red | មិនអាចឡើងថ្នាក់ | Cannot promote |
| 🟡 Yellow | វត្តមានខ្សោយ | Poor attendance |
| ⚫ Gray | គ្មានពិន្ទុ | No scores |

---

## 🆘 Common Issues / បញ្ហាទូទៅ

### ❌ Problem: គ្មានថ្នាក់សម្រាប់ឡើង

**Solution 1: Create Manually**
```
1. ទៅកាន់ "ថ្នាក់រៀន" (Classrooms)
2. ចុច "+ បន្ថែមថ្នាក់រៀន"
3. ជ្រើសរើសថ្នាក់និងឆ្នាំសិក្សា
4. រក្សាទុក
```

**Solution 2: Use Command**
```bash
python manage.py create_missing_classrooms --year "2026-2027"
```

---

### ❌ Problem: សិស្សទាំងអស់បង្ហាញមិនអាចឡើង

**Checks:**
- ✓ ពិន្ទុមធ្យម ≥ 50%?
- ✓ វត្តមាន ≥ 80%?
- ✓ មានពិន្ទុប្រឡង?

---

### ⚠️ Problem: ថ្នាក់គ្មានកាលវិភាគ

**Solution:**
```
1. ទៅកាន់ "តារាងម៉ោង" (Timetable)
2. ចុច "+ បន្ថែម"
3. បង្កើតកាលវិភាគសម្រាប់ថ្នាក់ថ្មី
```

**Note:** អាចបន្តឡើងថ្នាក់ ប៉ុន្តែសិស្សមិនឃើញកាលវិភាគ

---

## 🎯 Grade Transitions / ការផ្ទេរកម្រិត

```
Primary (បឋមសិក្សា)
Grade 1 → 2 → 3 → 4 → 5 → 6
                           ↓
Lower Secondary (បឋមភូមិ)      Level Transition
Grade 7 → 8 → 9
           ↓
Upper Secondary (មធ្យមភូមិ)    Level Transition
Grade 10 → 11 → 12
              ↓
           Graduation 🎓
```

---

## 🔍 Validation Rules / ច្បាប់ត្រួតពិនិត្យ

| Rule | Description | Example |
|------|-------------|---------|
| ✅ Sequential | រៀងគ្នា | 1→2→3 |
| ❌ Skip Grade | រំលងថ្នាក់ | 1→3 ✗ |
| ✅ Level Change | ផ្លាស់កម្រិត | 6→7, 9→10 |
| ❌ Beyond 12 | លើសថ្នាក់ 12 | 12→13 ✗ |

---

## 📊 Statistics Meaning / អត្ថន័យស្ថិតិ

```
╔═══════════╗  ╔═══════════╗  ╔═══════════╗
║ សិស្សសរុប  ║  ║ អាចឡើង    ║  ║ មិនអាច    ║
║    25     ║  ║    20     ║  ║     5     ║
║   នាក់     ║  ║   នាក់     ║  ║    នាក់    ║
╚═══════════╝  ╚═══════════╝  ╚═══════════╝
Total          Eligible       Not Eligible
```

---

## 💡 Tips / ជំនួយ

### ✅ DO / ធ្វើ
- ✓ ពិនិត្យពិន្ទុមុនពេលឡើងថ្នាក់
- ✓ បង្កើតថ្នាក់មុនពេលដំណើរការ
- ✓ បង្កើតកាលវិភាគសម្រាប់ថ្នាក់ថ្មី
- ✓ រក្សាទុក backup data

### ❌ DON'T / កុំធ្វើ
- ✗ រំលងថ្នាក់
- ✗ ឡើងថ្នាក់ដោយគ្មានពិន្ទុ
- ✗ បំភ្លេចពិនិត្យវត្តមាន
- ✗ ឡើងថ្នាក់មុនពេលបញ្ចប់ឆ្នាំ

---

## 🔗 Quick Links / តំណរហ័ស

| Page | Link | Icon |
|------|------|------|
| Students | `/school/students/` | 👥 |
| Classrooms | `/school/classrooms/` | 🏫 |
| Promotion | `/school/students/promote/` | 🎓 |
| Timetable | `/school/timetable/` | 📅 |
| Academic Years | `/school/academic-years/` | 📆 |

---

## ⌨️ Keyboard Shortcuts / គ្រាប់ចុចរហ័ស

| Action | Shortcut | Note |
|--------|----------|------|
| Select All | `Ctrl + A` | ជ្រើសរើសសិស្សទាំងអស់ |
| Submit | `Ctrl + Enter` | ឡើងថ្នាក់ |
| Cancel | `Esc` | បោះបង់ |

---

## 📞 Need Help? / ត្រូវការជំនួយ?

1. **Documentation**
   - [Full Guide](STUDENT_PROMOTION_GUIDE.md)
   - [Technical Fixes](PROMOTION_FIXES.md)
   - [Visual Guide](VISUAL_IMPROVEMENTS.md)

2. **Check Logs**
   ```bash
   tail -f logs/django.log
   ```

3. **Command Help**
   ```bash
   python manage.py create_missing_classrooms --help
   ```

---

## 🎯 Checklist Before Promotion / បញ្ជីពិនិត្យមុនឡើងថ្នាក់

```
☐ All exams completed
☐ All scores entered
☐ Attendance recorded
☐ Next year classrooms created
☐ Timetables prepared
☐ Academic year created
☐ Backup database
☐ Notify parents (optional)
```

---

## 📈 Success Rate / អត្រាជោគជ័យ

```
បញ្ចូលពិន្ទុពេញលេញ     →  95% ជោគជ័យ
Full score entry          95% success

គ្មានពិន្ទុខ្លះ          →  មិនអាចឡើង
Missing some scores       Cannot promote

វត្តមានលើស 80%         →  អាចឡើងបាន
Attendance over 80%      Can promote

វត្តមានក្រោម 80%        →  ត្រូវពិចារណា
Attendance under 80%     Need review
```

---

## 🎨 Interface Guide / មគ្គុទ្ទេសន៍ Interface

```
┌────────────────────────────────────────┐
│  📊 Summary (Purple gradient)          │
│  ┌─────┐ ┌─────┐ ┌─────┐              │
│  │ All │ │ Yes │ │ No  │              │
│  └─────┘ └─────┘ └─────┘              │
└────────────────────────────────────────┘
       ↓
┌────────────────────────────────────────┐
│  👥 Students (Blue header)             │
│  ┌──────────────────────────────────┐  │
│  │ ☑ Select next classroom          │  │
│  └──────────────────────────────────┘  │
│  ┌──────────────────────────────────┐  │
│  │ 🟢 Student 1 (Can promote)       │  │
│  │ 🔴 Student 2 (Cannot promote)    │  │
│  └──────────────────────────────────┘  │
│  [ដាក់ឡើងថ្នាក់]                     │
└────────────────────────────────────────┘
```

---

## 🔔 Notifications / ការជូនដំណឹង

After successful promotion:
- ✅ Students moved to new classroom
- ✅ History record created
- ✅ Previous classroom saved
- ✅ Status updated to "ACTIVE"
- ✅ Notes added to student record

---

## 💾 Data Backup / ការរក្សាទុកទិន្នន័យ

**Before bulk promotion:**
```bash
# Backup database
python manage.py dumpdata > backup_$(date +%Y%m%d).json

# Or use Django's backup
python manage.py dbbackup
```

**After promotion:**
```bash
# Verify changes
python manage.py shell
>>> from school.models import Student
>>> Student.objects.filter(status='ACTIVE').count()
```

---

## 🎓 Cambodia System Rules / ច្បាប់ប្រព័ន្ធកម្ពុជា

| Level | Grades | Years | Special |
|-------|--------|-------|---------|
| បឋមសិក្សា | 1-6 | 6 years | → បឋមភូមិ |
| បឋមភូមិ | 7-9 | 3 years | → មធ្យមភូមិ |
| មធ្យមភូមិ | 10-12 | 3 years | → បញ្ចប់ការសិក្សា |

---

## ⚡ Quick Commands / Command រហ័ស

```bash
# Create missing classrooms
python manage.py create_missing_classrooms --year "2026-2027"

# Check promotion status
python manage.py shell
>>> from school.models import StudentHistory
>>> StudentHistory.objects.filter(status='PROMOTED').count()

# View recent promotions
python manage.py shell
>>> from school.models import Student
>>> Student.objects.filter(promotion_date__isnull=False).order_by('-promotion_date')[:10]
```

---

**📌 Bookmark this page for quick reference!**

**សូមរក្សាទុកទំព័រនេះដើម្បីមើលរហ័ស!**

---

**Last Updated:** 2026-08-05  
**Version:** 2.0  
**Author:** Kiro AI Assistant
