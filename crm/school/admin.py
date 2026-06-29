from django.contrib import admin
from .models import (
    AcademicYear, Grade, Teacher, Classroom, Student, Subject,
    Attendance, ExamType, Exam, Score, TimeSlot, Timetable,
    Notification, NotificationRead, ReportCard, SchoolEvent,
    UserProfile, SchoolSettings
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


@admin.register(Classroom)
class ClassroomAdmin(admin.ModelAdmin):
    list_display = ('grade', 'homeroom_teacher', 'academic_year', 'room_number', 'capacity')
    list_filter  = ('academic_year',)


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display  = ('student_id', 'first_name', 'last_name', 'gender', 'classroom', 'is_active')
    search_fields = ('student_id', 'first_name', 'last_name')
    list_filter   = ('is_active', 'gender', 'classroom')


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'teacher', 'grade', 'credit')
    list_filter  = ('grade',)


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display   = ('student', 'date', 'status', 'note')
    list_filter    = ('status', 'date')
    search_fields  = ('student__first_name', 'student__last_name', 'student__student_id')
    date_hierarchy = 'date'


@admin.register(ExamType)
class ExamTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ('name', 'exam_type', 'subject', 'classroom', 'date', 'max_score')
    list_filter  = ('exam_type', 'academic_year', 'classroom')
    date_hierarchy = 'date'


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


@admin.register(ReportCard)
class ReportCardAdmin(admin.ModelAdmin):
    list_display = ('student', 'academic_year', 'term', 'status', 'generated_at')
    list_filter  = ('status', 'academic_year', 'term')


@admin.register(SchoolEvent)
class SchoolEventAdmin(admin.ModelAdmin):
    list_display = ('title', 'event_type', 'start_date', 'end_date')
    list_filter  = ('event_type',)
