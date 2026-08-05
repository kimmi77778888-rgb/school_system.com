from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    UserProfile, LoginHistory, AcademicYear, Grade, Teacher, TeacherDocument,
    TeacherEmploymentHistory, Classroom, Student, Subject, TimeSlot, Timetable,
    Attendance, TeacherAttendance, ExamType, Exam, Score, Notification,
    NotificationRead, ReportCard, SchoolEvent, SchoolSettings, StudentHistory
)


# ══════════════════════════════════════════════════════
#  USER & AUTHENTICATION
# ══════════════════════════════════════════════════════
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active', 'date_joined']
        read_only_fields = ['date_joined']


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.IntegerField(write_only=True, required=False)
    role_display = serializers.CharField(source='get_role_display', read_only=True)
    photo_url = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = [
            'id', 'user', 'user_id', 'role', 'role_display', 'phone', 
            'photo', 'photo_url', 'teacher', 'student'
        ]

    def get_photo_url(self, obj):
        if obj.photo:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.photo.url)
            return obj.photo.url
        return None


class LoginHistorySerializer(serializers.ModelSerializer):
    user_username = serializers.CharField(source='user.username', read_only=True)
    device_icon = serializers.CharField(source='get_device_icon', read_only=True)

    class Meta:
        model = LoginHistory
        fields = [
            'id', 'user', 'user_username', 'login_time', 'ip_address',
            'device_type', 'device_icon', 'browser', 'operating_system',
            'device_name', 'location', 'is_suspicious'
        ]
        read_only_fields = ['login_time']


# ══════════════════════════════════════════════════════
#  ACADEMIC STRUCTURE
# ══════════════════════════════════════════════════════
class AcademicYearSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicYear
        fields = ['id', 'year', 'is_active']


class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = ['id', 'name', 'section']


# ══════════════════════════════════════════════════════
#  TEACHER
# ══════════════════════════════════════════════════════
class TeacherDocumentSerializer(serializers.ModelSerializer):
    uploaded_by_username = serializers.CharField(source='uploaded_by.username', read_only=True)
    document_type_display = serializers.CharField(source='get_document_type_display', read_only=True)
    file_extension = serializers.CharField(source='get_file_extension', read_only=True)
    is_pdf = serializers.BooleanField(read_only=True)
    is_image = serializers.BooleanField(read_only=True)

    class Meta:
        model = TeacherDocument
        fields = [
            'id', 'teacher', 'document_type', 'document_type_display',
            'document_file', 'title', 'description', 'uploaded_at',
            'uploaded_by', 'uploaded_by_username', 'file_extension',
            'is_pdf', 'is_image'
        ]
        read_only_fields = ['uploaded_at']


class TeacherEmploymentHistorySerializer(serializers.ModelSerializer):
    duration_years = serializers.FloatField(read_only=True)

    class Meta:
        model = TeacherEmploymentHistory
        fields = [
            'id', 'teacher', 'school_name', 'position', 'start_date',
            'end_date', 'is_current', 'location', 'responsibilities',
            'achievements', 'reason_leaving', 'duration_years'
        ]


class TeacherSerializer(serializers.ModelSerializer):
    gender_display = serializers.CharField(source='get_gender_display', read_only=True)
    rank_display = serializers.CharField(source='get_teacher_rank_display', read_only=True)
    photo_url = serializers.SerializerMethodField()
    age = serializers.IntegerField(source='get_age', read_only=True)
    documents = TeacherDocumentSerializer(many=True, read_only=True)
    employment_history = TeacherEmploymentHistorySerializer(many=True, read_only=True)
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = Teacher
        fields = [
            'id', 'teacher_id', 'first_name', 'last_name', 'first_name_en',
            'last_name_en', 'full_name', 'gender', 'gender_display', 'phone', 'email',
            'address', 'subject_specialty', 'hire_date', 'photo', 'photo_url',
            'qualification', 'is_active', 'teacher_rank', 'rank_display',
            'teacher_license', 'ministry_id', 'date_of_birth', 'age',
            'place_of_birth', 'national_id', 'teacher_training', 'certifications',
            'university', 'degree', 'graduation_year', 'contract_type',
            'salary_scale', 'years_experience', 'emergency_contact',
            'emergency_phone', 'emergency_relation', 'documents', 'employment_history'
        ]
        read_only_fields = ['teacher_id']

    def get_photo_url(self, obj):
        if obj.photo:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.photo.url)
            return obj.photo.url
        return None

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"


class TeacherListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for list views"""
    gender_display = serializers.CharField(source='get_gender_display', read_only=True)
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = Teacher
        fields = [
            'id', 'teacher_id', 'first_name', 'last_name', 'full_name',
            'gender', 'gender_display', 'phone', 'email', 'subject_specialty',
            'is_active', 'photo'
        ]

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"


# ══════════════════════════════════════════════════════
#  STUDENT
# ══════════════════════════════════════════════════════
class StudentSerializer(serializers.ModelSerializer):
    gender_display = serializers.CharField(source='get_gender_display', read_only=True)
    photo_url = serializers.SerializerMethodField()
    classroom_name = serializers.CharField(source='classroom.__str__', read_only=True)
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = Student
        fields = [
            'id', 'student_id', 'first_name', 'last_name', 'first_name_en',
            'last_name_en', 'full_name', 'gender', 'gender_display', 'date_of_birth',
            'address', 'phone', 'parent_name', 'parent_phone', 'parent_email',
            'classroom', 'classroom_name', 'enrolled_date', 'photo', 'photo_url',
            'is_active', 'blood_group', 'medical_notes'
        ]
        read_only_fields = ['student_id', 'enrolled_date']

    def get_photo_url(self, obj):
        if obj.photo:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.photo.url)
            return obj.photo.url
        return None

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"


class StudentListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for list views"""
    gender_display = serializers.CharField(source='get_gender_display', read_only=True)
    classroom_name = serializers.CharField(source='classroom.__str__', read_only=True)
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = Student
        fields = [
            'id', 'student_id', 'first_name', 'last_name', 'full_name',
            'gender', 'gender_display', 'classroom', 'classroom_name',
            'is_active', 'photo'
        ]

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"


# ══════════════════════════════════════════════════════
#  STUDENT HISTORY
# ══════════════════════════════════════════════════════
class StudentHistorySerializer(serializers.ModelSerializer):
    """Student academic history serializer"""
    student_name = serializers.CharField(source='student.__str__', read_only=True)
    academic_year_name = serializers.CharField(source='academic_year.year', read_only=True)
    classroom_name = serializers.CharField(source='classroom.__str__', read_only=True, allow_null=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    grade_level_display = serializers.SerializerMethodField()
    attendance_percentage = serializers.FloatField(read_only=True)
    pass_percentage = serializers.FloatField(read_only=True)

    class Meta:
        model = StudentHistory
        fields = [
            'id', 'student', 'student_name', 'academic_year', 'academic_year_name',
            'classroom', 'classroom_name', 'grade_name', 'grade_number', 'grade_level',
            'grade_level_display', 'status', 'status_display', 'average_score',
            'total_subjects', 'passed_subjects', 'failed_subjects', 'total_days',
            'present_days', 'absent_days', 'attendance_percentage', 'pass_percentage',
            'start_date', 'end_date', 'promoted_to', 'promotion_note', 'notes',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def get_grade_level_display(self, obj):
        level_map = {
            'primary': 'បឋមសិក្សា (Primary)',
            'lower_secondary': 'បឋមភូមិ (Lower Secondary)',
            'upper_secondary': 'មធ្យមភូមិ (Upper Secondary)'
        }
        return level_map.get(obj.grade_level, obj.grade_level)


class PromotionEligibilitySerializer(serializers.Serializer):
    """Serializer for student promotion eligibility data"""
    student_id = serializers.IntegerField()
    student_name = serializers.CharField()
    student_code = serializers.CharField()
    current_classroom = serializers.CharField()
    current_grade_number = serializers.IntegerField()
    total_subjects = serializers.IntegerField()
    passed_subjects = serializers.IntegerField()
    failed_subjects = serializers.IntegerField()
    avg_percentage = serializers.FloatField()
    attendance_rate = serializers.FloatField()
    total_days = serializers.IntegerField()
    present_days = serializers.IntegerField()
    can_promote = serializers.BooleanField()
    promotion_status = serializers.CharField()
    reasons = serializers.ListField(child=serializers.CharField())


class BulkPromotionRequestSerializer(serializers.Serializer):
    """Serializer for bulk promotion request"""
    student_ids = serializers.ListField(
        child=serializers.IntegerField(),
        min_length=1,
        help_text="List of student IDs to promote"
    )
    next_classroom_id = serializers.IntegerField(help_text="Target classroom ID")
    academic_year_id = serializers.IntegerField(
        required=False,
        allow_null=True,
        help_text="Academic year to base promotion on (optional)"
    )
    passing_percentage = serializers.FloatField(
        default=50.0,
        min_value=0,
        max_value=100,
        help_text="Minimum passing percentage (default: 50)"
    )


class PromotionResultSerializer(serializers.Serializer):
    """Serializer for promotion operation results"""
    success = serializers.BooleanField()
    message = serializers.CharField()
    promoted_count = serializers.IntegerField()
    failed_count = serializers.IntegerField()
    promoted_students = serializers.ListField(child=serializers.DictField())
    failed_promotions = serializers.ListField(child=serializers.DictField())


# ══════════════════════════════════════════════════════
#  CLASSROOM
# ══════════════════════════════════════════════════════
class ClassroomSerializer(serializers.ModelSerializer):
    grade_name = serializers.CharField(source='grade.__str__', read_only=True)
    homeroom_teacher_name = serializers.CharField(source='homeroom_teacher.__str__', read_only=True)
    academic_year_name = serializers.CharField(source='academic_year.year', read_only=True)
    student_count = serializers.SerializerMethodField()

    class Meta:
        model = Classroom
        fields = [
            'id', 'classroom_id', 'grade', 'grade_name', 'homeroom_teacher',
            'homeroom_teacher_name', 'academic_year', 'academic_year_name',
            'room_number', 'capacity', 'student_count'
        ]
        read_only_fields = ['classroom_id']

    def get_student_count(self, obj):
        return obj.students.count()


# ══════════════════════════════════════════════════════
#  SUBJECT
# ══════════════════════════════════════════════════════
class SubjectSerializer(serializers.ModelSerializer):
    teacher_name = serializers.CharField(source='teacher.__str__', read_only=True)
    grade_name = serializers.CharField(source='grade.__str__', read_only=True)

    class Meta:
        model = Subject
        fields = [
            'id', 'subject_id', 'name', 'code', 'teacher', 'teacher_name',
            'grade', 'grade_name', 'credit', 'description'
        ]
        read_only_fields = ['subject_id']


# ══════════════════════════════════════════════════════
#  TIMETABLE
# ══════════════════════════════════════════════════════
class TimeSlotSerializer(serializers.ModelSerializer):
    day_display = serializers.CharField(source='get_day_display', read_only=True)

    class Meta:
        model = TimeSlot
        fields = ['id', 'day', 'day_display', 'start_time', 'end_time', 'period']


class TimetableSerializer(serializers.ModelSerializer):
    classroom_name = serializers.CharField(source='classroom.__str__', read_only=True)
    subject_name = serializers.CharField(source='subject.name', read_only=True)
    teacher_name = serializers.CharField(source='teacher.__str__', read_only=True)
    time_slot_details = TimeSlotSerializer(source='time_slot', read_only=True)
    academic_year_name = serializers.CharField(source='academic_year.year', read_only=True)

    class Meta:
        model = Timetable
        fields = [
            'id', 'classroom', 'classroom_name', 'subject', 'subject_name',
            'teacher', 'teacher_name', 'time_slot', 'time_slot_details',
            'academic_year', 'academic_year_name', 'room'
        ]


# ══════════════════════════════════════════════════════
#  ATTENDANCE
# ══════════════════════════════════════════════════════
class AttendanceSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.__str__', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Attendance
        fields = [
            'id', 'student', 'student_name', 'date', 'status',
            'status_display', 'note'
        ]


class TeacherAttendanceSerializer(serializers.ModelSerializer):
    teacher_name = serializers.CharField(source='teacher.__str__', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = TeacherAttendance
        fields = [
            'id', 'teacher', 'teacher_name', 'date', 'status',
            'status_display', 'note'
        ]


# ══════════════════════════════════════════════════════
#  EXAMS & SCORES
# ══════════════════════════════════════════════════════
class ExamTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamType
        fields = ['id', 'name']


class ExamSerializer(serializers.ModelSerializer):
    exam_type_name = serializers.CharField(source='exam_type.name', read_only=True)
    subject_name = serializers.CharField(source='subject.name', read_only=True)
    classroom_name = serializers.CharField(source='classroom.__str__', read_only=True)
    academic_year_name = serializers.CharField(source='academic_year.year', read_only=True)

    class Meta:
        model = Exam
        fields = [
            'id', 'exam_id', 'name', 'exam_type', 'exam_type_name',
            'subject', 'subject_name', 'classroom', 'classroom_name',
            'academic_year', 'academic_year_name', 'date', 'max_score',
            'description'
        ]
        read_only_fields = ['exam_id']


class ScoreSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.__str__', read_only=True)
    subject_name = serializers.CharField(source='subject.name', read_only=True)
    exam_type_name = serializers.CharField(source='exam_type.name', read_only=True)
    exam_name = serializers.CharField(source='exam.name', read_only=True, allow_null=True)
    academic_year_name = serializers.CharField(source='academic_year.year', read_only=True)
    percentage = serializers.FloatField(read_only=True)
    grade_letter = serializers.CharField(read_only=True)
    grade_color = serializers.CharField(read_only=True)

    class Meta:
        model = Score
        fields = [
            'id', 'student', 'student_name', 'subject', 'subject_name',
            'exam_type', 'exam_type_name', 'exam', 'exam_name',
            'academic_year', 'academic_year_name', 'score', 'max_score',
            'percentage', 'grade_letter', 'grade_color', 'date_recorded',
            'remarks'
        ]
        read_only_fields = ['date_recorded']


# ══════════════════════════════════════════════════════
#  NOTIFICATIONS
# ══════════════════════════════════════════════════════
class NotificationSerializer(serializers.ModelSerializer):
    type_display = serializers.CharField(source='get_notification_type_display', read_only=True)
    audience_display = serializers.CharField(source='get_audience_display', read_only=True)
    created_by_username = serializers.CharField(source='created_by.username', read_only=True, allow_null=True)
    is_read = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = [
            'id', 'notification_id', 'title', 'message', 'notification_type',
            'type_display', 'audience', 'audience_display', 'created_by',
            'created_by_username', 'created_at', 'is_active', 'scheduled_at',
            'classroom', 'student', 'is_read'
        ]
        read_only_fields = ['notification_id', 'created_at']

    def get_is_read(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.reads.filter(user=request.user).exists()
        return False


class NotificationReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationRead
        fields = ['id', 'notification', 'user', 'read_at']
        read_only_fields = ['read_at']


# ══════════════════════════════════════════════════════
#  REPORT CARD
# ══════════════════════════════════════════════════════
class ReportCardSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.__str__', read_only=True)
    academic_year_name = serializers.CharField(source='academic_year.year', read_only=True)
    generated_by_username = serializers.CharField(source='generated_by.username', read_only=True, allow_null=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = ReportCard
        fields = [
            'id', 'report_id', 'student', 'student_name', 'academic_year',
            'academic_year_name', 'term', 'generated_at', 'generated_by',
            'generated_by_username', 'status', 'status_display',
            'teacher_remarks', 'principal_remarks', 'conduct',
            'attendance_days', 'absent_days'
        ]
        read_only_fields = ['report_id', 'generated_at']


# ══════════════════════════════════════════════════════
#  SCHOOL EVENT
# ══════════════════════════════════════════════════════
class SchoolEventSerializer(serializers.ModelSerializer):
    type_display = serializers.CharField(source='get_event_type_display', read_only=True)
    created_by_username = serializers.CharField(source='created_by.username', read_only=True, allow_null=True)

    class Meta:
        model = SchoolEvent
        fields = [
            'id', 'event_id', 'title', 'event_type', 'type_display',
            'start_date', 'end_date', 'description', 'created_by',
            'created_by_username'
        ]
        read_only_fields = ['event_id']


# ══════════════════════════════════════════════════════
#  SCHOOL SETTINGS
# ══════════════════════════════════════════════════════
class SchoolSettingsSerializer(serializers.ModelSerializer):
    logo_url = serializers.SerializerMethodField()
    favicon_url = serializers.SerializerMethodField()

    class Meta:
        model = SchoolSettings
        fields = [
            'id', 'school_name', 'school_name_en', 'school_slogan',
            'logo', 'logo_url', 'favicon', 'favicon_url', 'address',
            'phone', 'email'
        ]

    def get_logo_url(self, obj):
        if obj.logo:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.logo.url)
            return obj.logo.url
        return None

    def get_favicon_url(self, obj):
        if obj.favicon:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.favicon.url)
            return obj.favicon.url
        return None
