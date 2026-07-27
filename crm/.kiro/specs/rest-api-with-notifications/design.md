# Design Document: REST API with Notifications

## Overview

This design document specifies the technical architecture for adding a comprehensive REST API to the existing Django school management system. The API will expose CRUD operations for all core entities (Students, Teachers, Classrooms, Attendance, Scores, Notifications, etc.) with robust authentication, role-based access control, and mobile app support.

### Feature Summary

The REST API will be built using Django REST Framework (DRF) 3.14+ and will provide:

- **Token-based authentication** (JWT or DRF Token Authentication)
- **Role-based access control** (Admin, Teacher, Parent, Student)
- **Complete CRUD endpoints** for 14+ model types
- **Advanced filtering, pagination, and search**
- **API documentation** (Swagger/OpenAPI)
- **Rate limiting and security best practices**
- **Mobile-optimized responses**
- **Optional SMS notification integration**
- **API versioning** starting with v1

### Technology Stack

- **Backend Framework**: Django 4.x with Django REST Framework 3.14+
- **Authentication**: djangorestframework-simplejwt or DRF TokenAuthentication
- **API Documentation**: drf-spectacular (OpenAPI 3.0)
- **Permissions**: Custom DRF permission classes
- **Rate Limiting**: django-ratelimit or DRF throttling
- **Filtering**: django-filter
- **Testing**: pytest-django with property-based testing
- **CORS**: django-cors-headers for web/mobile clients

### Key Design Principles

1. **Security-first**: All endpoints require authentication except login/registration
2. **Role-based access**: Users can only access data appropriate to their role
3. **RESTful conventions**: Proper HTTP verbs, status codes, and resource naming
4. **Mobile-optimized**: Efficient serialization and caching support
5. **Backward compatibility**: Versioned API to support gradual migration
6. **Comprehensive documentation**: Auto-generated, interactive API docs


## Architecture

### System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     API Clients                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │  Mobile App  │  │   Web App    │  │  Third-Party │     │
│  │  (iOS/Android)│  │  (Frontend)  │  │ Integration  │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└─────────────────────────────────────────────────────────────┘
                           │
                           │ HTTP/HTTPS (JSON)
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                  Django REST Framework API                   │
│  ┌───────────────────────────────────────────────────────┐ │
│  │  URL Router (/api/v1/)                                 │ │
│  └───────────────────────────────────────────────────────┘ │
│                           │                                  │
│  ┌─────────────┬──────────┴─────────┬───────────────────┐ │
│  │             │                     │                    │ │
│  ▼             ▼                     ▼                    ▼ │
│ ┌────────┐ ┌──────────┐  ┌─────────────────┐  ┌──────────┐│
│ │ Auth   │ │ Rate     │  │ Permission       │  │ Throttle ││
│ │ Midlwr │ │ Limiting │  │ Classes          │  │ Classes  ││
│ └────────┘ └──────────┘  └─────────────────┘  └──────────┘│
│                           │                                  │
│  ┌───────────────────────┴────────────────────────────┐   │
│  │             ViewSets & Serializers                  │   │
│  │  ┌──────────┬───────────┬────────────┬──────────┐ │   │
│  │  │ Student  │ Teacher   │ Classroom  │ Score    │ │   │
│  │  │ ViewSet  │ ViewSet   │ ViewSet    │ ViewSet  │ │   │
│  │  └──────────┴───────────┴────────────┴──────────┘ │   │
│  │  ┌──────────┬───────────┬────────────┬──────────┐ │   │
│  │  │ Attendnc │ Notifctn  │ Subject    │ Grade    │ │   │
│  │  │ ViewSet  │ ViewSet   │ ViewSet    │ ViewSet  │ │   │
│  │  └──────────┴───────────┴────────────┴──────────┘ │   │
│  └────────────────────────────────────────────────────┘   │
│                           │                                  │
└───────────────────────────┼──────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                  Django ORM Layer                            │
│  ┌───────────────────────────────────────────────────────┐ │
│  │  Django Models (Student, Teacher, Classroom, etc.)     │ │
│  └───────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│              Database (PostgreSQL / SQLite)                  │
└─────────────────────────────────────────────────────────────┘

     ┌──────────────────────────────────────┐
     │  Optional: SMS Service Integration    │
     │  (Twilio, AWS SNS, Africa's Talking) │
     └──────────────────────────────────────┘
```


### Request Flow

1. **Client sends HTTP request** → `/api/v1/students/` with auth token
2. **CORS middleware** → Validates origin for web/mobile clients
3. **Authentication** → Verifies token (JWT or DRF Token)
4. **Rate limiting** → Checks request count against limits
5. **URL routing** → Maps to appropriate ViewSet
6. **Permission check** → Validates role-based access
7. **ViewSet method** → Executes list/retrieve/create/update/delete
8. **Serializer** → Validates input or prepares output
9. **ORM query** → Filtered by permissions (e.g., teacher sees only their classes)
10. **Response** → JSON with appropriate status code
11. **Logging** → Records authentication attempts and errors

### Authentication Flow

```
┌──────────┐                                    ┌──────────┐
│  Client  │                                    │   API    │
└─────┬────┘                                    └────┬─────┘
      │                                              │
      │  POST /api/v1/auth/login/                   │
      │  { username, password }                     │
      ├─────────────────────────────────────────────>│
      │                                              │
      │                                              │ Validate
      │                                              │ Credentials
      │                                              │
      │  200 OK                                      │
      │  { token, user, role, ... }                 │
      │<─────────────────────────────────────────────┤
      │                                              │
      │  GET /api/v1/students/                      │
      │  Authorization: Token <token>               │
      ├─────────────────────────────────────────────>│
      │                                              │
      │                                              │ Verify Token
      │                                              │ Check Permissions
      │                                              │ Filter by Role
      │                                              │
      │  200 OK                                      │
      │  { results: [...], count, next, previous }  │
      │<─────────────────────────────────────────────┤
```


## Components and Interfaces

### Core Components

#### 1. Authentication System

**Component**: `TokenAuthenticationBackend`

**Responsibilities**:
- Validate user credentials (username/password)
- Generate authentication tokens (JWT or DRF Token)
- Refresh expired tokens
- Invalidate tokens on logout
- Track authentication attempts

**Interfaces**:
- `POST /api/v1/auth/login/` → Returns auth token
- `POST /api/v1/auth/logout/` → Invalidates token
- `POST /api/v1/auth/refresh/` → Refreshes JWT token (if using JWT)
- `POST /api/v1/auth/register/` → Creates new user account (optional)

**Implementation Strategy**:
- Use `djangorestframework-simplejwt` for JWT tokens (recommended)
- OR use DRF's built-in `TokenAuthentication` for simpler setup
- Token expiry: Access tokens expire after 60 minutes, refresh tokens after 7 days
- Store tokens securely (HTTP-only cookies or secure local storage on mobile)

#### 2. Permission Classes

**Component**: `RoleBasedPermission`

**Responsibilities**:
- Verify user has required role for endpoint access
- Filter querysets based on user role and associations
- Enforce ownership for parent/student data access

**Permission Matrix**:

| Role    | Students | Teachers | Classrooms | Attendance | Scores | Notifications |
|---------|----------|----------|------------|------------|--------|---------------|
| Admin   | CRUD     | CRUD     | CRUD       | CRUD       | CRUD   | CRUD          |
| Teacher | R (own)  | R (all)  | R (own)    | CRU (own)  | CRU    | R (relevant)  |
| Parent  | R (child)| R (all)  | R (child)  | R (child)  | R      | R (relevant)  |
| Student | R (self) | R (all)  | R (own)    | R (self)   | R      | R (relevant)  |

*CRUD = Create, Read, Update, Delete; R = Read only; (own) = own classes; (child) = linked child*

**Custom Permission Classes**:

```python
class IsAdminUser(BasePermission)
class IsTeacherOrAdmin(BasePermission)
class IsOwnerOrAdmin(BasePermission)
class CanAccessStudentData(BasePermission)  # Parent or student access
```


#### 3. ViewSets

**Component**: DRF `ModelViewSet` or `ReadOnlyModelViewSet`

**Key ViewSets**:

1. **StudentViewSet**
   - Path: `/api/v1/students/`
   - Filters: classroom, gender, is_active, search (name, student_id)
   - Role filtering: Teachers see only their classroom students
   - Methods: list, retrieve, create (admin), update (admin), partial_update (admin), destroy (admin - soft delete)

2. **TeacherViewSet**
   - Path: `/api/v1/teachers/`
   - Filters: subject_specialty, is_active, search (name)
   - Methods: list, retrieve, create (admin), update (admin), destroy (admin)

3. **ClassroomViewSet**
   - Path: `/api/v1/classrooms/`
   - Nested route: `/api/v1/classrooms/{id}/students/`
   - Role filtering: Teachers see only their assigned classrooms
   - Methods: list, retrieve, create (admin), update (admin), destroy (admin)

4. **AttendanceViewSet**
   - Path: `/api/v1/attendance/`
   - Filters: student, date, date_from, date_to, status
   - Custom action: `POST /api/v1/attendance/bulk/` for batch creation
   - Role filtering: Parents/students see only linked student data
   - Methods: list, retrieve, create (teacher/admin), update (teacher/admin)

5. **ScoreViewSet**
   - Path: `/api/v1/scores/`
   - Filters: student, subject, exam_type, academic_year
   - Computed fields: percentage, grade_letter (from model methods)
   - Role filtering: Parents/students see only linked student scores
   - Methods: list, retrieve, create (teacher/admin), update (teacher/admin), destroy (admin)

6. **NotificationViewSet**
   - Path: `/api/v1/notifications/`
   - Filters: notification_type, audience, created_at (date range)
   - Custom action: `POST /api/v1/notifications/{id}/mark_read/`
   - Role filtering: Users see only notifications matching their role
   - Methods: list, retrieve, create (admin), update (admin), destroy (admin - soft delete)

7. **SubjectViewSet**, **GradeViewSet**, **AcademicYearViewSet**
   - Reference data endpoints
   - Custom action: `/api/v1/academic-years/active/` returns current year
   - Mostly read-only except for admin

8. **TimetableViewSet**, **SchoolEventViewSet**
   - Schedule and calendar endpoints
   - Filtered by classroom and academic year
   - Role-based access (students see only their classroom timetable)

9. **ReportCardViewSet**
   - Path: `/api/v1/report-cards/`
   - Filters: student, academic_year, term, status
   - Custom action: `POST /api/v1/report-cards/{id}/publish/` (admin only)
   - Role filtering: Parents/students see only linked student reports


#### 4. Serializers

**Component**: DRF `ModelSerializer`

**Serializer Design Patterns**:

1. **Nested Serializers**: For related objects (e.g., Student includes classroom details)
2. **Read/Write Separation**: Use different serializers for input vs output when needed
3. **Dynamic Fields**: Support `?fields=` query param to reduce payload size
4. **Computed Fields**: Include percentage, grade_letter from model methods
5. **Validation**: Field-level and object-level validation

**Key Serializers**:

```python
# Example structure (pseudocode)
class StudentSerializer(ModelSerializer):
    classroom = ClassroomSerializer(read_only=True)
    classroom_id = PrimaryKeyRelatedField(write_only=True)
    age = SerializerMethodField()  # Computed from date_of_birth
    
    class Meta:
        model = Student
        fields = [
            'id', 'student_id', 'first_name', 'last_name',
            'first_name_en', 'last_name_en', 'gender', 'date_of_birth',
            'age', 'phone', 'parent_name', 'parent_phone',
            'classroom', 'classroom_id', 'photo', 'is_active'
        ]
        read_only_fields = ['student_id', 'age']

class AttendanceSerializer(ModelSerializer):
    student_name = ReadOnlyField(source='student.first_name')
    
    class Meta:
        model = Attendance
        fields = ['id', 'student', 'student_name', 'date', 'status', 'note']
        
    def validate(self, data):
        # Prevent duplicate attendance for same student/date
        if Attendance.objects.filter(
            student=data['student'],
            date=data['date']
        ).exists():
            raise ValidationError("Attendance already recorded")
        return data

class ScoreSerializer(ModelSerializer):
    percentage = ReadOnlyField()  # From model method
    grade_letter = ReadOnlyField()  # From model method
    
    class Meta:
        model = Score
        fields = [
            'id', 'student', 'subject', 'exam_type', 'exam',
            'score', 'max_score', 'percentage', 'grade_letter',
            'date_recorded', 'remarks'
        ]
```


#### 5. Filtering and Pagination

**Component**: `django-filter` + DRF pagination

**Pagination Configuration**:
- Default page size: 20 records
- Max page size: 100 records
- Pagination style: `PageNumberPagination`
- Response format:
```json
{
  "count": 150,
  "next": "http://api.example.com/api/v1/students/?page=3",
  "previous": "http://api.example.com/api/v1/students/?page=1",
  "results": [...]
}
```

**Filtering Strategy**:
- Use `django-filter` for declarative filtering
- Support field filters: `?classroom=5&is_active=true`
- Support date range filters: `?date_from=2024-01-01&date_to=2024-12-31`
- Support search: `?search=John` (searches across multiple fields)
- Support ordering: `?ordering=-date_recorded` (descending by date)

**Filter Examples**:
```python
class StudentFilter(FilterSet):
    classroom = NumberFilter(field_name='classroom__id')
    gender = ChoiceFilter(choices=Student.GENDER_CHOICES)
    is_active = BooleanFilter()
    search = CharFilter(method='filter_search')
    
    def filter_search(self, queryset, name, value):
        return queryset.filter(
            Q(first_name__icontains=value) |
            Q(last_name__icontains=value) |
            Q(student_id__icontains=value)
        )
    
    class Meta:
        model = Student
        fields = ['classroom', 'gender', 'is_active']
```

#### 6. Rate Limiting

**Component**: DRF Throttling Classes

**Rate Limits**:
- **Unauthenticated users**: 100 requests/hour per IP
- **Authenticated users**: 1000 requests/hour per user
- **Read operations**: Higher limits (current: 1000/hour)
- **Write operations**: Lower limits (300/hour)

**Implementation**:
```python
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle

class BurstRateThrottle(UserRateThrottle):
    scope = 'burst'
    rate = '60/min'  # For burst protection

class SustainedRateThrottle(UserRateThrottle):
    scope = 'sustained'
    rate = '1000/hour'

# Applied in settings:
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES': [
        'api.throttles.BurstRateThrottle',
        'api.throttles.SustainedRateThrottle',
    ],
}
```

**Response Headers**:
- `X-RateLimit-Limit`: Total allowed requests
- `X-RateLimit-Remaining`: Requests remaining
- `X-RateLimit-Reset`: Timestamp when limit resets
- `Retry-After`: Seconds until next allowed request (when throttled)


#### 7. SMS Notification Service (Optional)

**Component**: `SMSNotificationService`

**Responsibilities**:
- Queue SMS messages for delivery
- Integrate with SMS gateway (Twilio, AWS SNS, Africa's Talking)
- Retry failed deliveries (max 3 attempts)
- Log delivery status
- Format messages using templates

**SMS Gateway Integration**:

Choice of provider based on requirements:
- **Twilio**: Global coverage, reliable, moderate cost
- **AWS SNS**: AWS-integrated, good for existing AWS deployments
- **Africa's Talking**: Cost-effective for African markets

**Implementation Design**:

```python
class SMSService:
    def __init__(self, provider='twilio'):
        self.provider = self.get_provider(provider)
    
    def send_sms(self, phone_number, message, notification_id=None):
        """Queue SMS for delivery"""
        sms_log = SMSLog.objects.create(
            notification_id=notification_id,
            recipient=phone_number,
            message=message,
            status='pending'
        )
        # Queue using Celery or Django-Q
        send_sms_task.delay(sms_log.id)
    
    def format_message(self, template_name, context):
        """Format SMS using template"""
        template = SMSTemplate.objects.get(name=template_name)
        return template.content.format(**context)
```

**SMS Templates**:
- Attendance alert: "Dear {parent_name}, {student_name} was absent on {date}."
- Exam reminder: "{student_name} has {exam_name} on {date} at {time}."
- General announcement: "{title}: {message}"

**Endpoint**:
- `POST /api/v1/notifications/send-sms/` (Admin only)
- `GET /api/v1/sms-logs/` (Admin only - view delivery history)

**Data Model**:
```python
class SMSLog(models.Model):
    notification = ForeignKey(Notification, null=True, blank=True)
    recipient = CharField(max_length=20)
    message = TextField()
    status = CharField(choices=[
        ('pending', 'Pending'),
        ('sent', 'Sent'),
        ('failed', 'Failed'),
        ('delivered', 'Delivered')
    ])
    attempts = PositiveIntegerField(default=0)
    sent_at = DateTimeField(null=True)
    delivered_at = DateTimeField(null=True)
    error_message = TextField(blank=True)
```


#### 8. API Documentation

**Component**: `drf-spectacular` (OpenAPI 3.0)

**Documentation Features**:
- Auto-generated from code (serializers, viewsets, docstrings)
- Interactive testing via Swagger UI
- Alternative ReDoc interface
- Includes authentication instructions
- Shows request/response schemas
- Provides example requests

**Endpoints**:
- `/api/v1/docs/` - Swagger UI (interactive)
- `/api/v1/redoc/` - ReDoc (clean, readable)
- `/api/v1/schema/` - OpenAPI JSON schema

**Configuration**:
```python
SPECTACULAR_SETTINGS = {
    'TITLE': 'School Management API',
    'DESCRIPTION': 'REST API for School Management System',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'COMPONENT_SPLIT_REQUEST': True,
    'SCHEMA_PATH_PREFIX': r'/api/v[0-9]',
}
```

**Documentation Best Practices**:
- Add docstrings to ViewSets describing purpose
- Use `@extend_schema` decorator for custom actions
- Document query parameters with type hints
- Include error response examples
- Add authentication examples in docs


## Data Models

The REST API will use the existing Django models with minimal modifications. Key models:

### Existing Models (No Changes Required)

All existing models from `school/models.py` will be exposed via the API:

1. **UserProfile**: Links User to role (admin/teacher/parent/student) and related models
2. **AcademicYear**: Academic year with is_active flag
3. **Grade**: Grade levels with optional section
4. **Teacher**: Teacher information with auto-generated teacher_id
5. **Classroom**: Classroom with grade, homeroom teacher, academic year
6. **Student**: Student information with auto-generated student_id, linked to classroom
7. **Subject**: Subject with teacher, grade, credit hours
8. **TimeSlot**: Day and time period for timetable
9. **Timetable**: Schedule entry linking classroom, subject, teacher, time slot
10. **Attendance**: Daily attendance status (P/A/L/E) with unique constraint on (student, date)
11. **ExamType**: Exam category (midterm, final, quiz, etc.)
12. **Exam**: Specific exam instance with subject, classroom, date
13. **Score**: Student score with computed percentage() and grade_letter() methods
14. **TeacherAttendance**: Teacher attendance tracking
15. **Notification**: System notifications with audience targeting
16. **NotificationRead**: Tracks which users have read notifications
17. **ReportCard**: Academic report cards with term, status, remarks
18. **SchoolEvent**: School calendar events
19. **SchoolSettings**: Branding and configuration

### New Models for API

#### 1. SMSLog (Optional - for SMS feature)

```python
class SMSLog(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('sent', 'Sent'),
        ('failed', 'Failed'),
        ('delivered', 'Delivered'),
    ]
    
    sms_id = models.CharField(max_length=20, unique=True, blank=True)
    notification = models.ForeignKey(
        Notification, on_delete=models.SET_NULL, 
        null=True, blank=True, related_name='sms_logs'
    )
    recipient = models.CharField(max_length=20)
    message = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    attempts = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    sent_at = models.DateTimeField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)
    error_message = models.TextField(blank=True)
    gateway_response = models.JSONField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.recipient} - {self.status}"
    
    class Meta:
        ordering = ['-created_at']
```

#### 2. DeviceRegistration (for future push notifications)

```python
class DeviceRegistration(models.Model):
    PLATFORM_CHOICES = [
        ('ios', 'iOS'),
        ('android', 'Android'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='devices')
    device_token = models.CharField(max_length=255, unique=True)
    platform = models.CharField(max_length=10, choices=PLATFORM_CHOICES)
    is_active = models.BooleanField(default=True)
    registered_at = models.DateTimeField(auto_now_add=True)
    last_active = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.platform}"
    
    class Meta:
        unique_together = ('user', 'device_token')
```


### Model Modifications

#### Attendance Model - Add Unique Constraint Handling

The existing model has `unique_together = ('student', 'date')`. The API will:
- Check for existing record before creating
- Update existing record if duplicate is submitted (Requirement 7.10)
- Return appropriate error if update is not allowed

#### Notification Model - Read Tracking

The existing `NotificationRead` model tracks which users have read notifications.

API endpoint `/api/v1/notifications/{id}/mark_read/` will:
- Create `NotificationRead` entry if not exists
- Return 200 if already marked read (idempotent)

### Data Relationships

```
User (Django auth)
  ├── UserProfile (role: admin/teacher/parent/student)
  │     ├── teacher → Teacher (if role=teacher)
  │     └── student → Student (if role=parent or student)
  │
Student
  ├── classroom → Classroom
  ├── attendances → Attendance[]
  ├── scores → Score[]
  ├── report_cards → ReportCard[]
  └── notifications → Notification[] (when student field is set)

Teacher
  ├── homeroom_classes → Classroom[]
  ├── subjects → Subject[]
  ├── timetables → Timetable[]
  └── attendances → TeacherAttendance[]

Classroom
  ├── grade → Grade
  ├── homeroom_teacher → Teacher
  ├── academic_year → AcademicYear
  ├── students → Student[]
  ├── timetables → Timetable[]
  └── exams → Exam[]

Score
  ├── student → Student
  ├── subject → Subject
  ├── exam_type → ExamType
  ├── exam → Exam
  └── academic_year → AcademicYear
```

