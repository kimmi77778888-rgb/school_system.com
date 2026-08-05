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
    NotificationRead, ReportCard, SchoolEvent, SchoolSettings, StudentHistory
)
from .serializers import (
    UserSerializer, UserProfileSerializer, LoginHistorySerializer,
    AcademicYearSerializer, GradeSerializer, TeacherSerializer, TeacherListSerializer,
    TeacherDocumentSerializer, TeacherEmploymentHistorySerializer,
    ClassroomSerializer, StudentSerializer, StudentListSerializer,
    StudentHistorySerializer, PromotionEligibilitySerializer,
    BulkPromotionRequestSerializer, PromotionResultSerializer,
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

    @action(detail=True, methods=['get'])
    def history(self, request, pk=None):
        """
        Get student's academic history across all years
        GET /api/students/{id}/history/
        """
        student = self.get_object()
        histories = StudentHistory.objects.filter(student=student).order_by('-academic_year__year')
        serializer = StudentHistorySerializer(histories, many=True, context={'request': request})
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def check_promotion_eligibility(self, request):
        """
        Check promotion eligibility for students in a classroom
        
        POST /api/students/check_promotion_eligibility/
        Body: {
            "classroom_id": 1,
            "academic_year_id": 1,  // optional
            "passing_percentage": 50.0  // optional, default 50
        }
        
        Returns list of students with eligibility status
        """
        from django.shortcuts import get_object_or_404
        
        classroom_id = request.data.get('classroom_id')
        academic_year_id = request.data.get('academic_year_id')
        passing_percentage = float(request.data.get('passing_percentage', 50))
        
        if not classroom_id:
            return Response(
                {'error': 'classroom_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        current_classroom = get_object_or_404(Classroom, pk=classroom_id)
        
        # Get students in the classroom
        students = Student.objects.filter(
            classroom=current_classroom,
            is_active=True
        ).prefetch_related('scores', 'attendances')
        
        students_eligibility = []
        
        for student in students:
            # Filter scores by academic year if provided
            if academic_year_id:
                academic_year = get_object_or_404(AcademicYear, pk=academic_year_id)
                scores = student.scores.filter(academic_year=academic_year)
            else:
                # Use classroom's academic year or all scores
                if current_classroom.academic_year:
                    scores = student.scores.filter(academic_year=current_classroom.academic_year)
                else:
                    scores = student.scores.all()
            
            if scores.exists():
                # Calculate average percentage
                total_subjects = scores.count()
                avg_percentage = sum(score.percentage() for score in scores) / total_subjects if total_subjects > 0 else 0
                
                # Calculate attendance rate
                if academic_year_id:
                    year = get_object_or_404(AcademicYear, pk=academic_year_id)
                elif current_classroom.academic_year:
                    year = current_classroom.academic_year
                else:
                    year = None
                
                if year:
                    try:
                        if '-' in year.year:
                            start_year = year.year.split('-')[0]
                            end_year = year.year.split('-')[1]
                            year_attendance = student.attendances.filter(
                                date__gte=f'{start_year}-01-01',
                                date__lte=f'{end_year}-12-31'
                            )
                        else:
                            year_attendance = student.attendances.all()
                    except:
                        year_attendance = student.attendances.all()
                else:
                    year_attendance = student.attendances.all()
                
                total_days = year_attendance.count()
                present_days = year_attendance.filter(status='P').count()
                attendance_rate = (present_days / total_days * 100) if total_days > 0 else 0
                
                # Check promotion criteria
                can_promote = (
                    avg_percentage >= passing_percentage and 
                    total_subjects > 0 and
                    attendance_rate >= 80.0
                )
                
                passed_subjects = sum(1 for score in scores if score.is_passing(passing_percentage))
                failed_subjects = total_subjects - passed_subjects
                
                # Build reasons list
                reasons = []
                if avg_percentage < passing_percentage:
                    reasons.append(f'ពិន្ទុមធ្យម {avg_percentage:.1f}% < {passing_percentage}%')
                if attendance_rate < 80.0:
                    reasons.append(f'វត្តមាន {attendance_rate:.1f}% < 80%')
                if total_subjects == 0:
                    reasons.append('មិនមានពិន្ទុ')
                
                promotion_status = '✅ អាចឡើងថ្នាក់' if can_promote else '❌ មិនអាចឡើងថ្នាក់'
                
                students_eligibility.append({
                    'student_id': student.id,
                    'student_name': str(student),
                    'student_code': student.student_id,
                    'current_classroom': str(current_classroom),
                    'current_grade_number': current_classroom.grade.grade_number if current_classroom.grade else 0,
                    'total_subjects': total_subjects,
                    'passed_subjects': passed_subjects,
                    'failed_subjects': failed_subjects,
                    'avg_percentage': round(avg_percentage, 1),
                    'attendance_rate': round(attendance_rate, 1),
                    'total_days': total_days,
                    'present_days': present_days,
                    'can_promote': can_promote,
                    'promotion_status': promotion_status,
                    'reasons': reasons if not can_promote else []
                })
            else:
                students_eligibility.append({
                    'student_id': student.id,
                    'student_name': str(student),
                    'student_code': student.student_id,
                    'current_classroom': str(current_classroom),
                    'current_grade_number': current_classroom.grade.grade_number if current_classroom.grade else 0,
                    'total_subjects': 0,
                    'passed_subjects': 0,
                    'failed_subjects': 0,
                    'avg_percentage': 0,
                    'attendance_rate': 0,
                    'total_days': 0,
                    'present_days': 0,
                    'can_promote': False,
                    'promotion_status': '❌ មិនអាចឡើងថ្នាក់',
                    'reasons': ['មិនមានពិន្ទុ']
                })
        
        return Response({
            'classroom': str(current_classroom),
            'classroom_id': current_classroom.id,
            'total_students': len(students_eligibility),
            'eligible_count': sum(1 for s in students_eligibility if s['can_promote']),
            'students': students_eligibility
        })

    @action(detail=False, methods=['post'])
    def bulk_promote(self, request):
        """
        Bulk promote students to next grade
        
        POST /api/students/bulk_promote/
        Body: {
            "student_ids": [1, 2, 3],
            "next_classroom_id": 5,
            "academic_year_id": 1,  // optional
            "passing_percentage": 50.0  // optional, default 50
        }
        
        Returns promotion results with success/failure details
        """
        from django.shortcuts import get_object_or_404
        from django.utils import timezone
        
        serializer = BulkPromotionRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        student_ids = serializer.validated_data['student_ids']
        next_classroom_id = serializer.validated_data['next_classroom_id']
        academic_year_id = serializer.validated_data.get('academic_year_id')
        passing_percentage = serializer.validated_data.get('passing_percentage', 50.0)
        
        next_classroom = get_object_or_404(Classroom, pk=next_classroom_id)
        
        promoted_students = []
        failed_promotions = []
        
        for student_id in student_ids:
            try:
                student = Student.objects.get(pk=student_id)
                old_classroom = student.classroom
                
                if not old_classroom:
                    failed_promotions.append({
                        'student_id': student_id,
                        'student_name': str(student),
                        'reason': 'មិនមានថ្នាក់បច្ចុប្បន្ន'
                    })
                    continue
                
                # Get grade information
                old_grade = old_classroom.grade
                new_grade = next_classroom.grade
                old_grade_number = old_grade.grade_number if old_grade else 0
                new_grade_number = new_grade.grade_number if new_grade else 0
                
                # VALIDATION 1: Must promote to next grade only
                if new_grade_number != old_grade_number + 1:
                    failed_promotions.append({
                        'student_id': student_id,
                        'student_name': str(student),
                        'reason': f'មិនអាចរំលងថ្នាក់បានទេ (ថ្នាក់ {old_grade_number} → ថ្នាក់ {new_grade_number})'
                    })
                    continue
                
                # VALIDATION 2: Check level transitions
                if old_grade:
                    old_level = old_grade.level
                    new_level = new_grade.level if new_grade else ''
                    
                    if old_level == 'primary' and old_grade_number == 6:
                        if new_level != 'lower_secondary' or new_grade_number != 7:
                            failed_promotions.append({
                                'student_id': student_id,
                                'student_name': str(student),
                                'reason': 'ត្រូវផ្ទេរពីបឋមសិក្សាទៅបឋមភូមិ (Grade 6 → Grade 7)'
                            })
                            continue
                    
                    elif old_level == 'lower_secondary' and old_grade_number == 9:
                        if new_level != 'upper_secondary' or new_grade_number != 10:
                            failed_promotions.append({
                                'student_id': student_id,
                                'student_name': str(student),
                                'reason': 'ត្រូវផ្ទេរពីបឋមភូមិទៅមធ្យមភូមិ (Grade 9 → Grade 10)'
                            })
                            continue
                    
                    elif old_grade_number == 12:
                        failed_promotions.append({
                            'student_id': student_id,
                            'student_name': str(student),
                            'reason': 'បញ្ចប់ការសិក្សាហើយ (Grade 12)'
                        })
                        continue
                
                # === CREATE HISTORY RECORD ===
                if old_classroom.academic_year:
                    year = old_classroom.academic_year
                    
                    # Calculate scores for this academic year
                    year_scores = student.scores.filter(academic_year=year)
                    total_subjects = year_scores.count()
                    if total_subjects > 0:
                        avg_score = sum(s.score for s in year_scores) / total_subjects
                        passed = sum(1 for s in year_scores if s.is_passing(passing_percentage))
                        failed = total_subjects - passed
                    else:
                        avg_score = 0
                        passed = 0
                        failed = 0
                    
                    # Calculate attendance
                    try:
                        if '-' in year.year:
                            start_year = year.year.split('-')[0]
                            end_year = year.year.split('-')[1]
                            year_attendance = student.attendances.filter(
                                date__gte=f'{start_year}-01-01',
                                date__lte=f'{end_year}-12-31'
                            )
                        else:
                            year_attendance = student.attendances.all()
                    except:
                        year_attendance = student.attendances.all()
                    
                    total_days = year_attendance.count()
                    present_days = year_attendance.filter(status='P').count()
                    absent_days = year_attendance.filter(status='A').count()
                    attendance_rate = (present_days / total_days * 100) if total_days > 0 else 0
                    
                    # Determine level transition note
                    level_transition_note = ""
                    if old_grade_number == 6 and new_grade_number == 7:
                        level_transition_note = " | ✅ ផ្ទេរពីបឋមសិក្សាទៅបឋមភូមិ (Primary → Lower Secondary)"
                    elif old_grade_number == 9 and new_grade_number == 10:
                        level_transition_note = " | ✅ ផ្ទេរពីបឋមភូមិទៅមធ្យមភូមិ (Lower Secondary → Upper Secondary)"
                    elif old_grade_number == 12:
                        level_transition_note = " | 🎓 បញ្ចប់ការសិក្សា (Graduated)"
                    
                    # Create or update history record
                    history, created = StudentHistory.objects.update_or_create(
                        student=student,
                        academic_year=year,
                        defaults={
                            'classroom': old_classroom,
                            'grade_name': str(old_classroom.grade),
                            'grade_number': old_grade_number,
                            'grade_level': old_grade.level if old_grade else 'primary',
                            'status': 'PROMOTED',
                            'average_score': avg_score,
                            'total_subjects': total_subjects,
                            'passed_subjects': passed,
                            'failed_subjects': failed,
                            'total_days': total_days,
                            'present_days': present_days,
                            'absent_days': absent_days,
                            'end_date': timezone.now().date(),
                            'promoted_to': str(next_classroom),
                            'promotion_note': f"ឡើងថ្នាក់ទៅ {next_classroom.grade} នៅថ្ងៃទី {timezone.now().strftime('%d/%m/%Y')}{level_transition_note}",
                            'notes': f"ពិន្ទុមធ្យម: {avg_score:.1f} | វត្តមាន: {present_days}/{total_days} ថ្ងៃ ({attendance_rate:.1f}%)"
                        }
                    )
                
                # === UPDATE STUDENT RECORD ===
                old_classroom_str = str(old_classroom)
                student.previous_classroom = old_classroom_str
                student.promotion_date = timezone.now().date()
                student.status = 'ACTIVE'
                student.is_active = True  # Ensure student is active and visible
                student.classroom = next_classroom
                
                # Add note with level transition info
                level_note = ""
                if old_grade_number == 6 and new_grade_number == 7:
                    level_note = " (✅ ចូលបឋមភូមិ)"
                elif old_grade_number == 9 and new_grade_number == 10:
                    level_note = " (✅ ចូលមធ្យមភូមិ)"
                
                promotion_note = f"ឡើងថ្នាក់ពី {old_classroom_str} ទៅ {next_classroom} នៅថ្ងៃទី {timezone.now().strftime('%d/%m/%Y')}{level_note}"
                if student.notes:
                    student.notes += f"\n{promotion_note}"
                else:
                    student.notes = promotion_note
                
                student.save()
                
                promoted_students.append({
                    'student_id': student.id,
                    'student_name': str(student),
                    'student_code': student.student_id,
                    'from_classroom': old_classroom_str,
                    'to_classroom': str(next_classroom),
                    'promotion_date': timezone.now().strftime('%d/%m/%Y'),
                    'level_transition': level_note
                })
                
            except Student.DoesNotExist:
                failed_promotions.append({
                    'student_id': student_id,
                    'student_name': 'Unknown',
                    'reason': f'Student ID {student_id} not found'
                })
            except Exception as e:
                failed_promotions.append({
                    'student_id': student_id,
                    'student_name': str(student) if 'student' in locals() else 'Unknown',
                    'reason': str(e)
                })
        
        result = {
            'success': len(promoted_students) > 0,
            'message': f'បានដាក់សិស្ស {len(promoted_students)} នាក់ឡើងថ្នាក់ទៅ {next_classroom}',
            'promoted_count': len(promoted_students),
            'failed_count': len(failed_promotions),
            'promoted_students': promoted_students,
            'failed_promotions': failed_promotions
        }
        
        return Response(result, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def available_promotions(self, request):
        """
        Get available next-grade classrooms for a current classroom
        
        GET /api/students/available_promotions/?classroom_id=1
        
        Returns list of classrooms that are valid promotion targets
        """
        from django.shortcuts import get_object_or_404
        
        classroom_id = request.query_params.get('classroom_id')
        if not classroom_id:
            return Response(
                {'error': 'classroom_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        current_classroom = get_object_or_404(Classroom, pk=classroom_id)
        current_grade = current_classroom.grade
        
        if not current_grade or not current_grade.grade_number:
            return Response({
                'error': 'Current classroom does not have a valid grade'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        current_grade_num = current_grade.grade_number
        next_grade_num = current_grade_num + 1
        
        # Get classrooms with next grade number only (strict progression)
        next_classrooms = Classroom.objects.filter(
            grade__grade_number=next_grade_num
        ).select_related('grade', 'academic_year').prefetch_related('timetables')
        
        classrooms_data = []
        for classroom in next_classrooms:
            classrooms_data.append({
                'id': classroom.id,
                'name': str(classroom),
                'grade_number': classroom.grade.grade_number,
                'grade_name': str(classroom.grade),
                'grade_level': classroom.grade.level if classroom.grade else '',
                'academic_year': classroom.academic_year.year if classroom.academic_year else '',
                'room_number': classroom.room_number,
                'capacity': classroom.capacity,
                'current_students': classroom.students.filter(is_active=True).count(),
                'has_timetable': classroom.timetables.exists(),
                'timetable_count': classroom.timetables.count()
            })
        
        return Response({
            'current_classroom': str(current_classroom),
            'current_grade_number': current_grade_num,
            'next_grade_number': next_grade_num,
            'available_classrooms': classrooms_data,
            'total_available': len(classrooms_data)
        })


# ══════════════════════════════════════════════════════
#  STUDENT HISTORY
# ══════════════════════════════════════════════════════
class StudentHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for viewing student academic history
    Read-only: History is created automatically during promotion
    """
    queryset = StudentHistory.objects.select_related(
        'student', 'academic_year', 'classroom', 'classroom__grade'
    ).all()
    serializer_class = StudentHistorySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['student', 'academic_year', 'grade_number', 'grade_level', 'status']
    search_fields = ['student__first_name', 'student__last_name', 'student__student_id', 'grade_name']
    ordering_fields = ['academic_year__year', 'grade_number', 'average_score']
    ordering = ['-academic_year__year', 'student__last_name']

    @action(detail=False, methods=['get'])
    def by_student(self, request):
        """
        Get all history records for a specific student
        GET /api/student-history/by_student/?student_id=1
        """
        student_id = request.query_params.get('student_id')
        if not student_id:
            return Response(
                {'error': 'student_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        histories = self.queryset.filter(student_id=student_id).order_by('-academic_year__year')
        serializer = self.get_serializer(histories, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def by_academic_year(self, request):
        """
        Get all history records for a specific academic year
        GET /api/student-history/by_academic_year/?academic_year_id=1
        """
        academic_year_id = request.query_params.get('academic_year_id')
        if not academic_year_id:
            return Response(
                {'error': 'academic_year_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        histories = self.queryset.filter(academic_year_id=academic_year_id)
        serializer = self.get_serializer(histories, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def promotion_statistics(self, request):
        """
        Get promotion statistics for an academic year
        GET /api/student-history/promotion_statistics/?academic_year_id=1
        """
        academic_year_id = request.query_params.get('academic_year_id')
        if not academic_year_id:
            return Response(
                {'error': 'academic_year_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        from django.db.models import Count, Avg
        
        histories = self.queryset.filter(academic_year_id=academic_year_id)
        
        stats = {
            'total_students': histories.count(),
            'promoted': histories.filter(status='PROMOTED').count(),
            'graduated': histories.filter(status='GRADUATED').count(),
            'transferred': histories.filter(status='TRANSFERRED').count(),
            'withdrawn': histories.filter(status='WITHDRAWN').count(),
            'average_score': histories.aggregate(Avg('average_score'))['average_score__avg'],
            'average_attendance': histories.aggregate(
                avg_attendance=Avg('present_days') * 100.0 / Avg('total_days')
            )['avg_attendance'],
            'by_grade_level': {}
        }
        
        # Statistics by grade level
        for level in ['primary', 'lower_secondary', 'upper_secondary']:
            level_histories = histories.filter(grade_level=level)
            stats['by_grade_level'][level] = {
                'total': level_histories.count(),
                'promoted': level_histories.filter(status='PROMOTED').count(),
                'avg_score': level_histories.aggregate(Avg('average_score'))['average_score__avg']
            }
        
        return Response(stats)


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
