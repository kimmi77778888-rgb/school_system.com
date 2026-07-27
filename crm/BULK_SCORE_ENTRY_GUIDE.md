# បញ្ចូលពិន្ទុជាក្រុម (Bulk Score Entry) - User Guide

## Overview
This feature allows teachers and admins to enter exam scores for an entire class at once, instead of adding scores one student at a time.

## Features
✅ Select exam by academic year, classroom, and exam name
✅ Automatically loads all active students from the selected class
✅ Auto-calculate percentage and grade as you type
✅ Real-time validation (prevents scores above max score)
✅ Bulk actions: "Fill All Present" and "Clear All"
✅ Optional remarks field for each student
✅ Handles duplicate entries (updates existing scores)
✅ Skip students without scores (optional entry)

## How to Use

### Step 1: Access Bulk Score Entry
1. Go to **លទ្ធផលប្រឡង (Scores)** page
2. Click the green button **"បញ្ចូលពិន្ទុជាក្រុម"** (Bulk Score Entry)

### Step 2: Select Exam
1. **Select Academic Year** (ឆ្នាំសិក្សា)
   - Choose the school year for the exam
   
2. **Select Classroom** (ថ្នាក់)
   - Choose the class taking the exam
   
3. **Select Exam** (ការប្រឡង)
   - Choose the specific exam from the list
   - Shows: Exam name - Subject name
   
4. Click **"បន្ត"** (Continue)

### Step 3: Enter Scores
The page will display:
- **Exam Information Card** (gradient purple) showing:
  - Exam name
  - Subject
  - Classroom
  - Maximum score

- **Student List Table** with all students showing:
  - Student number
  - Student ID
  - Student name with photo
  - Score input field
  - Auto-calculated percentage
  - Auto-calculated grade (A, B, C, D, F)
  - Optional remarks field

### Step 4: Fill in Scores
- Enter score for each student (can use decimals like 85.5)
- As you type, percentage and grade automatically update
- Grade colors:
  - **A (90-100%)**: Green
  - **B (80-89%)**: Blue
  - **C (70-79%)**: Primary Blue
  - **D (60-69%)**: Yellow
  - **F (<60%)**: Red

### Step 5: Use Quick Actions (Optional)
- **"ពេញលេញទាំងអស់"** (Fill All Present): Sets all empty scores to maximum score
- **"សម្អាតទាំងអស់"** (Clear All): Clears all entered scores and remarks

### Step 6: Save
- Click **"រក្សាទុកពិន្ទុ"** (Save Scores)
- System will save all scores that have values entered
- Students without scores will be skipped (confirmation dialog will show count)
- Success message will show how many scores were saved

## Important Notes

### Auto-Calculations
- **Percentage**: Automatically calculated as (score / max_score) × 100
- **Grade Letter**: 
  - A: 90% and above
  - B: 80-89%
  - C: 70-79%
  - D: 60-69%
  - F: Below 60%

### Validation
- Score cannot be negative
- Score cannot exceed maximum score for the exam
- Invalid scores will be highlighted in red
- Cannot submit form with invalid scores

### Duplicate Handling
- If a score already exists for a student in the same subject/exam type/year, it will be **updated**
- This prevents duplicate score entries
- Uses Django's `update_or_create()` method

### Optional Entry
- You don't need to enter scores for all students
- Can enter scores for only some students
- Empty scores will be skipped when saving

## Technical Details

### Files Modified/Created
1. **Template**: `school/templates/school/score_bulk_entry.html`
   - New bulk entry interface with JavaScript calculations
   
2. **View**: `school/views.py`
   - Added `score_bulk_entry()` function
   
3. **URL**: `school/urls.py`
   - Added route: `scores/bulk-entry/`
   
4. **Updated**: `school/templates/school/score_list.html`
   - Added bulk entry button

### Database Operations
- Uses `Score.objects.update_or_create()` to prevent duplicates
- Respects unique constraint: `(student, subject, exam_type, academic_year)`
- Linked to `Exam` model for traceability

### Permissions
- Requires `@admin_or_teacher` decorator
- Teachers can only enter scores for their classes
- Admins can enter scores for any class

## Workflow Diagram
```
Score List Page
    ↓
Click "បញ្ចូលពិន្ទុជាក្រុម"
    ↓
Select Academic Year → Filters Classrooms
    ↓
Select Classroom → Filters Exams
    ↓
Select Exam → Loads Students
    ↓
Enter Scores (auto-calculate %, grade)
    ↓
Save → Creates/Updates Score records
    ↓
Redirect to Score List with success message
```

## Benefits
1. **Time Saving**: Enter scores for 30+ students in one page instead of 30+ separate forms
2. **Accuracy**: Auto-calculation eliminates manual percentage/grade calculation errors
3. **Efficiency**: Real-time validation prevents invalid data entry
4. **Flexibility**: Skip students or use quick-fill options
5. **Traceability**: Links scores to specific exam records

## Example Use Case
**Scenario**: Teacher needs to enter midterm exam scores for Math class (Grade 10A) with 35 students

**Old Way**: 
- Open score add form → Select student → Select subject → Enter score → Save
- Repeat 35 times ≈ 10-15 minutes

**New Way**:
- Open bulk entry → Select exam → Enter all 35 scores on one page → Save
- Total time ≈ 3-5 minutes

**Time Saved**: ~70%!

---

Created: 2026-07-27
Version: 1.0
