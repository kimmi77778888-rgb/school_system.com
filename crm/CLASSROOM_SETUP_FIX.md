# ការដោះស្រាយបញ្ហា "មិនឃើញថ្នាក់ត្រូវឡើង"
# Fix for "Cannot see next classroom" issue

## 🔴 បញ្ហា (Problem)

នៅពេលដាក់សិស្សឡើងថ្នាក់ អ្នកមិនឃើញ dropdown "ថ្នាក់ថ្មី" (Next Classroom) ដើម្បីជ្រើសរើស។

When promoting students, you cannot see the "Next Classroom" dropdown to select where students should be promoted to.

## 🔍 មូលហេតុ (Root Cause)

ប្រព័ន្ធត្រូវការថ្នាក់ (Classroom) សម្រាប់គ្រប់ថ្នាក់រៀន (Grade) ដែលអ្នកចង់ដាក់សិស្សឡើង។ ប៉ុន្តែមានតែថ្នាក់រៀនខ្លះប៉ុណ្ណោះដែលបានបង្កើត។

The system requires classrooms to exist for all grade levels you want to promote students to. However, only some grades had classrooms created.

**Before:**
- Grade 1 (ទី១): ✅ Has classroom
- Grade 2 (ទី២): ✅ Has classroom
- Grade 3 (ទី៣): ❌ NO classroom
- Grade 4 (ទី៤): ❌ NO classroom
- Grade 5 (ទី៥): ❌ NO classroom
- Grade 6 (ទី៦): ❌ NO classroom

ដូច្នេះ នៅពេលដាក់សិស្សពីថ្នាក់ទី២ឡើងថ្នាក់ទី៣ ប្រព័ន្ធមិនអាចរកថ្នាក់ទី៣បានទេ។

Therefore, when promoting students from Grade 2 to Grade 3, the system couldn't find any Grade 3 classrooms.

## ✅ ដំណោះស្រាយ (Solution)

បានបង្កើត management command ថ្មីដើម្បីបង្កើតថ្នាក់ដែលខ្វះដោយស្វ័យប្រវត្តិ។

Created a new management command to automatically create missing classrooms.

### Command បានរត់:

```bash
python manage.py create_missing_classrooms --year "2026"
```

### លទ្ធផល (Results):

**For Academic Year 2026:**
- Grade 1 (ទី១): ✅ Already existed (skipped)
- Grade 2 (ទី២): ✅ Already existed (skipped)
- Grade 3 (ទី៣): ✅ **Created new classroom**
- Grade 4 (ទី៤): ✅ **Created new classroom**
- Grade 5 (ទី៥): ✅ **Created new classroom**
- Grade 6 (ទី៦): ✅ **Created new classroom**

**For Academic Year Year3:**
- បានបង្កើតថ្នាក់ទាំង ៦ (Created all 6 classrooms)

## 📋 ផ្លូវឡើងថ្នាក់ដែលមានបច្ចុប្បន្ន (Current Promotion Paths)

```
Grade 1 → Grade 2 ✅
Grade 2 → Grade 3 ✅
Grade 3 → Grade 4 ✅
Grade 4 → Grade 5 ✅
Grade 5 → Grade 6 ✅
Grade 6 → Grade 7 ⚠️  (Need to create Grade 7 classroom when ready)
```

## 🎯 តេស្តឥឡូវនេះ (Test Now)

1. ទៅកាន់ **"ដាក់សិស្សឡើងថ្នាក់"** (Student Promotion page)
2. ជ្រើសរើស **"ថ្នាក់បច្ចុប្បន្ន"** (Current Classroom) - ឧទាហរណ៍: ទី២ | 2026
3. ចុច **"ពិនិត្យលទ្ធផល"** (Check Results)
4. អ្នកគួរតែឃើញ dropdown **"ថ្នាក់ថ្មី"** (Next Classroom) ជាមួយជម្រើស:
   - ទី៣ | 2026 ✅
   - ទី៣ | Year3 ✅

## 🔧 Management Command

### ការប្រើប្រាស់ (Usage):

```bash
# Create classrooms for most recent academic year
python manage.py create_missing_classrooms

# Create classrooms for specific academic year
python manage.py create_missing_classrooms --year "2026"
```

### មុខងារ (Features):

- ✅ Automatically detects which grades are missing classrooms
- ✅ Creates one classroom per grade
- ✅ Skips grades that already have classrooms
- ✅ Shows promotion paths available after creation
- ✅ Safe to run multiple times (won't create duplicates)

## 📝 សម្រាប់អនាគត (For Future)

នៅពេលអ្នកត្រូវការបង្កើតថ្នាក់ទី៧-១២ (Grade 7-12):

1. បង្កើត Grade records សម្រាប់ថ្នាក់ទាំងនោះ (Create Grade records)
2. ដំណើរការ `python manage.py create_missing_classrooms` (Run the command)
3. ប្រព័ន្ធនឹងបង្កើតថ្នាក់ដែលខ្វះដោយស្វ័យប្រវត្តិ (System will auto-create missing classrooms)

## ✨ ឥឡូវនេះដំណើរការ! (Now It Works!)

អ្នកអាចឃើញ និងជ្រើសរើសថ្នាក់ត្រូវឡើងបានហើយ! 🎉

You can now see and select the next classroom for student promotion! 🎉
