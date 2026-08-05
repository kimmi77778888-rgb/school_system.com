from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import (
    CustomAuthToken, UserViewSet, UserProfileViewSet, LoginHistoryViewSet,
    AcademicYearViewSet, GradeViewSet, TeacherViewSet, TeacherDocumentViewSet,
    TeacherEmploymentHistoryViewSet, TeacherAttendanceViewSet, ClassroomViewSet,
    StudentViewSet, StudentHistoryViewSet, SubjectViewSet, TimeSlotViewSet, TimetableViewSet,
    AttendanceViewSet, ExamTypeViewSet, ExamViewSet, ScoreViewSet,
    NotificationViewSet, ReportCardViewSet, SchoolEventViewSet,
    SchoolSettingsViewSet, DashboardViewSet
)

# Create a router and register viewsets
router = DefaultRouter()

# User & Authentication
router.register(r'users', UserViewSet, basename='user')
router.register(r'user-profiles', UserProfileViewSet, basename='userprofile')
router.register(r'login-history', LoginHistoryViewSet, basename='loginhistory')

# Academic Structure
router.register(r'academic-years', AcademicYearViewSet, basename='academicyear')
router.register(r'grades', GradeViewSet, basename='grade')

# Teachers
router.register(r'teachers', TeacherViewSet, basename='teacher')
router.register(r'teacher-documents', TeacherDocumentViewSet, basename='teacherdocument')
router.register(r'teacher-employment-history', TeacherEmploymentHistoryViewSet, basename='teacheremploymenthistory')
router.register(r'teacher-attendance', TeacherAttendanceViewSet, basename='teacherattendance')

# Students & Classrooms
router.register(r'students', StudentViewSet, basename='student')
router.register(r'student-history', StudentHistoryViewSet, basename='studenthistory')
router.register(r'classrooms', ClassroomViewSet, basename='classroom')

# Subjects & Timetable
router.register(r'subjects', SubjectViewSet, basename='subject')
router.register(r'timeslots', TimeSlotViewSet, basename='timeslot')
router.register(r'timetables', TimetableViewSet, basename='timetable')

# Attendance
router.register(r'attendance', AttendanceViewSet, basename='attendance')

# Exams & Scores
router.register(r'exam-types', ExamTypeViewSet, basename='examtype')
router.register(r'exams', ExamViewSet, basename='exam')
router.register(r'scores', ScoreViewSet, basename='score')

# Notifications
router.register(r'notifications', NotificationViewSet, basename='notification')

# Report Cards
router.register(r'report-cards', ReportCardViewSet, basename='reportcard')

# School Events
router.register(r'school-events', SchoolEventViewSet, basename='schoolevent')

# School Settings
router.register(r'school-settings', SchoolSettingsViewSet, basename='schoolsettings')

# Dashboard
router.register(r'dashboard', DashboardViewSet, basename='dashboard')

# URL patterns
urlpatterns = [
    # Authentication endpoint
    path('auth/login/', CustomAuthToken.as_view(), name='api-token-auth'),
    
    # Include router URLs
    path('', include(router.urls)),
]
