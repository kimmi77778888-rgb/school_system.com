# 🚀 REST API Quick Reference Card

## ⚡ Instant Access

**Your API is live at:** `http://localhost:8000/api/`

**Server running?** Check terminal or run: `python manage.py runserver`

## 🔑 Quick Login (Browser)

1. Go to: http://localhost:8000/api/
2. Click "Log in" (top right)
3. Enter your admin credentials
4. Start exploring!

## 📍 Most Used Endpoints

| Endpoint | What it does |
|----------|-------------|
| `/api/` | API root - see all endpoints |
| `/api/auth/login/` | Login and get token |
| `/api/dashboard/overview/` | Get system statistics |
| `/api/students/` | List all students |
| `/api/students/{id}/` | Get student details |
| `/api/teachers/` | List all teachers |
| `/api/attendance/` | Attendance records |
| `/api/attendance/today/` | Today's attendance |
| `/api/scores/` | Student scores |
| `/api/notifications/unread/` | Unread notifications |

## 🎯 Quick Code Examples

### JavaScript (Browser/Node.js)
```javascript
// Login
const response = await fetch('http://localhost:8000/api/auth/login/', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ username: 'admin', password: 'yourpass' })
});
const { token } = await response.json();

// Get students
const students = await fetch('http://localhost:8000/api/students/', {
  headers: { 'Authorization': `Token ${token}` }
});
const data = await students.json();
```

### Python
```python
import requests

# Login
r = requests.post('http://localhost:8000/api/auth/login/',
    json={'username': 'admin', 'password': 'yourpass'})
token = r.json()['token']

# Get students
headers = {'Authorization': f'Token {token}'}
students = requests.get('http://localhost:8000/api/students/',
    headers=headers).json()
```

### cURL
```bash
# Login
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "yourpass"}'

# Get students (use token from above)
curl http://localhost:8000/api/students/ \
  -H "Authorization: Token YOUR_TOKEN_HERE"
```

## 🔍 Query Parameters

| Parameter | Use | Example |
|-----------|-----|---------|
| `?search=john` | Search | `/api/students/?search=john` |
| `?page=2` | Pagination | `/api/students/?page=2` |
| `?page_size=50` | Items per page | `/api/students/?page_size=50` |
| `?ordering=name` | Sort ascending | `/api/students/?ordering=name` |
| `?ordering=-date` | Sort descending | `/api/students/?ordering=-date` |
| `?is_active=true` | Filter | `/api/students/?is_active=true` |
| `?classroom=1` | Filter by ID | `/api/students/?classroom=1` |

## 📚 Quick Documentation Links

| Need | File |
|------|------|
| Getting started | `START_HERE.md` |
| Quick guide | `API_QUICKSTART.md` |
| All endpoints | `API_DOCUMENTATION.md` |
| Code examples | `API_EXAMPLES.md` |
| Visual demo | `API_DEMO.html` |

## 🎨 HTTP Methods

| Method | Action | Example |
|--------|--------|---------|
| GET | Read/List | Get all students |
| POST | Create | Create new student |
| PUT | Update (full) | Update entire student record |
| PATCH | Update (partial) | Update student's name only |
| DELETE | Delete | Delete a student |

## 🔒 Authentication Header

Always include in your requests (after login):
```
Authorization: Token YOUR_TOKEN_HERE
```

## ⚠️ Common Issues

**"Authentication credentials were not provided"**
→ Include the Authorization header with your token

**"Invalid token"**
→ Login again to get a new token

**CORS errors in browser**
→ Add your frontend URL to CORS_ALLOWED_ORIGINS in .env

**Can't connect**
→ Make sure server is running: `python manage.py runserver`

## 🎯 Top 10 Actions

1. **Login**: `POST /api/auth/login/`
2. **Get dashboard**: `GET /api/dashboard/overview/`
3. **List students**: `GET /api/students/`
4. **Get student**: `GET /api/students/1/`
5. **Mark attendance**: `POST /api/attendance/`
6. **Get attendance**: `GET /api/attendance/today/`
7. **Add score**: `POST /api/scores/`
8. **List teachers**: `GET /api/teachers/`
9. **Get notifications**: `GET /api/notifications/unread/`
10. **Search students**: `GET /api/students/?search=name`

## 📊 Response Format

### Success (200 OK)
```json
{
  "count": 150,
  "next": "http://localhost:8000/api/students/?page=2",
  "previous": null,
  "results": [...]
}
```

### Created (201)
```json
{
  "id": 1,
  "student_id": "STU-0001",
  "full_name": "John Doe",
  ...
}
```

### Error (400)
```json
{
  "field_name": ["This field is required."]
}
```

## 🚀 Ready to Go!

**Start server**: `python manage.py runserver`  
**Open API**: http://localhost:8000/api/  
**Read docs**: `START_HERE.md`

---

Keep this file handy for quick reference! 🎉
