# REST API Usage Examples

## 📱 Frontend Integration Examples

### React Example

```javascript
// api.js - API service
const API_BASE_URL = 'http://localhost:8000/api';

class SchoolAPI {
  constructor() {
    this.token = localStorage.getItem('token');
  }

  async login(username, password) {
    const response = await fetch(`${API_BASE_URL}/auth/login/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ username, password })
    });
    
    if (!response.ok) throw new Error('Login failed');
    
    const data = await response.json();
    this.token = data.token;
    localStorage.setItem('token', data.token);
    localStorage.setItem('userRole', data.role);
    return data;
  }

  async getStudents(page = 1, search = '') {
    const params = new URLSearchParams({ page, search });
    const response = await fetch(`${API_BASE_URL}/students/?${params}`, {
      headers: {
        'Authorization': `Token ${this.token}`
      }
    });
    return response.json();
  }

  async getStudent(id) {
    const response = await fetch(`${API_BASE_URL}/students/${id}/`, {
      headers: {
        'Authorization': `Token ${this.token}`
      }
    });
    return response.json();
  }

  async createStudent(studentData) {
    const response = await fetch(`${API_BASE_URL}/students/`, {
      method: 'POST',
      headers: {
        'Authorization': `Token ${this.token}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(studentData)
    });
    return response.json();
  }

  async markAttendance(attendanceData) {
    const response = await fetch(`${API_BASE_URL}/attendance/`, {
      method: 'POST',
      headers: {
        'Authorization': `Token ${this.token}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(attendanceData)
    });
    return response.json();
  }

  async getDashboard() {
    const response = await fetch(`${API_BASE_URL}/dashboard/overview/`, {
      headers: {
        'Authorization': `Token ${this.token}`
      }
    });
    return response.json();
  }
}

export default new SchoolAPI();
```

```javascript
// StudentsList.jsx - React Component
import React, { useState, useEffect } from 'react';
import api from './api';

function StudentsList() {
  const [students, setStudents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [page, setPage] = useState(1);

  useEffect(() => {
    loadStudents();
  }, [page, search]);

  const loadStudents = async () => {
    setLoading(true);
    try {
      const data = await api.getStudents(page, search);
      setStudents(data.results);
    } catch (error) {
      console.error('Error loading students:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h2>Students</h2>
      <input
        type="text"
        placeholder="Search students..."
        value={search}
        onChange={(e) => setSearch(e.target.value)}
      />
      
      {loading ? (
        <p>Loading...</p>
      ) : (
        <ul>
          {students.map(student => (
            <li key={student.id}>
              {student.full_name} - {student.student_id}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default StudentsList;
```

### Vue.js Example

```javascript
// api.js
import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000/api',
});

// Add token to all requests
api.interceptors.request.use(config => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Token ${token}`;
  }
  return config;
});

export default {
  // Auth
  login(username, password) {
    return api.post('/auth/login/', { username, password });
  },

  // Students
  getStudents(params) {
    return api.get('/students/', { params });
  },
  
  getStudent(id) {
    return api.get(`/students/${id}/`);
  },

  createStudent(data) {
    return api.post('/students/', data);
  },

  updateStudent(id, data) {
    return api.put(`/students/${id}/`, data);
  },

  // Attendance
  markAttendance(data) {
    return api.post('/attendance/', data);
  },

  getTodayAttendance() {
    return api.get('/attendance/today/');
  },

  // Dashboard
  getDashboard() {
    return api.get('/dashboard/overview/');
  },
};
```

```vue
<!-- StudentsList.vue -->
<template>
  <div class="students-list">
    <h2>Students</h2>
    
    <input
      v-model="search"
      type="text"
      placeholder="Search students..."
      @input="loadStudents"
    />
    
    <div v-if="loading">Loading...</div>
    
    <ul v-else>
      <li v-for="student in students" :key="student.id">
        {{ student.full_name }} - {{ student.student_id }}
      </li>
    </ul>
    
    <button @click="prevPage" :disabled="!hasPrev">Previous</button>
    <button @click="nextPage" :disabled="!hasNext">Next</button>
  </div>
</template>

<script>
import api from './api';

export default {
  name: 'StudentsList',
  data() {
    return {
      students: [],
      loading: false,
      search: '',
      page: 1,
      count: 0,
    };
  },
  computed: {
    hasPrev() {
      return this.page > 1;
    },
    hasNext() {
      return this.page * 20 < this.count;
    },
  },
  methods: {
    async loadStudents() {
      this.loading = true;
      try {
        const response = await api.getStudents({
          page: this.page,
          search: this.search,
        });
        this.students = response.data.results;
        this.count = response.data.count;
      } catch (error) {
        console.error('Error loading students:', error);
      } finally {
        this.loading = false;
      }
    },
    nextPage() {
      this.page++;
      this.loadStudents();
    },
    prevPage() {
      this.page--;
      this.loadStudents();
    },
  },
  mounted() {
    this.loadStudents();
  },
};
</script>
```

### Python Requests Example

```python
# school_api_client.py
import requests
from typing import Optional, Dict, List

class SchoolAPIClient:
    def __init__(self, base_url: str = 'http://localhost:8000/api'):
        self.base_url = base_url
        self.token: Optional[str] = None
        self.headers = {}
    
    def login(self, username: str, password: str) -> Dict:
        """Login and get authentication token"""
        response = requests.post(
            f'{self.base_url}/auth/login/',
            json={'username': username, 'password': password}
        )
        response.raise_for_status()
        data = response.json()
        self.token = data['token']
        self.headers = {'Authorization': f'Token {self.token}'}
        return data
    
    def get_students(self, page: int = 1, search: str = '', 
                     is_active: bool = True) -> Dict:
        """Get list of students"""
        params = {
            'page': page,
            'search': search,
            'is_active': is_active
        }
        response = requests.get(
            f'{self.base_url}/students/',
            headers=self.headers,
            params=params
        )
        response.raise_for_status()
        return response.json()
    
    def get_student(self, student_id: int) -> Dict:
        """Get student details"""
        response = requests.get(
            f'{self.base_url}/students/{student_id}/',
            headers=self.headers
        )
        response.raise_for_status()
        return response.json()
    
    def create_student(self, student_data: Dict) -> Dict:
        """Create a new student"""
        response = requests.post(
            f'{self.base_url}/students/',
            headers=self.headers,
            json=student_data
        )
        response.raise_for_status()
        return response.json()
    
    def mark_attendance(self, student_id: int, date: str, 
                       status: str = 'P', note: str = '') -> Dict:
        """Mark student attendance"""
        data = {
            'student': student_id,
            'date': date,
            'status': status,
            'note': note
        }
        response = requests.post(
            f'{self.base_url}/attendance/',
            headers=self.headers,
            json=data
        )
        response.raise_for_status()
        return response.json()
    
    def bulk_mark_attendance(self, attendance_list: List[Dict]) -> Dict:
        """Bulk mark attendance for multiple students"""
        data = {'attendance': attendance_list}
        response = requests.post(
            f'{self.base_url}/attendance/bulk_create/',
            headers=self.headers,
            json=data
        )
        response.raise_for_status()
        return response.json()
    
    def get_dashboard(self) -> Dict:
        """Get dashboard statistics"""
        response = requests.get(
            f'{self.base_url}/dashboard/overview/',
            headers=self.headers
        )
        response.raise_for_status()
        return response.json()

# Usage example
if __name__ == '__main__':
    client = SchoolAPIClient()
    
    # Login
    client.login('admin', 'admin123')
    
    # Get students
    students = client.get_students(search='John')
    print(f"Found {students['count']} students")
    
    # Mark attendance
    from datetime import date
    today = date.today().isoformat()
    client.mark_attendance(
        student_id=1,
        date=today,
        status='P'
    )
    
    # Get dashboard
    dashboard = client.get_dashboard()
    print(f"Total students: {dashboard['total_students']}")
```

### Mobile App (Flutter) Example

```dart
// api_service.dart
import 'package:http/http.dart' as http;
import 'dart:convert';

class SchoolAPIService {
  static const String baseUrl = 'http://localhost:8000/api';
  String? token;

  Future<Map<String, dynamic>> login(String username, String password) async {
    final response = await http.post(
      Uri.parse('$baseUrl/auth/login/'),
      headers: {'Content-Type': 'application/json'},
      body: json.encode({
        'username': username,
        'password': password,
      }),
    );

    if (response.statusCode == 200) {
      final data = json.decode(response.body);
      token = data['token'];
      return data;
    } else {
      throw Exception('Login failed');
    }
  }

  Future<Map<String, dynamic>> getStudents({int page = 1, String search = ''}) async {
    final uri = Uri.parse('$baseUrl/students/').replace(
      queryParameters: {
        'page': page.toString(),
        'search': search,
      },
    );

    final response = await http.get(
      uri,
      headers: {
        'Authorization': 'Token $token',
      },
    );

    if (response.statusCode == 200) {
      return json.decode(response.body);
    } else {
      throw Exception('Failed to load students');
    }
  }

  Future<Map<String, dynamic>> markAttendance({
    required int studentId,
    required String date,
    required String status,
    String note = '',
  }) async {
    final response = await http.post(
      Uri.parse('$baseUrl/attendance/'),
      headers: {
        'Authorization': 'Token $token',
        'Content-Type': 'application/json',
      },
      body: json.encode({
        'student': studentId,
        'date': date,
        'status': status,
        'note': note,
      }),
    );

    if (response.statusCode == 201) {
      return json.decode(response.body);
    } else {
      throw Exception('Failed to mark attendance');
    }
  }
}
```

## 🔄 Advanced Usage Examples

### Bulk Operations

```python
# Bulk mark attendance for entire classroom
from datetime import date

client = SchoolAPIClient()
client.login('teacher', 'password')

# Get all students in classroom
classroom_id = 1
students = client.get_students()

# Prepare attendance data
today = date.today().isoformat()
attendance_list = [
    {
        'student': student['id'],
        'date': today,
        'status': 'P',  # Present by default
    }
    for student in students['results']
]

# Mark specific students as absent
absent_ids = [5, 12, 18]
for record in attendance_list:
    if record['student'] in absent_ids:
        record['status'] = 'A'
        record['note'] = 'Sick'

# Submit bulk attendance
result = client.bulk_mark_attendance(attendance_list)
print(f"Marked attendance for {len(result)} students")
```

### Filtering & Searching

```javascript
// Get students by multiple criteria
const students = await api.getStudents({
  classroom: 1,
  gender: 'M',
  is_active: true,
  search: 'John',
  ordering: 'last_name',
  page_size: 50
});

// Get teachers by specialty
const mathTeachers = await api.get('/teachers/', {
  params: {
    subject_specialty: 'Mathematics',
    is_active: true
  }
});

// Get attendance for date range
const attendance = await api.get('/attendance/summary/', {
  params: {
    student: 1,
    start_date: '2026-01-01',
    end_date: '2026-07-28'
  }
});
```

### File Upload

```javascript
// Upload student photo
async function uploadStudentPhoto(studentId, file) {
  const formData = new FormData();
  formData.append('photo', file);
  formData.append('first_name', 'Updated');
  // ... other fields

  const response = await fetch(`/api/students/${studentId}/`, {
    method: 'PATCH',
    headers: {
      'Authorization': `Token ${token}`,
    },
    body: formData
  });

  return response.json();
}
```

### Real-time Notifications

```javascript
// Poll for unread notifications
async function checkNotifications() {
  const response = await api.get('/notifications/unread/');
  const notifications = response.data;
  
  if (notifications.length > 0) {
    // Display notifications
    notifications.forEach(notif => {
      showNotification(notif.title, notif.message);
    });
    
    // Mark as read
    for (const notif of notifications) {
      await api.post(`/notifications/${notif.id}/mark_read/`);
    }
  }
}

// Check every 30 seconds
setInterval(checkNotifications, 30000);
```

## 🎯 Complete Application Example

### Dashboard Page

```javascript
import React, { useState, useEffect } from 'react';
import api from './api';

function Dashboard() {
  const [stats, setStats] = useState(null);
  const [attendance, setAttendance] = useState(null);
  const [notifications, setNotifications] = useState([]);

  useEffect(() => {
    loadDashboard();
  }, []);

  const loadDashboard = async () => {
    try {
      const [statsData, attendanceData, notifData] = await Promise.all([
        api.getDashboard(),
        api.get('/dashboard/attendance_today/'),
        api.get('/notifications/unread/')
      ]);

      setStats(statsData);
      setAttendance(attendanceData);
      setNotifications(notifData.data);
    } catch (error) {
      console.error('Error loading dashboard:', error);
    }
  };

  if (!stats) return <div>Loading...</div>;

  return (
    <div className="dashboard">
      <h1>School Dashboard</h1>
      
      <div className="stats-grid">
        <div className="stat-card">
          <h3>Students</h3>
          <p>{stats.total_students}</p>
        </div>
        <div className="stat-card">
          <h3>Teachers</h3>
          <p>{stats.total_teachers}</p>
        </div>
        <div className="stat-card">
          <h3>Classrooms</h3>
          <p>{stats.total_classrooms}</p>
        </div>
      </div>

      <div className="attendance-section">
        <h2>Today's Attendance</h2>
        <div>
          <h3>Students</h3>
          <p>Present: {attendance?.students.present}</p>
          <p>Absent: {attendance?.students.absent}</p>
          <p>Late: {attendance?.students.late}</p>
        </div>
      </div>

      <div className="notifications-section">
        <h2>Notifications ({notifications.length})</h2>
        <ul>
          {notifications.map(notif => (
            <li key={notif.id}>{notif.title}</li>
          ))}
        </ul>
      </div>
    </div>
  );
}

export default Dashboard;
```

This comprehensive documentation and examples should help you integrate the REST API into any frontend or mobile application!
