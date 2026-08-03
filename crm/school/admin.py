from django.contrib import admin
from .models import (
    AcademicYear, Grade, Teacher, TeacherDocument, Classroom, Student, StudentHistory, Subject,
    Attendance, TeacherAttendance, TeacherEmploymentHistory, ExamType, Exam, Score, TimeSlot, Timetable,
    Notification, NotificationRead, ReportCard, SchoolEvent,
    UserProfile, LoginHistory, SchoolSettings
)


@admin.register(SchoolSettings)
class SchoolSettingsAdmin(admin.ModelAdmin):
    list_display = ('school_name', 'school_name_en', 'phone', 'email', 'updated_at')
    fieldsets = (
        ('School Identity', {'fields': ('school_name', 'school_name_en', 'school_slogan', 'logo', 'favicon')}),
        ('Contact',         {'fields': ('address', 'phone', 'email', 'website')}),
        ('Colors',          {'fields': ('primary_color', 'secondary_color', 'sidebar_bg')}),
    )
    def has_add_permission(self, request):
        return not SchoolSettings.objects.exists()
    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'phone')
    list_filter  = ('role',)


@admin.register(LoginHistory)
class LoginHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'login_time', 'device_type', 'browser', 'ip_address', 'is_suspicious')
    list_filter = ('device_type', 'is_suspicious', 'login_time')
    search_fields = ('user__username', 'ip_address', 'browser', 'device_name')
    readonly_fields = ('login_time', 'user', 'ip_address', 'device_type', 'browser', 
                      'operating_system', 'device_name', 'location', 'user_agent')
    date_hierarchy = 'login_time'


@admin.register(AcademicYear)
class AcademicYearAdmin(admin.ModelAdmin):
    list_display  = ('year', 'is_active')
    list_editable = ('is_active',)


@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ('name', 'section')


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display  = ('teacher_id', 'first_name', 'last_name', 'gender', 'subject_specialty', 'phone', 'is_active')
    search_fields = ('first_name', 'last_name', 'email', 'teacher_id')
    list_filter   = ('gender', 'is_active')
    readonly_fields = ('teacher_id',)


@admin.register(TeacherDocument)
class TeacherDocumentAdmin(admin.ModelAdmin):
    list_display  = ('teacher', 'document_type', 'title', 'uploaded_at', 'uploaded_by')
    list_filter   = ('document_type', 'uploaded_at')
    search_fields = ('teacher__first_name', 'teacher__last_name', 'title', 'description')
    readonly_fields = ('uploaded_at',)


@admin.register(Classroom)
class ClassroomAdmin(admin.ModelAdmin):
    list_display = ('grade', 'homeroom_teacher', 'academic_year', 'room_number', 'capacity')
    list_filter  = ('academic_year',)
    readonly_fields = ('classroom_id',)


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display  = ('student_id', 'first_name', 'last_name', 'gender', 'classroom', 'status', 'is_active')
    search_fields = ('student_id', 'first_name', 'last_name', 'birth_certificate_number')
    list_filter   = ('is_active', 'status', 'gender', 'classroom', 'blood_group')
    readonly_fields = ('student_id', 'enrolled_date', 'previous_classroom', 'promotion_date')
    
    fieldsets = (
        ('ព័ត៌មានមូលដ្ឋាន (Basic Information)', {
            'fields': ('student_id', 'last_name', 'first_name', 'last_name_en', 'first_name_en', 
                      'gender', 'date_of_birth', 'place_of_birth', 'nationality', 'religion', 'photo')
        }),
        ('សំបុត្រកំណើត (Birth Certificate)', {
            'fields': ('birth_certificate_number', 'birth_certificate_file')
        }),
        ('ព័ត៌មានទំនាក់ទំនង (Contact Information)', {
            'fields': ('address', 'phone')
        }),
        ('ព័ត៌មានឪពុក (Father Information)', {
            'fields': ('father_name', 'father_phone', 'father_occupation'),
            'classes': ('collapse',)
        }),
        ('ព័ត៌មានម្តាយ (Mother Information)', {
            'fields': ('mother_name', 'mother_phone', 'mother_occupation'),
            'classes': ('collapse',)
        }),
        ('ព័ត៌មានឪពុកម្តាយ/អាណាព្យាបាល (Parent/Guardian)', {
            'fields': ('parent_name', 'parent_phone', 'parent_email', 'parent_occupation')
        }),
        ('ទំនាក់ទំនងបន្ទាន់ (Emergency Contact)', {
            'fields': ('emergency_contact_name', 'emergency_contact_phone', 'emergency_contact_relation')
        }),
        ('ព័ត៌មានសាលារៀន (School Information)', {
            'fields': ('classroom', 'enrolled_date', 'previous_school', 'status', 'is_active')
        }),
        ('ប្រវត្តិសិស្ស (Student History)', {
            'fields': ('previous_classroom', 'promotion_date', 'graduation_date', 'notes'),
            'classes': ('collapse',)
        }),
        ('ព័ត៌មានសុខភាព (Health Information)', {
            'fields': ('blood_group', 'allergies', 'medical_notes')
        }),
        ('ឯកសារបន្ថែម (Additional Documents)', {
            'fields': ('id_card_file',),
            'classes': ('collapse',)
        }),
    )


@admin.register(StudentHistory)
class StudentHistoryAdmin(admin.ModelAdmin):
    list_display = ('student', 'grade_name', 'academic_year', 'status', 'average_score', 
                   'passed_subjects', 'failed_subjects', 'attendance_percentage')
    list_filter = ('status', 'academic_year', 'grade_name')
    search_fields = ('student__student_id', 'student__first_name', 'student__last_name')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('ព័ត៌មានមូលដ្ឋាន (Basic Information)', {
            'fields': ('student', 'academic_year', 'classroom', 'grade_name', 'status')
        }),
        ('លទ្ធផលសិក្សា (Academic Performance)', {
            'fields': ('average_score', 'total_subjects', 'passed_subjects', 'failed_subjects')
        }),
        ('វត្តមាន (Attendance)', {
            'fields': ('total_days', 'present_days', 'absent_days')
        }),
        ('កាលបរិច្ឆេទ (Dates)', {
            'fields': ('start_date', 'end_date', 'created_at', 'updated_at')
        }),
        ('កំណត់ចំណាំ (Notes)', {
            'fields': ('notes',)
        }),
    )
    
    def attendance_percentage(self, obj):
        return f"{obj.attendance_percentage()}%"
    attendance_percentage.short_description = 'វត្តមាន %'


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'teacher', 'grade', 'credit')
    list_filter  = ('grade',)
    readonly_fields = ('subject_id',)


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display   = ('student', 'date', 'status', 'note')
    list_filter    = ('status', 'date')
    search_fields  = ('student__first_name', 'student__last_name', 'student__student_id')
    date_hierarchy = 'date'


@admin.register(TeacherAttendance)
class TeacherAttendanceAdmin(admin.ModelAdmin):
    list_display   = ('teacher', 'date', 'status', 'note')
    list_filter    = ('status', 'date')
    search_fields  = ('teacher__first_name', 'teacher__last_name', 'teacher__teacher_id')
    date_hierarchy = 'date'


@admin.register(TeacherEmploymentHistory)
class TeacherEmploymentHistoryAdmin(admin.ModelAdmin):
    list_display   = ('teacher', 'school_name', 'position', 'start_date', 'end_date', 'is_current')
    list_filter    = ('is_current', 'start_date')
    search_fields  = ('teacher__first_name', 'teacher__last_name', 'school_name', 'position')
    date_hierarchy = 'start_date'
    ordering       = ('-start_date',)


@admin.register(ExamType)
class ExamTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ('name', 'exam_type', 'subject', 'classroom', 'date', 'max_score')
    list_filter  = ('exam_type', 'academic_year', 'classroom')
    date_hierarchy = 'date'
    readonly_fields = ('exam_id',)


@admin.register(Score)
class ScoreAdmin(admin.ModelAdmin):
    list_display  = ('student', 'subject', 'exam_type', 'score', 'max_score', 'academic_year', 'date_recorded')
    list_filter   = ('exam_type', 'academic_year', 'subject')
    search_fields = ('student__first_name', 'student__last_name', 'student__student_id')


@admin.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ('get_day_display', 'period', 'start_time', 'end_time')
    list_filter  = ('day',)


@admin.register(Timetable)
class TimetableAdmin(admin.ModelAdmin):
    list_display = ('classroom', 'subject', 'teacher', 'time_slot', 'room')
    list_filter  = ('academic_year', 'classroom')


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('title', 'notification_type', 'audience', 'created_by', 'created_at', 'is_active')
    list_filter  = ('notification_type', 'audience', 'is_active')
    readonly_fields = ('notification_id', 'created_at')


@admin.register(ReportCard)
class ReportCardAdmin(admin.ModelAdmin):
    list_display = ('student', 'academic_year', 'term', 'status', 'generated_at')
    list_filter  = ('status', 'academic_year', 'term')
    readonly_fields = ('report_id', 'generated_at')


@admin.register(SchoolEvent)
class SchoolEventAdmin(admin.ModelAdmin):
    list_display = ('title', 'event_type', 'start_date', 'end_date')
    list_filter  = ('event_type',)
    readonly_fields = ('event_id',)
