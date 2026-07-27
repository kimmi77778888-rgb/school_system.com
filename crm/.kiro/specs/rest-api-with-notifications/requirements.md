# Requirements Document

## Introduction

This document specifies requirements for adding a REST API to the existing Django school management system. The API will expose CRUD operations for core entities (Students, Teachers, Classrooms, Grades, Subjects, Attendance, Scores, Notifications, etc.) with role-based access control. Optional SMS notification capability and mobile app support are included as future enhancements.

## Glossary

- **REST_API**: The Django REST Framework-based API system providing HTTP endpoints for data access and manipulation
- **API_Client**: Any application or service consuming the REST API (web app, mobile app, third-party integrations)
- **Authentication_Token**: A secure token (JWT or DRF Token) used to authenticate API requests
- **SMS_Service**: External SMS gateway service for sending text messages to students, parents, and teachers
- **Mobile_App**: Mobile application (iOS/Android) that consumes the REST API
- **Admin_User**: User with admin role who can perform all operations
- **Teacher_User**: User with teacher role who can view and manage their classes
- **Parent_User**: User with parent role who can view their child's information
- **Student_User**: User with student role who can view their own information
- **Rate_Limiter**: Component that restricts the number of API requests per time period
- **Serializer**: Component that converts Django model instances to/from JSON
- **ViewSet**: Django REST Framework component that handles CRUD operations for a model
- **Permission_Class**: Component that enforces role-based access control
- **Pagination_System**: Component that divides large result sets into pages
- **Filter_Backend**: Component that allows filtering and searching API results
- **SMS_Template**: Pre-defined message format for SMS notifications
- **Notification_Queue**: System for queuing and processing notification delivery
- **API_Response**: HTTP response containing data in JSON format with appropriate status codes

## Requirements

### Requirement 1: REST API Framework Setup

**User Story:** As a developer, I want to set up Django REST Framework, so that I can expose API endpoints for the school management system.

#### Acceptance Criteria

1. THE REST_API SHALL use Django REST Framework version 3.14 or higher
2. THE REST_API SHALL provide endpoints at the base URL path `/api/v1/`
3. THE REST_API SHALL return responses in JSON format with appropriate HTTP status codes
4. THE REST_API SHALL include API documentation accessible at `/api/v1/docs/`
5. WHEN an invalid endpoint is accessed, THE REST_API SHALL return a 404 status code with an error message
6. THE REST_API SHALL include CORS headers configuration for web and mobile clients

### Requirement 2: Authentication and Authorization

**User Story:** As an API client, I want to authenticate with tokens, so that I can securely access protected endpoints.

#### Acceptance Criteria

1. THE REST_API SHALL support token-based authentication using Django REST Framework TokenAuthentication or JWT
2. WHEN valid credentials are provided to `/api/v1/auth/login/`, THE REST_API SHALL return an authentication token
3. WHEN an invalid token is provided, THE REST_API SHALL return a 401 Unauthorized status code
4. WHEN an expired token is provided, THE REST_API SHALL return a 401 Unauthorized status code with an expiration message
5. THE REST_API SHALL provide a logout endpoint at `/api/v1/auth/logout/` that invalidates the token
6. THE REST_API SHALL provide a token refresh endpoint at `/api/v1/auth/refresh/` for JWT tokens
7. WHEN an authenticated request is made, THE REST_API SHALL identify the user from the token

### Requirement 3: Role-Based Access Control

**User Story:** As an administrator, I want API access to be restricted by user role, so that users can only access data they're authorized to see.

#### Acceptance Criteria

1. THE Permission_Class SHALL allow Admin_User to access all API endpoints
2. THE Permission_Class SHALL allow Teacher_User to access student and classroom data for their assigned classes only
3. THE Permission_Class SHALL allow Parent_User to access only their child's student record, attendance, and scores
4. THE Permission_Class SHALL allow Student_User to access only their own student record, attendance, and scores
5. WHEN an unauthorized access attempt is made, THE REST_API SHALL return a 403 Forbidden status code
6. THE Permission_Class SHALL verify role association (teacher linked to Teacher model, parent/student linked to Student model)
7. WHERE a user attempts to access another user's protected resource, THE REST_API SHALL deny access and return a 403 status code

### Requirement 4: Student API Endpoints

**User Story:** As an API client, I want to perform CRUD operations on students, so that I can manage student records programmatically.

#### Acceptance Criteria

1. THE REST_API SHALL provide a GET endpoint `/api/v1/students/` that returns a paginated list of students
2. THE REST_API SHALL provide a GET endpoint `/api/v1/students/{id}/` that returns a single student's details
3. THE REST_API SHALL provide a POST endpoint `/api/v1/students/` that creates a new student (Admin_User only)
4. THE REST_API SHALL provide a PUT/PATCH endpoint `/api/v1/students/{id}/` that updates a student (Admin_User only)
5. THE REST_API SHALL provide a DELETE endpoint `/api/v1/students/{id}/` that soft-deletes a student by setting is_active to False (Admin_User only)
6. THE Serializer SHALL include student_id, first_name, last_name, first_name_en, last_name_en, gender, date_of_birth, classroom, phone, parent_name, parent_phone, photo, and is_active fields
7. WHEN a Teacher_User requests `/api/v1/students/`, THE REST_API SHALL return only students in their assigned classrooms
8. WHEN a Parent_User requests `/api/v1/students/`, THE REST_API SHALL return only their linked child's record
9. THE REST_API SHALL support filtering students by classroom, gender, and is_active status
10. THE REST_API SHALL support searching students by first_name, last_name, and student_id

### Requirement 5: Teacher API Endpoints

**User Story:** As an API client, I want to perform CRUD operations on teachers, so that I can manage teacher records programmatically.

#### Acceptance Criteria

1. THE REST_API SHALL provide a GET endpoint `/api/v1/teachers/` that returns a paginated list of teachers
2. THE REST_API SHALL provide a GET endpoint `/api/v1/teachers/{id}/` that returns a single teacher's details
3. THE REST_API SHALL provide a POST endpoint `/api/v1/teachers/` that creates a new teacher (Admin_User only)
4. THE REST_API SHALL provide a PUT/PATCH endpoint `/api/v1/teachers/{id}/` that updates a teacher (Admin_User only)
5. THE REST_API SHALL provide a DELETE endpoint `/api/v1/teachers/{id}/` that deletes a teacher (Admin_User only)
6. THE Serializer SHALL include teacher_id, first_name, last_name, first_name_en, last_name_en, gender, phone, email, subject_specialty, hire_date, photo, qualification, and is_active fields
7. THE REST_API SHALL support filtering teachers by subject_specialty and is_active status
8. THE REST_API SHALL support searching teachers by first_name, last_name, and subject_specialty

### Requirement 6: Classroom API Endpoints

**User Story:** As an API client, I want to access classroom information, so that I can view class assignments and rosters.

#### Acceptance Criteria

1. THE REST_API SHALL provide a GET endpoint `/api/v1/classrooms/` that returns a paginated list of classrooms
2. THE REST_API SHALL provide a GET endpoint `/api/v1/classrooms/{id}/` that returns a single classroom's details
3. THE REST_API SHALL provide a POST endpoint `/api/v1/classrooms/` that creates a new classroom (Admin_User only)
4. THE REST_API SHALL provide a PUT/PATCH endpoint `/api/v1/classrooms/{id}/` that updates a classroom (Admin_User only)
5. THE REST_API SHALL provide a DELETE endpoint `/api/v1/classrooms/{id}/` that deletes a classroom (Admin_User only)
6. THE Serializer SHALL include classroom_id, grade, homeroom_teacher, academic_year, room_number, capacity, and student_count fields
7. THE REST_API SHALL provide a nested endpoint `/api/v1/classrooms/{id}/students/` that returns all students in that classroom
8. WHEN a Teacher_User requests `/api/v1/classrooms/`, THE REST_API SHALL return only classrooms where they are the homeroom_teacher

### Requirement 7: Attendance API Endpoints

**User Story:** As an API client, I want to record and retrieve attendance data, so that I can track student presence programmatically.

#### Acceptance Criteria

1. THE REST_API SHALL provide a GET endpoint `/api/v1/attendance/` that returns paginated attendance records
2. THE REST_API SHALL provide a GET endpoint `/api/v1/attendance/{id}/` that returns a single attendance record
3. THE REST_API SHALL provide a POST endpoint `/api/v1/attendance/` that creates a new attendance record (Admin_User and Teacher_User only)
4. THE REST_API SHALL provide a POST endpoint `/api/v1/attendance/bulk/` that creates multiple attendance records at once (Admin_User and Teacher_User only)
5. THE REST_API SHALL provide a PUT/PATCH endpoint `/api/v1/attendance/{id}/` that updates an attendance record (Admin_User and Teacher_User only)
6. THE Serializer SHALL include student, date, status (P/A/L/E), and note fields
7. THE REST_API SHALL support filtering attendance by student, date, date range, and status
8. WHEN a Teacher_User submits attendance, THE REST_API SHALL verify the student belongs to their assigned classroom
9. WHEN a Parent_User or Student_User requests attendance, THE REST_API SHALL return only records for the linked student
10. WHEN duplicate attendance is submitted for the same student and date, THE REST_API SHALL update the existing record instead of creating a duplicate

### Requirement 8: Score and Exam API Endpoints

**User Story:** As an API client, I want to record and retrieve exam scores, so that I can manage academic performance data programmatically.

#### Acceptance Criteria

1. THE REST_API SHALL provide a GET endpoint `/api/v1/scores/` that returns paginated score records
2. THE REST_API SHALL provide a GET endpoint `/api/v1/scores/{id}/` that returns a single score record
3. THE REST_API SHALL provide a POST endpoint `/api/v1/scores/` that creates a new score (Admin_User and Teacher_User only)
4. THE REST_API SHALL provide a PUT/PATCH endpoint `/api/v1/scores/{id}/` that updates a score (Admin_User and Teacher_User only)
5. THE REST_API SHALL provide a DELETE endpoint `/api/v1/scores/{id}/` that deletes a score (Admin_User only)
6. THE Serializer SHALL include student, subject, exam_type, exam, score, max_score, percentage, grade_letter, and date_recorded fields
7. THE Serializer SHALL calculate percentage and grade_letter dynamically based on score and max_score
8. THE REST_API SHALL support filtering scores by student, subject, exam_type, and academic_year
9. WHEN a Teacher_User submits scores, THE REST_API SHALL verify the student belongs to a classroom they teach
10. WHEN a Parent_User or Student_User requests scores, THE REST_API SHALL return only records for the linked student

### Requirement 9: Notification API Endpoints

**User Story:** As an API client, I want to create and retrieve notifications, so that I can send announcements and alerts to users.

#### Acceptance Criteria

1. THE REST_API SHALL provide a GET endpoint `/api/v1/notifications/` that returns paginated notifications
2. THE REST_API SHALL provide a GET endpoint `/api/v1/notifications/{id}/` that returns a single notification
3. THE REST_API SHALL provide a POST endpoint `/api/v1/notifications/` that creates a new notification (Admin_User only)
4. THE REST_API SHALL provide a PUT/PATCH endpoint `/api/v1/notifications/{id}/` that updates a notification (Admin_User only)
5. THE REST_API SHALL provide a DELETE endpoint `/api/v1/notifications/{id}/` that soft-deletes a notification by setting is_active to False (Admin_User only)
6. THE Serializer SHALL include notification_id, title, message, notification_type, audience, created_by, created_at, scheduled_at, classroom, and student fields
7. WHEN a Teacher_User, Parent_User, or Student_User requests `/api/v1/notifications/`, THE REST_API SHALL return only notifications matching their role in the audience field
8. THE REST_API SHALL provide a POST endpoint `/api/v1/notifications/{id}/mark_read/` that marks a notification as read for the authenticated user
9. THE REST_API SHALL support filtering notifications by notification_type, audience, and created_at date range

### Requirement 10: Subject, Grade, and Academic Year API Endpoints

**User Story:** As an API client, I want to access subject, grade, and academic year data, so that I can use reference data in my application.

#### Acceptance Criteria

1. THE REST_API SHALL provide a GET endpoint `/api/v1/subjects/` that returns a paginated list of subjects
2. THE REST_API SHALL provide a GET endpoint `/api/v1/grades/` that returns a list of all grades
3. THE REST_API SHALL provide a GET endpoint `/api/v1/academic-years/` that returns a list of all academic years
4. THE REST_API SHALL provide POST/PUT/DELETE endpoints for subjects, grades, and academic years (Admin_User only)
5. THE Serializer SHALL include all relevant fields for each model
6. THE REST_API SHALL include the active academic year in the response metadata or provide a `/api/v1/academic-years/active/` endpoint

### Requirement 11: Pagination and Filtering

**User Story:** As an API client, I want paginated responses and filtering options, so that I can efficiently retrieve large datasets.

#### Acceptance Criteria

1. THE REST_API SHALL paginate list endpoints with a default page size of 20 records
2. THE REST_API SHALL support query parameter `page_size` to adjust pagination size up to a maximum of 100 records
3. THE REST_API SHALL include pagination metadata in responses: count, next, previous, and current page
4. THE Filter_Backend SHALL support filtering by model-specific fields using query parameters
5. THE Filter_Backend SHALL support date range filtering using query parameters `date_from` and `date_to` for date fields
6. THE Filter_Backend SHALL support search functionality using query parameter `search` for text fields
7. THE Filter_Backend SHALL support ordering results using query parameter `ordering` with field names

### Requirement 12: Error Handling and Validation

**User Story:** As an API client, I want clear error messages, so that I can understand and fix request issues.

#### Acceptance Criteria

1. WHEN validation fails, THE REST_API SHALL return a 400 Bad Request status code with field-specific error messages in JSON format
2. WHEN authentication fails, THE REST_API SHALL return a 401 Unauthorized status code with an error message
3. WHEN authorization fails, THE REST_API SHALL return a 403 Forbidden status code with an error message
4. WHEN a resource is not found, THE REST_API SHALL return a 404 Not Found status code with an error message
5. WHEN a server error occurs, THE REST_API SHALL return a 500 Internal Server Error status code and log the error details
6. THE Serializer SHALL validate required fields, data types, and format constraints
7. THE Serializer SHALL validate foreign key references exist before creating or updating records
8. WHEN invalid JSON is submitted, THE REST_API SHALL return a 400 status code with a parsing error message

### Requirement 13: Rate Limiting

**User Story:** As a system administrator, I want API rate limiting, so that I can prevent abuse and ensure fair usage.

#### Acceptance Criteria

1. THE Rate_Limiter SHALL limit unauthenticated requests to 100 requests per hour per IP address
2. THE Rate_Limiter SHALL limit authenticated requests to 1000 requests per hour per user
3. WHEN the rate limit is exceeded, THE REST_API SHALL return a 429 Too Many Requests status code
4. THE API_Response SHALL include rate limit headers: X-RateLimit-Limit, X-RateLimit-Remaining, and X-RateLimit-Reset
5. THE Rate_Limiter SHALL apply different limits to read operations (higher) and write operations (lower)

### Requirement 14: Mobile App Support

**User Story:** As a mobile app developer, I want mobile-optimized API endpoints, so that I can build iOS and Android applications.

#### Acceptance Criteria

1. THE REST_API SHALL support authentication token storage and refresh for mobile clients
2. THE REST_API SHALL provide compact response formats suitable for mobile bandwidth constraints
3. THE REST_API SHALL support image upload for profile photos with mobile-friendly formats (JPEG, PNG) and size limits
4. THE REST_API SHALL return image URLs in responses that are accessible from mobile apps
5. THE REST_API SHALL support push notification device registration endpoint `/api/v1/devices/` for future push notification integration
6. THE Serializer SHALL include nested relationships with configurable depth to minimize API round trips
7. THE REST_API SHALL support conditional requests using ETag headers to enable client-side caching

### Requirement 15: SMS Notification Integration (Optional)

**User Story:** As an administrator, I want to send SMS notifications, so that I can reach parents and students without requiring app usage.

#### Acceptance Criteria

1. WHERE SMS notifications are enabled, THE SMS_Service SHALL integrate with an external SMS gateway API
2. WHERE SMS notifications are enabled, THE REST_API SHALL provide a POST endpoint `/api/v1/notifications/send-sms/` (Admin_User only)
3. WHERE SMS notifications are enabled, THE SMS_Service SHALL send SMS to parent_phone numbers for notifications with audience "parents"
4. WHERE SMS notifications are enabled, THE SMS_Service SHALL use SMS_Template for common notification types (attendance alerts, exam reminders, announcements)
5. WHERE SMS notifications are enabled, THE SMS_Service SHALL queue messages in the Notification_Queue for batch processing
6. WHERE SMS notifications are enabled, THE SMS_Service SHALL log all sent messages with timestamp, recipient, and delivery status
7. WHERE SMS notifications are enabled, THE SMS_Service SHALL handle delivery failures gracefully and retry up to 3 times
8. WHERE SMS notifications are enabled, THE REST_API SHALL provide a GET endpoint `/api/v1/sms-logs/` to view SMS delivery history (Admin_User only)
9. IF the SMS gateway is unavailable, THEN THE SMS_Service SHALL log an error and continue without blocking the notification creation
10. THE SMS_Service SHALL validate phone numbers are in correct format before sending

### Requirement 16: API Documentation

**User Story:** As an API consumer, I want interactive API documentation, so that I can understand and test endpoints easily.

#### Acceptance Criteria

1. THE REST_API SHALL provide interactive API documentation using Swagger/OpenAPI at `/api/v1/docs/`
2. THE REST_API SHALL provide alternative ReDoc documentation at `/api/v1/redoc/`
3. THE REST_API SHALL document all endpoints with descriptions, parameters, request schemas, and response schemas
4. THE REST_API SHALL include authentication instructions in the documentation
5. THE REST_API SHALL provide example requests and responses for each endpoint
6. THE REST_API SHALL allow testing endpoints directly from the documentation interface (Swagger UI)

### Requirement 17: API Security

**User Story:** As a security administrator, I want secure API practices, so that I can protect sensitive student and teacher data.

#### Acceptance Criteria

1. THE REST_API SHALL enforce HTTPS for all API requests in production environments
2. THE REST_API SHALL validate and sanitize all input data to prevent SQL injection attacks
3. THE REST_API SHALL implement CSRF protection for state-changing operations
4. THE REST_API SHALL not expose sensitive information (passwords, tokens) in API responses or logs
5. THE REST_API SHALL implement secure password hashing for any password-related endpoints
6. THE REST_API SHALL log all authentication attempts (success and failure) with timestamps and IP addresses
7. WHEN multiple failed authentication attempts occur from the same IP, THE REST_API SHALL implement temporary IP blocking

### Requirement 18: Timetable and School Event API Endpoints

**User Story:** As an API client, I want to access timetable and school event data, so that I can display schedules in my application.

#### Acceptance Criteria

1. THE REST_API SHALL provide a GET endpoint `/api/v1/timetables/` that returns timetable entries
2. THE REST_API SHALL provide a GET endpoint `/api/v1/timetables/{classroom_id}/` that returns timetable for a specific classroom
3. THE REST_API SHALL provide a GET endpoint `/api/v1/events/` that returns school events
4. THE Serializer SHALL include time_slot, subject, teacher, classroom, and academic_year for timetable entries
5. THE Serializer SHALL include title, event_type, start_date, end_date, and description for school events
6. THE REST_API SHALL support filtering timetables by classroom, day, and academic_year
7. THE REST_API SHALL support filtering events by event_type and date range
8. WHEN a Student_User or Parent_User requests timetables, THE REST_API SHALL return only the timetable for the linked student's classroom

### Requirement 19: Report Card API Endpoint

**User Story:** As an API client, I want to retrieve report cards, so that I can display academic summaries in my application.

#### Acceptance Criteria

1. THE REST_API SHALL provide a GET endpoint `/api/v1/report-cards/` that returns report cards
2. THE REST_API SHALL provide a GET endpoint `/api/v1/report-cards/{id}/` that returns a single report card with full details
3. THE Serializer SHALL include student, academic_year, term, status, teacher_remarks, principal_remarks, conduct, attendance_days, and absent_days
4. THE REST_API SHALL support filtering report cards by student, academic_year, term, and status
5. WHEN a Parent_User or Student_User requests report cards, THE REST_API SHALL return only report cards for the linked student
6. THE REST_API SHALL provide a POST endpoint `/api/v1/report-cards/{id}/publish/` that changes status from draft to published (Admin_User only)

### Requirement 20: API Versioning and Deprecation

**User Story:** As an API consumer, I want API versioning support, so that my application continues working when the API evolves.

#### Acceptance Criteria

1. THE REST_API SHALL use URL path versioning with the current version being `v1`
2. THE REST_API SHALL maintain backward compatibility within a major version
3. WHEN breaking changes are needed, THE REST_API SHALL create a new major version (e.g., `v2`)
4. THE REST_API SHALL provide deprecation warnings in response headers for endpoints scheduled for removal
5. THE REST_API SHALL maintain deprecated endpoints for at least 6 months after deprecation notice
6. THE REST_API SHALL document version history and migration guides in the API documentation
