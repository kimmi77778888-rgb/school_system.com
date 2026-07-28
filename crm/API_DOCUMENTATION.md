# School Management System - REST API Documentation

## 🚀 Overview

This is a comprehensive REST API for the School Management System built with Django REST Framework. The API provides endpoints for managing students, teachers, classrooms, attendance, scores, notifications, and more.

## 📋 Base URL

```
http://localhost:8000/api/
```

## 🔐 Authentication

The API uses Token Authentication. Include the token in the request header:

```
Authorization: Token <your-token-here>
```

### Login Endpoint

**POST** `/api/auth/login/`

Request:
```json
{
  "username": "admin",
  "password": "your-password"
}
```

Response:
```json
{
  "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b",
  "user_id": 1,
  "username": "admin",
  "email": "admin@school.com",
  "role": "admin",
  "first_name": "Admin",
  "last_name": "User"
}
```

## 📚 API Endpoints

### Users & Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/login/` | Login and get token |
| GET | `/api/users/` | List all users |
| GET | `/api/users/{id}/` | Get user details |
| GET | `/api/users/me/` | Get current user info |
| POST | `/api/users/change_password/` | Change password |
| GET | `/api/user-profiles/` | List user profiles |
| GET | `/api/user-profiles/my_profile/` | Get current user's profile |
| GET | `/api/login-history/` | List login history |

### Academic Structure

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/academic-years/` | List academic years |
| POST | `/api/academic-years/` | Create academic year |
| GET | `/api/academic-years/{id}/` | Get academic year |
| PUT | `/api/academic-years/{id}/` | Update academic year |
| DELETE | `/api/academic-years/{id}/` | Delete academic year |
| GET | `/api/academic-years/active/` | Get active academic year |
| GET | `/api/grades/` | List grades |
| POST | `/api/grades/` | Create grade |

### Teachers

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/teachers/` | List all teachers |
| POST | `/api/teachers/` | Create teacher |
| GET | `/api/teachers/{id}/` | Get teacher details |
| PUT | `/api/teachers/{id}/` | Update teacher |
| DELETE | `/api/teachers/{id}/` | Delete teacher |
| GET | `/api/teachers/{id}/statistics/` | Get teacher statistics |
| GET | `/api/teachers/active/` | Get active teachers |
| GET | `/api/teacher-documents/` | List teacher documents |
| POST | `/api/teacher-documents/` | Upload document |
| GET | `/api/teacher-employment-history/` | List employment history |
| GET | `/api/teacher-attendance/` | List teacher attendance |
| POST | `/api/teacher-attendance/` | Mark teacher attendance |
| GET | `/api/teacher-attendance/today/` | Today's teacher attendance |
| GET | `/api/teacher-attendance/summary/` | Attendance summary |

### Students

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/students/` | List all students |
| POST | `/api/students/` | Create student |
| GET | `/api/students/{id}/` | Get student details |
| PUT | `/api/students/{id}/` | Update student |
| DELETE | `/api/students/{id}/` | Delete student |
| GET | `/api/students/{id}/statistics/` | Get student statistics |
| GET | `/api/students/{id}/report_card/` | Get student report card |
| GET | `/api/students/active/` | Get active students |

### Classrooms

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/classrooms/` | List classrooms |
| POST | `/api/classrooms/` | Create classroom |
| GET | `/api/classrooms/{id}/` | Get classroom details |
| GET | `/api/classrooms/{id}/students/` | Get classroom students |
| GET | `/api/classrooms/{id}/timetable/` | Get classroom timetable |

### Subjects & Timetable

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/subjects/` | List subjects |
| POST | `/api/subjects/` | Create subject |
| GET | `/api/timeslots/` | List time slots |
| POST | `/api/timeslots/` | Create time slot |
| GET | `/api/timetables/` | List timetables |
| POST | `/api/timetables/` | Create timetable entry |

### Attendance

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/attendance/` | List attendance records |
| POST | `/api/attendance/` | Mark attendance |
| GET | `/api/attendance/today/` | Today's attendance |
| GET | `/api/attendance/summary/` | Attendance summary |
| POST | `/api/attendance/bulk_create/` | Bulk mark attendance |

### Exams & Scores

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/exam-types/` | List exam types |
| POST | `/api/exam-types/` | Create exam type |
| GET | `/api/exams/` | List exams |
| POST | `/api/exams/` | Create exam |
| GET | `/api/scores/` | List scores |
| POST | `/api/scores/` | Create score |
| GET | `/api/scores/student_scores/?student_id={id}` | Get student scores |
| POST | `/api/scores/bulk_create/` | Bulk create scores |

### Notifications

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/notifications/` | List notifications |
| POST | `/api/notifications/` | Create notification |
| GET | `/api/notifications/{id}/` | Get notification |
| POST | `/api/notifications/{id}/mark_read/` | Mark as read |
| GET | `/api/notifications/unread/` | Get unread notifications |

### Report Cards

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/report-cards/` | List report cards |
| POST | `/api/report-cards/` | Create report card |
| GET | `/api/report-cards/{id}/` | Get report card |

### School Events

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/school-events/` | List events |
| POST | `/api/school-events/` | Create event |
| GET | `/api/school-events/upcoming/` | Get upcoming events |

### School Settings

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/school-settings/` | List settings |
| GET | `/api/school-settings/current/` | Get current settings |
| PUT | `/api/school-settings/{id}/` | Update settings |

### Dashboard & Analytics

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/dashboard/overview/` | Dashboard overview stats |
| GET | `/api/dashboard/attendance_today/` | Today's attendance stats |

## 🔍 Filtering, Searching & Ordering

### Filtering

Most list endpoints support filtering by specific fields. Use query parameters:

```
GET /api/students/?classroom=1&is_active=true
GET /api/teachers/?gender=M&is_active=true
GET /api/attendance/?student=1&date=2026-07-28
```

### Searching

Use the `search` parameter:

```
GET /api/students/?search=John
GET /api/teachers/?search=Smith
```

### Ordering

Use the `ordering` parameter:

```
GET /api/students/?ordering=last_name
GET /api/students/?ordering=-enrolled_date
```

### Pagination

Results are paginated (20 items per page). Navigate using:

```
GET /api/students/?page=2
```

Response includes:
```json
{
  "count": 150,
  "next": "http://localhost:8000/api/students/?page=3",
  "previous": "http://localhost:8000/api/students/?page=1",
  "results": [...]
}
```

## 📝 Example Requests

### Create a Student

**POST** `/api/students/`

```json
{
  "first_name": "សុខ",
  "last_name": "ចាន់",
  "first_name_en": "Sok",
  "last_name_en": "Chan",
  "gender": "M",
  "date_of_birth": "2010-05-15",
  "address": "Phnom Penh, Cambodia",
  "phone": "012345678",
  "parent_name": "Chan Dara",
  "parent_phone": "012987654",
  "classroom": 1,
  "blood_group": "O+"
}
```

### Mark Attendance

**POST** `/api/attendance/`

```json
{
  "student": 1,
  "date": "2026-07-28",
  "status": "P",
  "note": ""
}
```

### Bulk Mark Attendance

**POST** `/api/attendance/bulk_create/`

```json
{
  "attendance": [
    {
      "student": 1,
      "date": "2026-07-28",
      "status": "P"
    },
    {
      "student": 2,
      "date": "2026-07-28",
      "status": "A",
      "note": "Sick"
    }
  ]
}
```

### Create Exam Score

**POST** `/api/scores/`

```json
{
  "student": 1,
  "subject": 1,
  "exam_type": 1,
  "exam": 1,
  "academic_year": 1,
  "score": 85.5,
  "max_score": 100,
  "remarks": "Good performance"
}
```

### Bulk Create Scores

**POST** `/api/scores/bulk_create/`

```json
{
  "scores": [
    {
      "student": 1,
      "subject": 1,
      "exam_type": 1,
      "academic_year": 1,
      "score": 85.5,
      "max_score": 100
    },
    {
      "student": 2,
      "subject": 1,
      "exam_type": 1,
      "academic_year": 1,
      "score": 92.0,
      "max_score": 100
    }
  ]
}
```

### Create Notification

**POST** `/api/notifications/`

```json
{
  "title": "Parent-Teacher Meeting",
  "message": "Reminder: Parent-teacher meeting on Friday at 2 PM.",
  "notification_type": "reminder",
  "audience": "parents",
  "is_active": true
}
```

### Get Student Statistics

**GET** `/api/students/1/statistics/`

Response:
```json
{
  "total_scores": 15,
  "average_score": 87.5,
  "attendance_records": 120,
  "present_days": 110,
  "absent_days": 10
}
```

### Get Attendance Summary

**GET** `/api/attendance/summary/?student=1&start_date=2026-01-01&end_date=2026-07-28`

Response:
```json
{
  "total_days": 120,
  "present": 110,
  "absent": 8,
  "late": 2,
  "excused": 0
}
```

## 🎯 Common Query Parameters

| Parameter | Description | Example |
|-----------|-------------|---------|
| `search` | Search across multiple fields | `?search=John` |
| `ordering` | Sort results | `?ordering=-date` |
| `page` | Page number for pagination | `?page=2` |
| `page_size` | Items per page | `?page_size=50` |
| `student` | Filter by student ID | `?student=1` |
| `teacher` | Filter by teacher ID | `?teacher=1` |
| `classroom` | Filter by classroom ID | `?classroom=1` |
| `date` | Filter by date | `?date=2026-07-28` |
| `start_date` | Filter from date | `?start_date=2026-01-01` |
| `end_date` | Filter to date | `?end_date=2026-07-28` |
| `is_active` | Filter active records | `?is_active=true` |
| `academic_year` | Filter by academic year | `?academic_year=1` |

## 🔒 Permissions

- All endpoints require authentication
- Users can only access data appropriate to their role
- Login history: Users see only their own, admins see all
- Most write operations require admin or teacher role

## 🌐 CORS Configuration

CORS is enabled for configured origins (set in environment):

```bash
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173
```

## 📦 Response Format

### Success Response

```json
{
  "id": 1,
  "field1": "value1",
  "field2": "value2"
}
```

### Error Response

```json
{
  "error": "Error message description"
}
```

### Validation Error

```json
{
  "field_name": [
    "This field is required."
  ]
}
```

## 🧪 Testing the API

### Using cURL

```bash
# Login
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'

# Get students (with token)
curl http://localhost:8000/api/students/ \
  -H "Authorization: Token YOUR_TOKEN_HERE"
```

### Using Python requests

```python
import requests

# Login
response = requests.post('http://localhost:8000/api/auth/login/', 
    json={'username': 'admin', 'password': 'admin123'})
token = response.json()['token']

# Get students
headers = {'Authorization': f'Token {token}'}
response = requests.get('http://localhost:8000/api/students/', headers=headers)
students = response.json()
```

### Using JavaScript fetch

```javascript
// Login
const loginResponse = await fetch('http://localhost:8000/api/auth/login/', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ username: 'admin', password: 'admin123' })
});
const { token } = await loginResponse.json();

// Get students
const studentsResponse = await fetch('http://localhost:8000/api/students/', {
  headers: { 'Authorization': `Token ${token}` }
});
const students = await studentsResponse.json();
```

## 📱 Browsable API

Django REST Framework provides a browsable web interface for the API. Visit any endpoint in your browser while logged in:

```
http://localhost:8000/api/
http://localhost:8000/api/students/
http://localhost:8000/api/teachers/
```

## 🚀 Getting Started

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run migrations:
```bash
python manage.py migrate
```

3. Create a superuser:
```bash
python manage.py createsuperuser
```

4. Start the server:
```bash
python manage.py runserver
```

5. Access the API at:
```
http://localhost:8000/api/
```

## 📄 Additional Resources

- [Django REST Framework Documentation](https://www.django-rest-framework.org/)
- [API Root](http://localhost:8000/api/)
- [Admin Panel](http://localhost:8000/admin/)
- [School Dashboard](http://localhost:8000/school/)

## 🤝 Support

For questions or issues, please contact the development team or refer to the project documentation.
