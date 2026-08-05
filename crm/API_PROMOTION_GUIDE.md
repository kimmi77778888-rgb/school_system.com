# 🎓 Student Promotion API Guide
# មគ្គុទ្ទេសក៍ API ឡើងថ្នាក់សិស្ស

Complete API documentation for student promotion system following Cambodia Education System standards.

## 📚 Overview

The Promotion API provides endpoints for:
- **Checking promotion eligibility** - Verify which students can be promoted
- **Bulk promotion** - Promote multiple students at once
- **Promotion history** - View historical promotion records
- **Available classrooms** - Find valid next-grade classrooms

## 🔑 Authentication

All endpoints require authentication using Token Authentication:

```bash
# Login to get token
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "your_password"}'

# Response
{
  "token": "your_auth_token_here",
  "user_id": 1,
  "username": "admin",
  "role": "admin"
}

# Use token in subsequent requests
curl -X GET http://localhost:8000/api/students/ \
  -H "Authorization: Token your_auth_token_here"
```

## 📍 API Endpoints

### 1. Check Promotion Eligibility

**Endpoint:** `POST /api/students/check_promotion_eligibility/`

Check which students in a classroom are eligible for promotion based on Cambodia Education System criteria.

**Promotion Criteria:**
- ✅ Average score ≥ passing_percentage (default 50%)
- ✅ Attendance rate ≥ 80%
- ✅ Must have at least 1 subject with scores

**Request Body:**
```json
{
  "classroom_id": 1,
  "academic_year_id": 1,
  "passing_percentage": 50.0
}
```

**Parameters:**
- `classroom_id` (required): Current classroom ID
- `academic_year_id` (optional): Academic year to check (defaults to classroom's year)
- `passing_percentage` (optional): Minimum passing percentage (default: 50.0)

**Response:**
```json
{
  "classroom": "Grade 1 A | 2024-2025",
  "classroom_id": 1,
  "total_students": 25,
  "eligible_count": 20,
  "students": [
    {
      "student_id": 1,
      "student_name": "STU-0001 - សុខ សុផល",
      "student_code": "STU-0001",
      "current_classroom": "Grade 1 A | 2024-2025",
      "current_grade_number": 1,
      "total_subjects": 8,
      "passed_subjects": 8,
      "failed_subjects": 0,
      "avg_percentage": 75.5,
      "attendance_rate": 95.2,
      "total_days": 180,
      "present_days": 171,
      "can_promote": true,
      "promotion_status": "✅ អាចឡើងថ្នាក់",
      "reasons": []
    },
    {
      "student_id": 2,
      "student_name": "STU-0002 - ចន្ទ ចន្ទា",
      "student_code": "STU-0002",
      "current_classroom": "Grade 1 A | 2024-2025",
      "current_grade_number": 1,
      "total_subjects": 8,
      "passed_subjects": 5,
      "failed_subjects": 3,
      "avg_percentage": 45.2,
      "attendance_rate": 75.0,
      "total_days": 180,
      "present_days": 135,
      "can_promote": false,
      "promotion_status": "❌ មិនអាចឡើងថ្នាក់",
      "reasons": [
        "ពិន្ទុមធ្យម 45.2% < 50.0%",
        "វត្តមាន 75.0% < 80%"
      ]
    }
  ]
}
```

**Example Usage:**

```bash
# Check eligibility for classroom 1
curl -X POST http://localhost:8000/api/students/check_promotion_eligibility/ \
  -H "Authorization: Token your_token" \
  -H "Content-Type: application/json" \
  -d '{
    "classroom_id": 1,
    "academic_year_id": 1,
    "passing_percentage": 50.0
  }'
```

```python
# Python example
import requests

headers = {"Authorization": "Token your_token"}
data = {
    "classroom_id": 1,
    "academic_year_id": 1,
    "passing_percentage": 50.0
}

response = requests.post(
    "http://localhost:8000/api/students/check_promotion_eligibility/",
    headers=headers,
    json=data
)
print(response.json())
```

---

### 2. Bulk Promote Students

**Endpoint:** `POST /api/students/bulk_promote/`

Promote multiple students to the next grade following Cambodia Education System rules.

**Validation Rules:**
- ✅ Strict grade progression (Grade N → Grade N+1 only, no skipping)
- ✅ Level transition validation (Grade 6→7, Grade 9→10)
- ✅ No promotion beyond Grade 12
- ✅ Automatic history record creation

**Request Body:**
```json
{
  "student_ids": [1, 2, 3, 4, 5],
  "next_classroom_id": 5,
  "academic_year_id": 1,
  "passing_percentage": 50.0
}
```

**Parameters:**
- `student_ids` (required): Array of student IDs to promote
- `next_classroom_id` (required): Target classroom ID (must be next grade)
- `academic_year_id` (optional): Academic year for history records
- `passing_percentage` (optional): Used for history record calculation (default: 50.0)

**Response:**
```json
{
  "success": true,
  "message": "បានដាក់សិស្ស 3 នាក់ឡើងថ្នាក់ទៅ Grade 2 A | 2025-2026",
  "promoted_count": 3,
  "failed_count": 2,
  "promoted_students": [
    {
      "student_id": 1,
      "student_name": "STU-0001 - សុខ សុផល",
      "student_code": "STU-0001",
      "from_classroom": "Grade 1 A | 2024-2025",
      "to_classroom": "Grade 2 A | 2025-2026",
      "promotion_date": "05/08/2026",
      "level_transition": ""
    },
    {
      "student_id": 6,
      "student_name": "STU-0006 - ផល ផលា",
      "student_code": "STU-0006",
      "from_classroom": "Grade 6 A | 2024-2025",
      "to_classroom": "Grade 7 A | 2025-2026",
      "promotion_date": "05/08/2026",
      "level_transition": " (✅ ចូលបឋមភូមិ)"
    }
  ],
  "failed_promotions": [
    {
      "student_id": 2,
      "student_name": "STU-0002 - ចន្ទ ចន្ទា",
      "reason": "មិនអាចរំលងថ្នាក់បានទេ (ថ្នាក់ 1 → ថ្នាក់ 3)"
    },
    {
      "student_id": 12,
      "student_name": "STU-0012 - ធារា ធារី",
      "reason": "បញ្ចប់ការសិក្សាហើយ (Grade 12)"
    }
  ]
}
```

**Example Usage:**

```bash
# Promote students
curl -X POST http://localhost:8000/api/students/bulk_promote/ \
  -H "Authorization: Token your_token" \
  -H "Content-Type: application/json" \
  -d '{
    "student_ids": [1, 2, 3],
    "next_classroom_id": 5,
    "academic_year_id": 1,
    "passing_percentage": 50.0
  }'
```

```javascript
// JavaScript example
const response = await fetch('http://localhost:8000/api/students/bulk_promote/', {
  method: 'POST',
  headers: {
    'Authorization': 'Token your_token',
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    student_ids: [1, 2, 3],
    next_classroom_id: 5,
    academic_year_id: 1,
    passing_percentage: 50.0
  })
});

const result = await response.json();
console.log(result);
```

---

### 3. Get Available Promotion Classrooms

**Endpoint:** `GET /api/students/available_promotions/?classroom_id={id}`

Get list of valid next-grade classrooms for promotion (strict progression only).

**Query Parameters:**
- `classroom_id` (required): Current classroom ID

**Response:**
```json
{
  "current_classroom": "Grade 1 A | 2024-2025",
  "current_grade_number": 1,
  "next_grade_number": 2,
  "available_classrooms": [
    {
      "id": 5,
      "name": "Grade 2 A | 2025-2026",
      "grade_number": 2,
      "grade_name": "Grade 2",
      "grade_level": "primary",
      "academic_year": "2025-2026",
      "room_number": "202",
      "capacity": 40,
      "current_students": 28,
      "has_timetable": true,
      "timetable_count": 25
    },
    {
      "id": 6,
      "name": "Grade 2 B | 2025-2026",
      "grade_number": 2,
      "grade_name": "Grade 2",
      "grade_level": "primary",
      "academic_year": "2025-2026",
      "room_number": "203",
      "capacity": 40,
      "current_students": 30,
      "has_timetable": true,
      "timetable_count": 25
    }
  ],
  "total_available": 2
}
```

**Example Usage:**

```bash
curl -X GET "http://localhost:8000/api/students/available_promotions/?classroom_id=1" \
  -H "Authorization: Token your_token"
```

---

### 4. Get Student History

**Endpoint:** `GET /api/students/{id}/history/`

Get complete academic history for a specific student.

**Response:**
```json
[
  {
    "id": 10,
    "student": 1,
    "student_name": "STU-0001 - សុខ សុផល",
    "academic_year": 2,
    "academic_year_name": "2024-2025",
    "classroom": 1,
    "classroom_name": "Grade 1 A | 2024-2025",
    "grade_name": "Grade 1",
    "grade_number": 1,
    "grade_level": "primary",
    "grade_level_display": "បឋមសិក្សា (Primary)",
    "status": "PROMOTED",
    "status_display": "ឡើងថ្នាក់ (Promoted)",
    "average_score": 75.50,
    "total_subjects": 8,
    "passed_subjects": 8,
    "failed_subjects": 0,
    "total_days": 180,
    "present_days": 171,
    "absent_days": 9,
    "attendance_percentage": 95.0,
    "pass_percentage": 100.0,
    "start_date": null,
    "end_date": "2025-06-15",
    "promoted_to": "Grade 2 A | 2025-2026",
    "promotion_note": "ឡើងថ្នាក់ទៅ Grade 2 នៅថ្ងៃទី 15/06/2025",
    "notes": "ពិន្ទុមធ្យម: 75.5 | វត្តមាន: 171/180 ថ្ងៃ (95.0%)",
    "created_at": "2025-06-15T10:30:00Z",
    "updated_at": "2025-06-15T10:30:00Z"
  },
  {
    "id": 5,
    "student": 1,
    "student_name": "STU-0001 - សុខ សុផល",
    "academic_year": 1,
    "academic_year_name": "2023-2024",
    "classroom": 0,
    "classroom_name": "Kindergarten | 2023-2024",
    "grade_name": "Kindergarten",
    "grade_number": 0,
    "grade_level": "primary",
    "grade_level_display": "បឋមសិក្សា (Primary)",
    "status": "PROMOTED",
    "status_display": "ឡើងថ្នាក់ (Promoted)",
    "average_score": 80.00,
    "total_subjects": 5,
    "passed_subjects": 5,
    "failed_subjects": 0,
    "total_days": 160,
    "present_days": 155,
    "absent_days": 5,
    "attendance_percentage": 96.9,
    "pass_percentage": 100.0,
    "start_date": "2023-09-01",
    "end_date": "2024-06-10",
    "promoted_to": "Grade 1 A | 2024-2025",
    "promotion_note": "ឡើងថ្នាក់ទៅ Grade 1 នៅថ្ងៃទី 10/06/2024",
    "notes": "ពិន្ទុមធ្យម: 80.0 | វត្តមាន: 155/160 ថ្ងៃ (96.9%)",
    "created_at": "2024-06-10T09:00:00Z",
    "updated_at": "2024-06-10T09:00:00Z"
  }
]
```

**Example Usage:**

```bash
curl -X GET http://localhost:8000/api/students/1/history/ \
  -H "Authorization: Token your_token"
```

---

### 5. Student History ViewSet

**Base Endpoint:** `/api/student-history/`

Complete CRUD operations for student history (read-only).

#### 5.1 List All History Records

**Endpoint:** `GET /api/student-history/`

**Query Parameters:**
- `student` - Filter by student ID
- `academic_year` - Filter by academic year ID
- `grade_number` - Filter by grade number (1-12)
- `grade_level` - Filter by level (primary, lower_secondary, upper_secondary)
- `status` - Filter by status (ACTIVE, PROMOTED, GRADUATED, etc.)
- `search` - Search by student name or grade name
- `ordering` - Sort by fields (e.g., `-academic_year__year`)

**Example:**
```bash
curl -X GET "http://localhost:8000/api/student-history/?grade_level=primary&ordering=-average_score" \
  -H "Authorization: Token your_token"
```

#### 5.2 Get History by Student

**Endpoint:** `GET /api/student-history/by_student/?student_id={id}`

Get all history records for a specific student.

**Example:**
```bash
curl -X GET "http://localhost:8000/api/student-history/by_student/?student_id=1" \
  -H "Authorization: Token your_token"
```

#### 5.3 Get History by Academic Year

**Endpoint:** `GET /api/student-history/by_academic_year/?academic_year_id={id}`

Get all history records for a specific academic year.

**Example:**
```bash
curl -X GET "http://localhost:8000/api/student-history/by_academic_year/?academic_year_id=2" \
  -H "Authorization: Token your_token"
```

#### 5.4 Get Promotion Statistics

**Endpoint:** `GET /api/student-history/promotion_statistics/?academic_year_id={id}`

Get comprehensive promotion statistics for an academic year.

**Response:**
```json
{
  "total_students": 250,
  "promoted": 230,
  "graduated": 15,
  "transferred": 3,
  "withdrawn": 2,
  "average_score": 72.5,
  "average_attendance": 89.3,
  "by_grade_level": {
    "primary": {
      "total": 150,
      "promoted": 140,
      "avg_score": 75.2
    },
    "lower_secondary": {
      "total": 75,
      "promoted": 70,
      "avg_score": 70.5
    },
    "upper_secondary": {
      "total": 25,
      "promoted": 20,
      "avg_score": 68.8
    }
  }
}
```

**Example:**
```bash
curl -X GET "http://localhost:8000/api/student-history/promotion_statistics/?academic_year_id=2" \
  -H "Authorization: Token your_token"
```

---

## 🔒 Validation Rules

### Strict Grade Progression
```
✅ Grade 1 → Grade 2 (allowed)
✅ Grade 6 → Grade 7 (allowed, level transition)
❌ Grade 1 → Grade 3 (not allowed, skipping)
❌ Grade 6 → Grade 8 (not allowed, skipping)
```

### Level Transitions
```
Grade 6 → Grade 7: Primary → Lower Secondary (បឋមសិក្សា → បឋមភូមិ)
Grade 9 → Grade 10: Lower Secondary → Upper Secondary (បឋមភូមិ → មធ្យមភូមិ)
Grade 12: Graduation (បញ្ចប់ការសិក្សា)
```

### Promotion Criteria
```python
can_promote = (
    avg_percentage >= passing_percentage and  # Default: 50%
    total_subjects > 0 and                   # Has at least 1 subject
    attendance_rate >= 80.0                  # Attendance requirement
)
```

---

## 📊 Complete Workflow Example

### Step 1: Check Eligibility
```bash
curl -X POST http://localhost:8000/api/students/check_promotion_eligibility/ \
  -H "Authorization: Token your_token" \
  -H "Content-Type: application/json" \
  -d '{"classroom_id": 1, "passing_percentage": 50.0}'
```

### Step 2: Get Available Classrooms
```bash
curl -X GET "http://localhost:8000/api/students/available_promotions/?classroom_id=1" \
  -H "Authorization: Token your_token"
```

### Step 3: Promote Eligible Students
```bash
curl -X POST http://localhost:8000/api/students/bulk_promote/ \
  -H "Authorization: Token your_token" \
  -H "Content-Type: application/json" \
  -d '{
    "student_ids": [1, 3, 5, 7],
    "next_classroom_id": 5,
    "academic_year_id": 1
  }'
```

### Step 4: Verify History
```bash
curl -X GET http://localhost:8000/api/students/1/history/ \
  -H "Authorization: Token your_token"
```

---

## ⚠️ Error Responses

### 400 Bad Request
```json
{
  "error": "classroom_id is required"
}
```

### 404 Not Found
```json
{
  "detail": "Not found."
}
```

### 401 Unauthorized
```json
{
  "detail": "Authentication credentials were not provided."
}
```

---

## 📝 Notes

1. **Automatic History Creation**: When students are promoted, a `StudentHistory` record is automatically created preserving their academic data for that year.

2. **Status Updates**: Students remain `ACTIVE` after promotion (they're active in the new grade). History records show `PROMOTED` status.

3. **Data Preservation**: The history system preserves:
   - Grade information
   - Academic performance (scores, subjects)
   - Attendance records
   - Promotion details and notes

4. **Level Transitions**: Special notes are added for level transitions:
   - Grade 6 → 7: "✅ ចូលបឋមភូមិ"
   - Grade 9 → 10: "✅ ចូលមធ្យមភូមិ"

5. **Validation**: The API enforces strict Cambodia Education System rules to prevent invalid promotions.

---

## 🔗 Related Documentation

- [API Documentation](API_DOCUMENTATION.md)
- [Cambodia Promotion System](CAMBODIA_PROMOTION_SYSTEM.md)
- [API Examples](API_EXAMPLES.md)

---

**Last Updated:** 05/08/2026  
**Version:** 1.0  
**API Base URL:** `http://localhost:8000/api/`
