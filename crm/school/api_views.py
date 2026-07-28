from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.models import User
from django.db.models import Q, Count, Avg
from datetime import date, timedelta

from .models import (
    UserProfile, LoginHistory, AcademicYear, Grade, Teacher, TeacherDocument,
    TeacherEmploymentHistory, Classroom, Student, Subject, TimeSlot, Timetable,
    Attendance, TeacherAttendance, ExamType, Exam, Score, Notification,
    NotificationRead, ReportCard, SchoolEvent, SchoolSettings
)
from .serializers import (
    UserSerializer, UserProfileSerializer, LoginHistorySerializer,
    AcademicYearSerializer, GradeSerializer, TeacherSerializer, TeacherListSerializer,
    TeacherDocumentSerializer, TeacherEmploymentHistorySerializer,
    ClassroomSerializer, StudentSerializer, StudentListSerializer,
    SubjectSerializer, TimeSlotSerializer, TimetableSerializer,
    AttendanceSerializer, TeacherAttendanceSerializer, ExamTypeSerializer,
    ExamSerializer, ScoreSerializer, NotificationSerializer,
    NotificationReadSerializer, ReportCardSerializer, SchoolEventSerializer,
    SchoolSettingsSerializer
)


# ══════════════════════════════════════════════════════
#  CUSTOM AUTHENTICATION
# ══════════════════════════════════════════════════════
class CustomAuthToken(ObtainAuthToken):
    """
    Custom token authentication with user profile information
    """
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        
        # Get or create user profile
        profile, _ = UserProfile.objects.get_or_create(user=user)
        
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'username': user.username,
            'email': user.email,
            'role': profile.role,
            'first_name': user.first_name,
            'last_name': user.last_name,
        })


# ══════════════════════════════════════════════════════
#  USER VIEWSETS
# ══════════════════════════════════════════════════════
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['username', 'email', 'first_name', 'last_name']
    ordering_fields = ['username', 'date_joined']
    ordering = ['-date_joined']

    @action(detail=False, methods=['get'])
    def me(self, request):
        """Get current user information"""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def change_password(self, request):
        """Change user password"""
        user = request.user
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')
        
        if not user.check_password(old_password):
            return Response({'error': 'Invalid old password'}, status=status.HTTP_400_BAD_REQUEST)
        
        user.set_password(new_password)
        user.save()
        return Response({'message': 'Password changed successfully'})


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.select_related('user', 'teacher', 'student').all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['role', 'user']
    search_fields = ['user__username', 'user__email', 'phone']

    @action(detail=False, methods=['get'])
    def my_profile(self, request):
        """Get current user's profile"""
        profile, _ = UserProfile.objects.get_or_create(user=request.user)
        serializer = self.get_serializer(profile)
        return Response(serializer.data)


class LoginHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = LoginHistory.objects.select_related('user').all()
    serializer_class = LoginHistorySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['user', 'device_type', 'is_suspicious']
    ordering_fields = ['login_time']
    ordering = ['-login_time']

    def get_queryset(self):
        """Users can only see their own login history unless admin"""
        if self.request.user.is_staff:
            return self.queryset
        return self.queryset.filter(user=self.request.user)


# ══════════════════════════════════════════════════════
#  ACADEMIC STRUCTURE
# ══════════════════════════════════════════════════════
class AcademicYearViewSet(viewsets.ModelViewSet):
    queryset = AcademicYear.objects.all()
    serializer_class = AcademicYearSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['is_active']
    ordering = ['-year']

    @action(detail=False, methods=['get'])
    def active(self, request):
        """Get the current active academic year"""
        active_year = self.queryset.filter(is_active=True).first()
        if active_year:
            serializer = self.get_serializer(active_year)
            return Response(serializer.data)
        return Response({'error': 'No active academic year'}, status=status.HTTP_404_NOT_FOUND)


class GradeViewSet(viewsets.ModelViewSet):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'section']
    ordering = ['name', 'section']


# ══════════════════════════════════════════════════════
#  TEACHER
# ══════════════════════════════════════════════════════
class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['gender', 'is_active', 'teacher_rank', 'subject_specialty']
    search_fields = ['first_name', 'last_name', 'first_name_en', 'last_name_en', 'teacher_id', 'email', 'phone']
    ordering_fields = ['last_name', 'hire_date', 'years_experience']
    ordering = ['last_name', 'first_name']

    def get_serializer_class(self):
        if self.action == 'list':
            return TeacherListSerializer
        return TeacherSerializer

    @action(detail=True, methods=['get'])
    def statistics(self, request, pk=None):
        """Get teacher statistics"""
        teacher = self.get_object()
        data = {
            'total_classes': teacher.homeroom_classes.count(),
            'total_subjects': teacher.subjects.count(),
            'timetable_slots': teacher.timetables.count(),
            'attendance_records': teacher.attendances.count(),
            'years_of_service': teacher.years_experience,
        }
        return Response(data)

    @action(detail=False, methods=['get'])
    def active(self, request):
        """Get all active teachers"""
        active_teachers = self.queryset.filter(is_active=True)
        serializer = self.get_serializer(active_teachers, many=True)
        return Response(serializer.data)


class TeacherDocumentViewSet(viewsets.ModelViewSet):
    queryset = TeacherDocument.objects.select_related('teacher', 'uploaded_by').all()
    serializer_class = TeacherDocumentSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['teacher', 'document_type']
    ordering = ['-uploaded_at']

    def perform_create(self, serializer):
        serializer.save(uploaded_by=self.request.user)


class TeacherEmploymentHistoryViewSet(viewsets.ModelViewSet):
    queryset = TeacherEmploymentHistory.objects.select_related('teacher').all()
    serializer_class = TeacherEmploymentHistorySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['teacher', 'is_current']
    ordering = ['-start_date']


class TeacherAttendanceViewSet(viewsets.ModelViewSet):
    queryset = TeacherAttendance.objects.select_related('teacher').all()
    serializer_class = TeacherAttendanceSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['teacher', 'date', 'status']
    ordering = ['-date']

    @action(detail=False, methods=['get'])
    def today(self, request):
        """Get today's teacher attendance"""
        today_attendance = self.queryset.filter(date=date.today())
        serializer = self.get_serializer(today_attendance, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def summary(self, request):
        """Get attendance summary statistics"""
        teacher_id = request.query_params.get('teacher')
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date', date.today().isoformat())

        queryset = self.queryset
        if teacher_id:
            queryset = queryset.filter(teacher_id=teacher_id)
        if start_date:
            queryset = queryset.filter(date__gte=start_date)
        if end_date:
            queryset = queryset.filter(date__lte=end_date)

        summary = {
            'total_days': queryset.count(),
            'present': queryset.filter(status='P').count(),
            'absent': queryset.filter(status='A').count(),
            'late': queryset.filter(status='L').count(),
            'excused': queryset.filter(status='E').count(),
        }
        return Response(summary)


# ══════════════════════════════════════════════════════
#  STUDENT
# ══════════════════════════════════════════════════════
class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.select_related('classroom', 'classroom__grade').all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['gender', 'is_active', 'classroom', 'classroom__grade']
    search_fields = ['first_name', 'last_name', 'first_name_en', 'last_name_en', 'student_id', 'phone', 'parent_name']
    ordering_fields = ['last_name', 'enrolled_date', 'date_of_birth']
    ordering = ['last_name', 'first_name']

    def get_serializer_class(self):
        if self.action == 'list':
            return StudentListSerializer
        return StudentSerializer

    @action(detail=True, methods=['get'])
    def statistics(self, request, pk=None):
        """Get student statistics"""
        student = self.get_object()
        data = {
            'total_scores': student.scores.count(),
            'average_score': student.scores.aggregate(Avg('score'))['score__avg'],
            'attendance_records': student.attendances.count(),
            'present_days': student.attendances.filter(status='P').count(),
            'absent_days': student.attendances.filter(status='A').count(),
        }
        return Response(data)

    @action(detail=False, methods=['get'])
    def active(self, request):
        """Get all active students"""
        active_students = self.queryset.filter(is_active=True)
        serializer = self.get_serializer(active_students, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def report_card(self, request, pk=None):
        """Get student's report card"""
        student = self.get_object()
        academic_year_id = request.query_params.get('academic_year')
        term = request.query_params.get('term', 'Term 1')

        report_cards = student.report_cards.all()
        if academic_year_id:
            report_cards = report_cards.filter(academic_year_id=academic_year_id)
        if term:
            report_cards = report_cards.filter(term=term)

        serializer = ReportCardSerializer(report_cards, many=True, context={'request': request})
        return Response(serializer.data)


# ══════════════════════════════════════════════════════
#  CLASSROOM
# ══════════════════════════════════════════════════════
class ClassroomViewSet(viewsets.ModelViewSet):
    queryset = Classroom.objects.select_related('grade', 'homeroom_teacher', 'academic_year').all()
    serializer_class = ClassroomSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['grade', 'academic_year', 'homeroom_teacher']
    search_fields = ['classroom_id', 'room_number', 'grade__name']
    ordering = ['grade__name']

    @action(detail=True, methods=['get'])
    def students(self, request, pk=None):
        """Get all students in a classroom"""
        classroom = self.get_object()
        students = classroom.students.all()
        serializer = StudentListSerializer(students, many=True, context={'request': request})
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def timetable(self, request, pk=None):
        """Get classroom timetable"""
        classroom = self.get_object()
        timetable = classroom.timetables.all()
        serializer = TimetableSerializer(timetable, many=True, context={'request': request})
        return Response(serializer.data)


# ══════════════════════════════════════════════════════
#  SUBJECT
# ══════════════════════════════════════════════════════
class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.select_related('teacher', 'grade').all()
    serializer_class = SubjectSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['grade', 'teacher']
    search_fields = ['name', 'code', 'subject_id']
    ordering = ['name']


# ══════════════════════════════════════════════════════
#  TIMETABLE
# ══════════════════════════════════════════════════════
class TimeSlotViewSet(viewsets.ModelViewSet):
    queryset = TimeSlot.objects.all()
    serializer_class = TimeSlotSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['day', 'period']
    ordering = ['day', 'start_time']


class TimetableViewSet(viewsets.ModelViewSet):
    queryset = Timetable.objects.select_related('classroom', 'subject', 'teacher', 'time_slot', 'academic_year').all()
    serializer_class = TimetableSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['classroom', 'subject', 'teacher', 'academic_year', 'time_slot__day']
    ordering = ['time_slot__day', 'time_slot__start_time']


# ══════════════════════════════════════════════════════
#  ATTENDANCE
# ══════════════════════════════════════════════════════
class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.select_related('student').all()
    serializer_class = AttendanceSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['student', 'date', 'status']
    ordering = ['-date']

    @action(detail=False, methods=['get'])
    def today(self, request):
        """Get today's attendance"""
        today_attendance = self.queryset.filter(date=date.today())
        serializer = self.get_serializer(today_attendance, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def summary(self, request):
        """Get attendance summary statistics"""
        student_id = request.query_params.get('student')
        classroom_id = request.query_params.get('classroom')
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date', date.today().isoformat())

        queryset = self.queryset
        if student_id:
            queryset = queryset.filter(student_id=student_id)
        if classroom_id:
            queryset = queryset.filter(student__classroom_id=classroom_id)
        if start_date:
            queryset = queryset.filter(date__gte=start_date)
        if end_date:
            queryset = queryset.filter(date__lte=end_date)

        summary = {
            'total_days': queryset.count(),
            'present': queryset.filter(status='P').count(),
            'absent': queryset.filter(status='A').count(),
            'late': queryset.filter(status='L').count(),
            'excused': queryset.filter(status='E').count(),
        }
        return Response(summary)

    @action(detail=False, methods=['post'])
    def bulk_create(self, request):
        """Bulk create attendance records"""
        attendance_data = request.data.get('attendance', [])
        created = []
        
        for item in attendance_data:
            attendance, created_flag = Attendance.objects.update_or_create(
                student_id=item['student'],
                date=item['date'],
                defaults={
                    'status': item.get('status', 'P'),
                    'note': item.get('note', '')
                }
            )
            created.append(attendance)
        
        serializer = self.get_serializer(created, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# ══════════════════════════════════════════════════════
#  EXAMS & SCORES
# ══════════════════════════════════════════════════════
class ExamTypeViewSet(viewsets.ModelViewSet):
    queryset = ExamType.objects.all()
    serializer_class = ExamTypeSerializer
    permission_classes = [IsAuthenticated]


class ExamViewSet(viewsets.ModelViewSet):
    queryset = Exam.objects.select_related('exam_type', 'subject', 'classroom', 'academic_year').all()
    serializer_class = ExamSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['exam_type', 'subject', 'classroom', 'academic_year']
    search_fields = ['name', 'exam_id']
    ordering = ['-date']


class ScoreViewSet(viewsets.ModelViewSet):
    queryset = Score.objects.select_related('student', 'subject', 'exam_type', 'exam', 'academic_year').all()
    serializer_class = ScoreSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['student', 'subject', 'exam_type', 'exam', 'academic_year']
    ordering = ['-date_recorded']

    @action(detail=False, methods=['get'])
    def student_scores(self, request):
        """Get all scores for a specific student"""
        student_id = request.query_params.get('student_id')
        if not student_id:
            return Response({'error': 'student_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        scores = self.queryset.filter(student_id=student_id)
        serializer = self.get_serializer(scores, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def bulk_create(self, request):
        """Bulk create or update scores"""
        scores_data = request.data.get('scores', [])
        created = []
        
        for item in scores_data:
            score, created_flag = Score.objects.update_or_create(
                student_id=item['student'],
                subject_id=item['subject'],
                exam_type_id=item['exam_type'],
                academic_year_id=item['academic_year'],
                defaults={
                    'score': item['score'],
                    'max_score': item.get('max_score', 100),
                    'exam_id': item.get('exam'),
                    'remarks': item.get('remarks', '')
                }
            )
            created.append(score)
        
        serializer = self.get_serializer(created, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# ══════════════════════════════════════════════════════
#  NOTIFICATIONS
# ══════════════════════════════════════════════════════
class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.select_related('created_by', 'classroom', 'student').all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['notification_type', 'audience', 'is_active', 'classroom', 'student']
    search_fields = ['title', 'message']
    ordering = ['-created_at']

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=['post'])
    def mark_read(self, request, pk=None):
        """Mark notification as read"""
        notification = self.get_object()
        NotificationRead.objects.get_or_create(
            notification=notification,
            user=request.user
        )
        return Response({'status': 'marked as read'})

    @action(detail=False, methods=['get'])
    def unread(self, request):
        """Get unread notifications for current user"""
        user = request.user
        profile = UserProfile.objects.get(user=user)
        
        # Filter by audience
        notifications = self.queryset.filter(is_active=True)
        notifications = notifications.filter(
            Q(audience='all') | Q(audience=profile.role)
        )
        
        # Exclude already read
        read_notification_ids = NotificationRead.objects.filter(user=user).values_list('notification_id', flat=True)
        notifications = notifications.exclude(id__in=read_notification_ids)
        
        serializer = self.get_serializer(notifications, many=True)
        return Response(serializer.data)


# ══════════════════════════════════════════════════════
#  REPORT CARD
# ══════════════════════════════════════════════════════
class ReportCardViewSet(viewsets.ModelViewSet):
    queryset = ReportCard.objects.select_related('student', 'academic_year', 'generated_by').all()
    serializer_class = ReportCardSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['student', 'academic_year', 'term', 'status']
    ordering = ['-generated_at']

    def perform_create(self, serializer):
        serializer.save(generated_by=self.request.user)


# ══════════════════════════════════════════════════════
#  SCHOOL EVENT
# ══════════════════════════════════════════════════════
class SchoolEventViewSet(viewsets.ModelViewSet):
    queryset = SchoolEvent.objects.select_related('created_by').all()
    serializer_class = SchoolEventSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['event_type']
    search_fields = ['title', 'description']
    ordering = ['start_date']

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=False, methods=['get'])
    def upcoming(self, request):
        """Get upcoming events"""
        upcoming_events = self.queryset.filter(start_date__gte=date.today())
        serializer = self.get_serializer(upcoming_events, many=True)
        return Response(serializer.data)


# ══════════════════════════════════════════════════════
#  SCHOOL SETTINGS
# ══════════════════════════════════════════════════════
class SchoolSettingsViewSet(viewsets.ModelViewSet):
    queryset = SchoolSettings.objects.all()
    serializer_class = SchoolSettingsSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def current(self, request):
        """Get current school settings"""
        settings = self.queryset.first()
        if settings:
            serializer = self.get_serializer(settings)
            return Response(serializer.data)
        return Response({'error': 'No school settings found'}, status=status.HTTP_404_NOT_FOUND)


# ══════════════════════════════════════════════════════
#  DASHBOARD & ANALYTICS
# ══════════════════════════════════════════════════════
class DashboardViewSet(viewsets.ViewSet):
    """
    Dashboard statistics and analytics
    """
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def overview(self, request):
        """Get dashboard overview statistics"""
        data = {
            'total_students': Student.objects.filter(is_active=True).count(),
            'total_teachers': Teacher.objects.filter(is_active=True).count(),
            'total_classrooms': Classroom.objects.count(),
            'total_subjects': Subject.objects.count(),
            'active_academic_year': None,
        }
        
        active_year = AcademicYear.objects.filter(is_active=True).first()
        if active_year:
            data['active_academic_year'] = active_year.year
        
        return Response(data)

    @action(detail=False, methods=['get'])
    def attendance_today(self, request):
        """Get today's attendance statistics"""
        today = date.today()
        student_attendance = Attendance.objects.filter(date=today)
        teacher_attendance = TeacherAttendance.objects.filter(date=today)
        
        data = {
            'students': {
                'total': student_attendance.count(),
                'present': student_attendance.filter(status='P').count(),
                'absent': student_attendance.filter(status='A').count(),
                'late': student_attendance.filter(status='L').count(),
                'excused': student_attendance.filter(status='E').count(),
            },
            'teachers': {
                'total': teacher_attendance.count(),
                'present': teacher_attendance.filter(status='P').count(),
                'absent': teacher_attendance.filter(status='A').count(),
                'late': teacher_attendance.filter(status='L').count(),
                'excused': teacher_attendance.filter(status='E').count(),
            }
        }
        
        return Response(data)
