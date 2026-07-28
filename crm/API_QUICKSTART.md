# REST API Quick Start Guide

## 🚀 Installation & Setup

### 1. Install New Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- `djangorestframework` - REST API framework
- `django-filter` - Advanced filtering
- `django-cors-headers` - CORS support for frontend apps

### 2. Run Migrations

```bash
python manage.py migrate
```

### 3. Create API Tokens for Existing Users (Optional)

```bash
python manage.py shell
```

```python
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

# Create tokens for all users
for user in User.objects.all():
    Token.objects.get_or_create(user=user)
    
# Or create token for specific user
user = User.objects.get(username='admin')
token, created = Token.objects.get_or_create(user=user)
print(f"Token for {user.username}: {token.key}")
```

### 4. Start the Server

```bash
python manage.py runserver
```

## 🎯 Quick Test

### Method 1: Using the Browsable API

1. Open your browser and go to: `http://localhost:8000/api/`
2. You'll see a nice web interface for browsing the API
3. Login using the login form (top right)
4. Browse through different endpoints

### Method 2: Using the Test Script

```bash
python test_api.py
```

Enter your credentials when prompted.

### Method 3: Using cURL

```bash
# 1. Login and get token
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d "{\"username\": \"admin\", \"password\": \"yourpassword\"}"

# Response will include your token:
# {"token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b", ...}

# 2. Use the token to access endpoints
curl http://localhost:8000/api/students/ \
  -H "Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
```

## 📱 Quick Examples

### Get Dashboard Statistics

```bash
GET /api/dashboard/overview/
```

Response:
```json
{
  "total_students": 150,
  "total_teachers": 25,
  "total_classrooms": 12,
  "total_subjects": 15,
  "active_academic_year": "2025-2026"
}
```

### List Students

```bash
GET /api/students/?page_size=10&is_active=true
```

### Search Students

```bash
GET /api/students/?search=John
```

### Filter Students by Classroom

```bash
GET /api/students/?classroom=1
```

### Get Student Details

```bash
GET /api/students/1/
```

### Get Student Statistics

```bash
GET /api/students/1/statistics/
```

### Mark Attendance

```bash
POST /api/attendance/
Content-Type: application/json

{
  "student": 1,
  "date": "2026-07-28",
  "status": "P"
}
```

### Get Today's Attendance

```bash
GET /api/attendance/today/
```

### Create a Score

```bash
POST /api/scores/
Content-Type: application/json

{
  "student": 1,
  "subject": 1,
  "exam_type": 1,
  "academic_year": 1,
  "score": 85.5,
  "max_score": 100
}
```

### Get Unread Notifications

```bash
GET /api/notifications/unread/
```

## 🔑 Key Features

### 1. Token Authentication
- Secure API access with tokens
- Tokens are automatically generated on login

### 2. Role-Based Access
- Users see data appropriate to their role
- Admins have full access
- Teachers and parents have restricted access

### 3. Advanced Filtering
- Filter by any field: `?classroom=1&is_active=true`
- Search across multiple fields: `?search=John`
- Order results: `?ordering=-date`

### 4. Pagination
- Default 20 items per page
- Customize with `?page_size=50`
- Navigate with `?page=2`

### 5. Bulk Operations
- Bulk mark attendance: `/api/attendance/bulk_create/`
- Bulk create scores: `/api/scores/bulk_create/`

### 6. Custom Actions
- Get active teachers: `/api/teachers/active/`
- Get today's attendance: `/api/attendance/today/`
- Get attendance summary: `/api/attendance/summary/`
- Get upcoming events: `/api/school-events/upcoming/`

## 🌐 CORS Configuration

For frontend development (React, Vue, Angular, etc.), configure CORS in `.env`:

```bash
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173
```

## 📚 Available Endpoints

### Core Resources
- `/api/students/` - Student management
- `/api/teachers/` - Teacher management
- `/api/classrooms/` - Classroom management
- `/api/subjects/` - Subject management

### Attendance & Academic
- `/api/attendance/` - Student attendance
- `/api/teacher-attendance/` - Teacher attendance
- `/api/timetables/` - Class schedules
- `/api/exams/` - Exam management
- `/api/scores/` - Score tracking

### Communication
- `/api/notifications/` - System notifications
- `/api/school-events/` - Event calendar

### Reports & Analytics
- `/api/report-cards/` - Student report cards
- `/api/dashboard/` - Dashboard statistics

### Administration
- `/api/academic-years/` - Academic year management
- `/api/grades/` - Grade levels
- `/api/school-settings/` - School configuration

## 🔐 Security Best Practices

1. **Never share your token** - Treat it like a password
2. **Use HTTPS in production** - Don't send tokens over HTTP
3. **Rotate tokens regularly** - Delete old tokens periodically
4. **Use environment variables** - Store sensitive data in `.env`

## 🐛 Troubleshooting

### "Authentication credentials were not provided"
Make sure you include the token header:
```
Authorization: Token YOUR_TOKEN_HERE
```

### "Invalid token"
Your token may have expired or been deleted. Login again to get a new token.

### CORS errors in browser
Add your frontend URL to `CORS_ALLOWED_ORIGINS` in settings.

## 📖 Full Documentation

For complete API documentation with all endpoints, parameters, and examples, see:
- [API_DOCUMENTATION.md](./API_DOCUMENTATION.md)
- Browsable API: http://localhost:8000/api/

## 💡 Next Steps

1. ✅ Test the API using the browsable interface
2. ✅ Try the test script: `python test_api.py`
3. ✅ Review full documentation in `API_DOCUMENTATION.md`
4. 🚀 Build a frontend app using the API
5. 📱 Create a mobile app
6. 🔗 Integrate with other systems

## 🤝 Support

For questions or issues:
1. Check the full documentation: `API_DOCUMENTATION.md`
2. Review Django REST Framework docs: https://www.django-rest-framework.org/
3. Contact the development team

---

**Happy Coding! 🎉**
