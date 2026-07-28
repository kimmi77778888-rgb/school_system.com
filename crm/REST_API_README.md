# 🎓 School Management System REST API

## ✨ Overview

A comprehensive REST API for the School Management System built with Django REST Framework. This API provides complete access to all school management features including students, teachers, attendance, scores, notifications, and more.

## 🚀 Features

- ✅ **Token-based Authentication** - Secure API access with tokens
- ✅ **Complete CRUD Operations** - Full create, read, update, delete for all resources
- ✅ **Advanced Filtering** - Filter by any field with query parameters
- ✅ **Search Functionality** - Full-text search across multiple fields
- ✅ **Pagination** - Efficient data loading with customizable page sizes
- ✅ **Bulk Operations** - Bulk create attendance and scores
- ✅ **Role-based Access** - Permissions based on user roles
- ✅ **CORS Support** - Ready for frontend integration
- ✅ **Browsable API** - Built-in web interface for testing
- ✅ **Comprehensive Documentation** - Detailed docs with examples

## 📦 What's Included

### API Endpoints (50+)

- **Authentication** - Login, logout, password change
- **Users & Profiles** - User management and profiles
- **Students** - Complete student management
- **Teachers** - Teacher information and documents
- **Classrooms** - Class management and timetables
- **Subjects** - Subject and curriculum management
- **Attendance** - Student and teacher attendance tracking
- **Exams & Scores** - Exam management and grade tracking
- **Notifications** - System-wide notifications
- **Report Cards** - Student report generation
- **School Events** - Event calendar management
- **Dashboard** - Analytics and statistics
- **School Settings** - System configuration

### Files Created

1. **`school/serializers.py`** - Data serialization (500+ lines)
2. **`school/api_views.py`** - API endpoints and logic (700+ lines)
3. **`school/api_urls.py`** - URL routing configuration
4. **`API_DOCUMENTATION.md`** - Complete API reference
5. **`API_QUICKSTART.md`** - Quick start guide
6. **`API_EXAMPLES.md`** - Integration examples
7. **`test_api.py`** - API testing script
8. **`REST_API_README.md`** - This file

## ⚡ Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run Migrations

```bash
python manage.py migrate
```

### 3. Start Server

```bash
python manage.py runserver
```

### 4. Access API

- **API Root**: http://localhost:8000/api/
- **Browsable API**: http://localhost:8000/api/ (in browser)
- **Admin Panel**: http://localhost:8000/admin/

### 5. Test the API

```bash
# Option 1: Run test script
python test_api.py

# Option 2: Use browser
# Go to http://localhost:8000/api/ and login

# Option 3: Use cURL
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "yourpassword"}'
```

## 📚 Documentation

| Document | Description |
|----------|-------------|
| [API_QUICKSTART.md](./API_QUICKSTART.md) | Get started in 5 minutes |
| [API_DOCUMENTATION.md](./API_DOCUMENTATION.md) | Complete API reference |
| [API_EXAMPLES.md](./API_EXAMPLES.md) | Integration examples (React, Vue, Python, Flutter) |

## 🔑 Authentication

### Login and Get Token

```bash
POST /api/auth/login/
```

```json
{
  "username": "admin",
  "password": "yourpassword"
}
```

**Response:**
```json
{
  "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b",
  "user_id": 1,
  "username": "admin",
  "email": "admin@school.com",
  "role": "admin"
}
```

### Use Token in Requests

```bash
curl http://localhost:8000/api/students/ \
  -H "Authorization: Token YOUR_TOKEN_HERE"
```

## 📱 Example Usage

### Get Students List

```bash
GET /api/students/?page=1&is_active=true&search=John
```

### Create Student

```bash
POST /api/students/
```

```json
{
  "first_name": "John",
  "last_name": "Doe",
  "gender": "M",
  "classroom": 1,
  "date_of_birth": "2010-05-15"
}
```

### Mark Attendance

```bash
POST /api/attendance/
```

```json
{
  "student": 1,
  "date": "2026-07-28",
  "status": "P"
}
```

### Get Dashboard Stats

```bash
GET /api/dashboard/overview/
```

**Response:**
```json
{
  "total_students": 150,
  "total_teachers": 25,
  "total_classrooms": 12,
  "total_subjects": 15,
  "active_academic_year": "2025-2026"
}
```

## 🎯 Key Features

### Filtering

```bash
# Filter by multiple fields
GET /api/students/?classroom=1&gender=M&is_active=true

# Filter attendance by date range
GET /api/attendance/?start_date=2026-01-01&end_date=2026-07-28
```

### Searching

```bash
# Search across multiple fields
GET /api/students/?search=John
GET /api/teachers/?search=Math
```

### Ordering

```bash
# Sort results
GET /api/students/?ordering=last_name
GET /api/students/?ordering=-enrolled_date  # descending
```

### Pagination

```bash
# Navigate pages
GET /api/students/?page=2&page_size=50
```

### Bulk Operations

```bash
POST /api/attendance/bulk_create/
```

```json
{
  "attendance": [
    {"student": 1, "date": "2026-07-28", "status": "P"},
    {"student": 2, "date": "2026-07-28", "status": "A"}
  ]
}
```

## 🌐 Frontend Integration

### React

```javascript
import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000/api',
  headers: {
    'Authorization': `Token ${localStorage.getItem('token')}`
  }
});

// Get students
const students = await api.get('/students/');

// Create student
const newStudent = await api.post('/students/', studentData);
```

### Vue.js

```javascript
// In your Vue component
async mounted() {
  const response = await fetch('http://localhost:8000/api/students/', {
    headers: {
      'Authorization': `Token ${this.token}`
    }
  });
  this.students = await response.json();
}
```

### Python

```python
import requests

# Login
response = requests.post('http://localhost:8000/api/auth/login/',
    json={'username': 'admin', 'password': 'admin123'})
token = response.json()['token']

# Get students
headers = {'Authorization': f'Token {token}'}
students = requests.get('http://localhost:8000/api/students/', headers=headers)
```

See [API_EXAMPLES.md](./API_EXAMPLES.md) for complete integration examples.

## 🔒 Security Features

- ✅ Token-based authentication
- ✅ Role-based access control
- ✅ CORS configuration for frontend apps
- ✅ HTTPS support (production)
- ✅ Secure password handling
- ✅ Input validation
- ✅ SQL injection protection

## ⚙️ Configuration

### Environment Variables

Add to your `.env` file:

```bash
# CORS - Allow frontend apps
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173

# Database (optional)
DATABASE_URL=postgresql://user:pass@localhost/dbname

# Django settings
DEBUG=True
SECRET_KEY=your-secret-key
```

### CORS Setup

The API is pre-configured for CORS. Just set your frontend URLs:

```python
# In settings.py
CORS_ALLOWED_ORIGINS = os.environ.get(
    'CORS_ALLOWED_ORIGINS',
    'http://localhost:3000,http://localhost:5173'
).split(',')
```

## 📊 Available Endpoints Summary

| Category | Endpoints | Count |
|----------|-----------|-------|
| Authentication | `/api/auth/*` | 2 |
| Users | `/api/users/*`, `/api/user-profiles/*` | 6 |
| Students | `/api/students/*` | 5 |
| Teachers | `/api/teachers/*`, `/api/teacher-*` | 12 |
| Classrooms | `/api/classrooms/*` | 4 |
| Subjects | `/api/subjects/*`, `/api/timeslots/*`, `/api/timetables/*` | 6 |
| Attendance | `/api/attendance/*`, `/api/teacher-attendance/*` | 8 |
| Exams | `/api/exams/*`, `/api/exam-types/*`, `/api/scores/*` | 7 |
| Notifications | `/api/notifications/*` | 4 |
| Reports | `/api/report-cards/*` | 3 |
| Events | `/api/school-events/*` | 3 |
| Settings | `/api/school-settings/*` | 2 |
| Dashboard | `/api/dashboard/*` | 2 |

**Total: 60+ endpoints**

## 🧪 Testing

### Using the Test Script

```bash
python test_api.py
```

This will:
- Test authentication
- Fetch dashboard stats
- List students and teachers
- Check attendance
- Get notifications

### Using Browsable API

1. Go to http://localhost:8000/api/
2. Login with your credentials
3. Browse and test endpoints interactively

### Using Postman/Insomnia

Import the API and start testing:
- Base URL: `http://localhost:8000/api`
- Auth: Token authentication
- Headers: `Authorization: Token YOUR_TOKEN`

## 🐛 Troubleshooting

### "Authentication credentials were not provided"

Make sure you include the authorization header:
```
Authorization: Token YOUR_TOKEN_HERE
```

### CORS Errors

Add your frontend URL to `CORS_ALLOWED_ORIGINS` in `.env`:
```
CORS_ALLOWED_ORIGINS=http://localhost:3000
```

### Token Not Working

Get a new token by logging in again:
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "yourpassword"}'
```

## 📖 Learn More

- [Django REST Framework Documentation](https://www.django-rest-framework.org/)
- [API Authentication Guide](https://www.django-rest-framework.org/api-guide/authentication/)
- [Filtering Documentation](https://django-filter.readthedocs.io/)

## 🤝 Support

For questions or issues:
1. Check the documentation files
2. Test with the browsable API at http://localhost:8000/api/
3. Run `python test_api.py` to verify setup
4. Review the examples in [API_EXAMPLES.md](./API_EXAMPLES.md)

## 🎉 What's Next?

Now that your REST API is ready, you can:

1. **Build a Frontend** - Use React, Vue, or Angular
2. **Create Mobile Apps** - Flutter, React Native, or native iOS/Android
3. **Integrate with Other Systems** - CRM, payment gateways, etc.
4. **Add More Features** - Custom endpoints, webhooks, etc.
5. **Deploy to Production** - Heroku, AWS, DigitalOcean, etc.

## 📄 License

This project is part of the School Management System.

---

**Happy Coding! 🚀**

Built with ❤️ using Django REST Framework
