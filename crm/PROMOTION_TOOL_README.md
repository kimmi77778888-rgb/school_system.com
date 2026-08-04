# 🎓 Student Promotion Tool - ឧបករណ៍ដាក់សិស្សឡើងថ្នាក់

## Quick Start - ចាប់ផ្តើមរហ័ស

### Method 1: Interactive Tool (Easiest) ✨

```bash
cd d:\Monday-Friday-Year3S1\Monday\python
env\Scripts\activate
cd crm
python promote_students.py
```

**What it does:**
- Shows all classrooms
- Preview students
- Test promotion (dry run)
- Execute promotion (live)

---

### Method 2: Command Line (Advanced) 🚀

```bash
cd d:\Monday-Friday-Year3S1\Monday\python
env\Scripts\activate
cd crm

# DRY RUN (preview only)
python process_promotion.py --from-classroom 1 --to-classroom 2 --dry-run

# LIVE (make changes)
python process_promotion.py --from-classroom 1 --to-classroom 2

# Custom criteria
python process_promotion.py --from-classroom 1 --to-classroom 2 --passing-score 60 --min-attendance 85
```

---

## Features

### ✅ Automatic Validation
- Checks if student meets criteria (score ≥ 50%, attendance ≥ 80%)
- Validates grade progression (no skipping grades)
- Validates level transitions (Grade 6→7, Grade 9→10)
- Prevents invalid promotions

### 📊 Clear Reports
- Shows all students with their scores and attendance
- Marks eligible vs ineligible students
- Summary of results
- Error messages for failed promotions

### 🔒 Safe Processing
- DRY RUN mode to preview before making changes
- Confirmation required for live mode
- Creates history records
- Preserves student data

---

## Examples

### Example 1: Promote Grade 2 to Grade 3

```bash
# Step 1: Find classroom IDs
python promote_students.py
# Select option 1 to list classrooms

# Step 2: Preview
python process_promotion.py --from-classroom 5 --to-classroom 8 --dry-run

# Step 3: Execute
python process_promotion.py --from-classroom 5 --to-classroom 8
```

### Example 2: Interactive Mode

```bash
python promote_students.py

# Choose:
# 1 - See all classrooms
# 2 - Preview specific classroom
# 3 - Test promotion (no changes)
# 4 - Execute promotion
```

---

## Criteria

### Default Requirements:
- **Score:** Average ≥ 50% across all subjects
- **Attendance:** ≥ 80% attendance rate
- **Subjects:** Must have at least 1 subject with scores

### Customizable:
```bash
--passing-score 60    # Change to 60%
--min-attendance 85   # Change to 85%
```

---

## What Happens During Promotion?

1. **Validation** ✅
   - Check student eligibility
   - Validate grade progression
   - Check level transitions

2. **Create History** 📚
   - Save academic year record
   - Store scores and attendance
   - Mark as "PROMOTED"

3. **Update Student** 🔄
   - Move to new classroom
   - Save previous classroom
   - Set promotion date
   - Add note

---

## Troubleshooting

### Error: "Cannot skip grades"
**Problem:** Trying to promote from Grade 1 to Grade 3
**Solution:** Create Grade 2 classroom first, then promote Grade 1→2, then 2→3

### Error: "Must transition to Lower Secondary"
**Problem:** Promoting Grade 6 to wrong level
**Solution:** Ensure Grade 7 classroom has level "lower_secondary"

### Error: "No scores available"
**Problem:** Student has no exam scores
**Solution:** Enter scores first, or exclude student from promotion

---

## Need Help?

Check documentation:
- `មគ្គុទ្ទេសន៍ប្រព័ន្ធឡើងថ្នាក់.md` (Khmer guide)
- `CAMBODIA_PROMOTION_SYSTEM.md` (Detailed system docs)

---

**Created:** 2026-08-04  
**Version:** 1.0
