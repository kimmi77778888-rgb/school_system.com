from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Count, Avg, Q
from django.utils import timezone
from django.urls import reverse
from .decorators import admin_required, admin_or_teacher, all_roles, role_required
from .models import (
    Student, Teacher, Classroom, Grade, Subject,
    Attendance, TeacherAttendance, Score, AcademicYear, ExamType, Exam,
    Timetable, TimeSlot, Notification, NotificationRead,
    ReportCard, SchoolEvent, UserProfile, SchoolSettings
)
from .forms import (
    StudentForm, TeacherForm, ClassroomForm, AttendanceForm,
    BulkAttendanceForm, TeacherAttendanceForm, BulkTeacherAttendanceForm,
    ScoreForm, SubjectForm, GradeForm,
    AcademicYearForm, ExamTypeForm, ExamForm, TimetableForm,
    TimeSlotForm, NotificationForm, ReportCardForm,
    SchoolEventForm, LoginForm, UserCreateForm, ProfileUpdateForm,
    SchoolSettingsForm
)

# ══════════════════════════════════════════════
#  AUTH
# ══════════════════════════════════════════════
def login_view(request):
    if request.user.is_authenticated:
        return redirect('school:dashboard')
    form = LoginForm(request, data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.get_user()
        login(request, user)
        name = user.get_full_name() or user.username
        messages.success(request, f'សូមស្វាគមន៍, {name}!')
        return redirect(request.GET.get('next', 'school:dashboard'))
    return render(request, 'school/auth/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, 'អ្នកបានចាកចេញពីប្រព័ន្ធ។')
    return redirect('school:login')


# ══════════════════════════════════════════════
#  PROFILE UPDATE (all roles)
# ══════════════════════════════════════════════
@login_required
def profile_update(request):
    profile = request.user.profile
    form = ProfileUpdateForm(
        request.POST or None,
        request.FILES or None,
        instance=profile,
        user=request.user
    )
    if request.method == 'POST' and form.is_valid():
        try:
            form.save_user(request.user)
            form.save()
            messages.success(request, 'ប្រវត្តិរូបបានធ្វើបច្ចុប្បន្នភាព។')
            return redirect('school:profile_update')
        except Exception as e:
            import traceback, logging
            logging.getLogger(__name__).error("profile_update failed: %s\n%s", e, traceback.format_exc())
            messages.error(request, f'បញ្ហា: {e}')
    return render(request, 'school/auth/profile.html', {
        'form': form, 'profile': profile
    })


# ══════════════════════════════════════════════
#  SCHOOL SETTINGS (Admin only)
# ══════════════════════════════════════════════
@admin_required
def school_settings_view(request):
    settings_obj = SchoolSettings.get()
    form = SchoolSettingsForm(
        request.POST or None,
        request.FILES or None,
        instance=settings_obj
    )
    if request.method == 'POST':
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'ការកំណត់សាលាបានរក្សាទុក។')
                return redirect('school:school_settings')
            except Exception as e:
                import traceback, logging
                logging.getLogger(__name__).error(
                    "school_settings_view save failed: %s\n%s",
                    e, traceback.format_exc()
                )
                messages.error(request, f'មានបញ្ហាក្នុងការរក្សាទុក: {e}')
        # If form invalid or save failed, fall through to re-render with errors
    return render(request, 'school/school_settings.html', {
        'form': form, 'settings': settings_obj
    })

# ══════════════════════════════════════════════
#  DASHBOARD — role-specific
# ══════════════════════════════════════════════
@login_required
def dashboard(request):
    today = timezone.now().date()
    try:
        role = request.user.profile.role
    except Exception:
        role = 'student'

    notifications  = Notification.objects.filter(is_active=True).order_by('-created_at')[:5]
    upcoming_events = SchoolEvent.objects.filter(start_date__gte=today).order_by('start_date')[:5]

    # ── ADMIN dashboard ──────────────────────
    if role == 'admin':
        return render(request, 'school/dashboard.html', {
            'role': role,
            'total_students':   Student.objects.filter(is_active=True).count(),
            'total_teachers':   Teacher.objects.filter(is_active=True).count(),
            'total_classrooms': Classroom.objects.count(),
            'total_subjects':   Subject.objects.count(),
            'today_present': Attendance.objects.filter(date=today, status='P').count(),
            'today_absent':  Attendance.objects.filter(date=today, status='A').count(),
            'today_late':    Attendance.objects.filter(date=today, status='L').count(),
            'recent_students': Student.objects.filter(is_active=True).order_by('-enrolled_date')[:5],
            'recent_scores':   Score.objects.select_related('student','subject','exam_type').order_by('-date_recorded')[:5],
            'notifications': notifications,
            'upcoming_events': upcoming_events,
            'today': today,
        })

    # ── TEACHER dashboard ────────────────────
    if role == 'teacher':
        try:
            teacher = request.user.profile.teacher
        except Exception:
            teacher = None
        my_classes   = Classroom.objects.filter(homeroom_teacher=teacher) if teacher else Classroom.objects.none()
        my_students  = Student.objects.filter(classroom__in=my_classes, is_active=True) if teacher else Student.objects.none()
        today_att    = Attendance.objects.filter(date=today, student__in=my_students)
        return render(request, 'school/dashboard_teacher.html', {
            'role': role, 'teacher': teacher,
            'my_classes': my_classes,
            'my_students_count': my_students.count(),
            'today_present': today_att.filter(status='P').count(),
            'today_absent':  today_att.filter(status='A').count(),
            'today_late':    today_att.filter(status='L').count(),
            'recent_scores': Score.objects.filter(student__in=my_students).select_related('student','subject','exam_type').order_by('-date_recorded')[:5],
            'notifications': notifications,
            'upcoming_events': upcoming_events,
            'today': today,
        })

    # ── PARENT dashboard ─────────────────────
    if role == 'parent':
        try:
            student = request.user.profile.student
        except Exception:
            student = None
        att = student.attendances.order_by('-date')[:10] if student else []
        scores = student.scores.select_related('subject','exam_type').order_by('-date_recorded')[:10] if student else []
        return render(request, 'school/dashboard_parent.html', {
            'role': role, 'student': student,
            'attendances': att, 'scores': scores,
            'notifications': notifications,
            'upcoming_events': upcoming_events,
            'today': today,
        })

    # ── STUDENT dashboard ────────────────────
    try:
        student = request.user.profile.student
    except Exception:
        student = None
    att    = student.attendances.order_by('-date')[:5] if student else []
    scores = student.scores.select_related('subject','exam_type').order_by('-date_recorded')[:5] if student else []
    timetables = []
    if student and student.classroom:
        timetables = Timetable.objects.filter(
            classroom=student.classroom
        ).select_related('subject','teacher','time_slot').order_by('time_slot__day','time_slot__start_time')
    return render(request, 'school/dashboard_student.html', {
        'role': role, 'student': student,
        'attendances': att, 'scores': scores,
        'timetables': timetables,
        'notifications': notifications,
        'upcoming_events': upcoming_events,
        'today': today,
    })

# ══════════════════════════════════════════════
#  USER MANAGEMENT (Admin only)
# ══════════════════════════════════════════════
@admin_required
def user_list(request):
    # select_related avoids N+1 queries; profiles are guaranteed by the
    # ensure_user_profile context processor and post_save signal.
    users = User.objects.select_related('profile').order_by('username')
    # Safety net: create any missing profiles in a single pass
    missing = [u for u in users if not hasattr(u, 'profile') or u.profile is None]
    if missing:
        for u in missing:
            role = 'admin' if u.is_superuser else 'student'
            UserProfile.objects.get_or_create(user=u, defaults={'role': role})
        users = User.objects.select_related('profile').order_by('username')
    return render(request, 'school/users/user_list.html', {'users': users})

@admin_required
def user_add(request):
    form = UserCreateForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'អ្នកប្រើបានបង្កើតរួច។')
        return redirect('school:user_list')
    return render(request, 'school/users/user_add.html', {'form': form})

@admin_required
def user_delete(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        user.delete()
        messages.success(request, 'អ្នកប្រើបានលុបរួច។')
        return redirect('school:user_list')
    return render(request, 'school/confirm_delete.html', {
        'object': user, 'title': 'លុបអ្នកប្រើ', 'back_url': reverse('school:user_list')
    })

# ══════════════════════════════════════════════
#  STUDENTS (Admin: full CRUD | Teacher: view | Parent/Student: own only)
# ══════════════════════════════════════════════
@admin_or_teacher
def student_list(request):
    role = request.user.profile.role
    q = request.GET.get('q', '')
    classroom_id = request.GET.get('classroom', '')
    students = Student.objects.filter(is_active=True).select_related('classroom__grade')
    # Teacher sees only their class students
    if role == 'teacher':
        try:
            teacher = request.user.profile.teacher
            my_classes = Classroom.objects.filter(homeroom_teacher=teacher)
            students = students.filter(classroom__in=my_classes)
        except Exception:
            students = Student.objects.none()
    if q:
        students = students.filter(Q(first_name__icontains=q)|Q(last_name__icontains=q)|Q(student_id__icontains=q))
    if classroom_id:
        students = students.filter(classroom_id=classroom_id)
    classrooms = Classroom.objects.select_related('grade','academic_year')
    return render(request, 'school/student_list.html', {
        'students': students, 'q': q,
        'classrooms': classrooms, 'selected_classroom': classroom_id, 'role': role,
    })

@admin_or_teacher
def student_detail(request, pk):
    student = get_object_or_404(Student, pk=pk)
    attendances   = student.attendances.order_by('-date')[:10]
    scores        = student.scores.select_related('subject','exam_type','academic_year').order_by('-date_recorded')
    present_count = student.attendances.filter(status='P').count()
    absent_count  = student.attendances.filter(status='A').count()
    return render(request, 'school/student_detail.html', {
        'student': student, 'attendances': attendances, 'scores': scores,
        'present_count': present_count, 'absent_count': absent_count,
        'role': request.user.profile.role,
    })

@admin_required
def student_add(request):
    form = StudentForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        try:
            form.save()
            messages.success(request, 'សិស្សបានបន្ថែមរួច។')
            return redirect('school:student_list')
        except Exception as e:
            import traceback, logging
            logging.getLogger(__name__).error("student_add failed: %s\n%s", e, traceback.format_exc())
            messages.error(request, f'បញ្ហា: {e}')
    return render(request, 'school/form.html', {
        'form': form, 'title': 'បន្ថែមសិស្ស', 'back_url': reverse('school:student_list')
    })

@admin_required
def student_edit(request, pk):
    student = get_object_or_404(Student, pk=pk)
    form = StudentForm(request.POST or None, request.FILES or None, instance=student)
    if request.method == 'POST' and form.is_valid():
        try:
            form.save()
            messages.success(request, 'សិស្សបានកែប្រែ។')
            return redirect('school:student_detail', pk=pk)
        except Exception as e:
            import traceback, logging
            logging.getLogger(__name__).error("student_edit failed: %s\n%s", e, traceback.format_exc())
            messages.error(request, f'បញ្ហា: {e}')
    return render(request, 'school/form.html', {
        'form': form, 'title': 'កែប្រែសិស្ស',
        'subtitle': f'ID: {student.student_id}',
        'back_url': reverse('school:student_list'),
    })

@admin_required
def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        student.is_active = False
        student.save()
        messages.success(request, 'សិស្សបានដកចេញ។')
        return redirect('school:student_list')
    return render(request, 'school/confirm_delete.html', {
        'object': student, 'title': 'ដកសិស្ស', 'back_url': reverse('school:student_list')
    })

# ══════════════════════════════════════════════
#  TEACHERS (Admin: full CRUD | Teacher: view self)
# ══════════════════════════════════════════════
@admin_or_teacher
def teacher_list(request):
    q = request.GET.get('q', '')
    teachers = Teacher.objects.filter(is_active=True)
    if q:
        teachers = teachers.filter(Q(first_name__icontains=q)|Q(last_name__icontains=q)|Q(subject_specialty__icontains=q))
    return render(request, 'school/teacher_list.html', {
        'teachers': teachers, 'q': q, 'role': request.user.profile.role
    })

@admin_or_teacher
def teacher_detail(request, pk):
    teacher    = get_object_or_404(Teacher, pk=pk)
    subjects   = teacher.subjects.all()
    classes    = teacher.homeroom_classes.select_related('grade','academic_year')
    timetables = teacher.timetables.select_related('time_slot','subject','classroom').order_by('time_slot__day','time_slot__start_time')
    return render(request, 'school/teacher_detail.html', {
        'teacher': teacher, 'subjects': subjects,
        'classes': classes, 'timetables': timetables,
        'role': request.user.profile.role,
    })

@admin_required
def teacher_add(request):
    form = TeacherForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        try:
            form.save()
            messages.success(request, 'គ្រូបានបន្ថែមរួច។')
            return redirect('school:teacher_list')
        except Exception as e:
            import traceback, logging
            logging.getLogger(__name__).error("teacher_add failed: %s\n%s", e, traceback.format_exc())
            messages.error(request, f'បញ្ហា: {e}')
    return render(request, 'school/form.html', {
        'form': form, 'title': 'បន្ថែមគ្រូ', 'back_url': reverse('school:teacher_list')
    })

@admin_required
def teacher_edit(request, pk):
    teacher = get_object_or_404(Teacher, pk=pk)
    form = TeacherForm(request.POST or None, request.FILES or None, instance=teacher)
    if request.method == 'POST' and form.is_valid():
        try:
            form.save()
            messages.success(request, 'គ្រូបានកែប្រែ។')
            return redirect('school:teacher_detail', pk=pk)
        except Exception as e:
            import traceback, logging
            logging.getLogger(__name__).error("teacher_edit failed: %s\n%s", e, traceback.format_exc())
            messages.error(request, f'បញ្ហា: {e}')
    return render(request, 'school/form.html', {
        'form': form, 'title': 'កែប្រែគ្រូ',
        'subtitle': f'ID: {teacher.teacher_id}',
        'back_url': reverse('school:teacher_list'),
    })

@admin_required
def teacher_delete(request, pk):
    teacher = get_object_or_404(Teacher, pk=pk)
    if request.method == 'POST':
        teacher.delete()
        messages.success(request, 'គ្រូបានលុប។')
        return redirect('school:teacher_list')
    return render(request, 'school/confirm_delete.html', {
        'object': teacher, 'title': 'លុបគ្រូ', 'back_url': reverse('school:teacher_list')
    })

# ══════════════════════════════════════════════
#  CLASSROOMS & SUBJECTS (Admin only)
# ══════════════════════════════════════════════

# ══════════════════════════════════════════════
#  ACADEMIC YEAR
# ══════════════════════════════════════════════
@admin_required
def academic_year_list(request):
    years = AcademicYear.objects.all()
    return render(request, 'school/academic_year_list.html', {'years': years})

@admin_required
def academic_year_add(request):
    form = AcademicYearForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'ឆ្នាំសិក្សាបានបន្ថែម។')
        return redirect('school:academic_year_list')
    return render(request, 'school/form.html', {
        'form': form, 'title': 'បន្ថែមឆ្នាំសិក្សា',
        'back_url': reverse('school:academic_year_list')
    })

@admin_required
def academic_year_edit(request, pk):
    year = get_object_or_404(AcademicYear, pk=pk)
    form = AcademicYearForm(request.POST or None, instance=year)
    if form.is_valid():
        form.save()
        messages.success(request, 'ឆ្នាំសិក្សាបានកែប្រែ។')
        return redirect('school:academic_year_list')
    return render(request, 'school/form.html', {
        'form': form, 'title': 'កែប្រែឆ្នាំសិក្សា',
        'back_url': reverse('school:academic_year_list')
    })

@admin_required
def academic_year_delete(request, pk):
    year = get_object_or_404(AcademicYear, pk=pk)
    if request.method == 'POST':
        year.delete()
        messages.success(request, 'ឆ្នាំសិក្សាបានលុប។')
        return redirect('school:academic_year_list')
    return render(request, 'school/confirm_delete.html', {
        'object': year, 'title': 'លុបឆ្នាំសិក្សា',
        'back_url': reverse('school:academic_year_list')
    })

@admin_required
def academic_year_set_active(request, pk):
    AcademicYear.objects.all().update(is_active=False)
    AcademicYear.objects.filter(pk=pk).update(is_active=True)
    messages.success(request, 'ឆ្នាំសិក្សាសកម្មបានកំណត់។')
    return redirect('school:academic_year_list')

@admin_required
def academic_year_generate(request):
    """Generate multiple academic years at once."""
    if request.method == 'POST':
        base_year = int(request.POST.get('base_year', timezone.now().year))
        count = int(request.POST.get('count', 5))
        count = max(1, min(20, count))  # limit 1-20
        
        created_count = 0
        existing_count = 0
        
        for i in range(count):
            year_str = f"{base_year + i}-{base_year + i + 1}"
            obj, created = AcademicYear.objects.get_or_create(
                year=year_str,
                defaults={'is_active': False}
            )
            if created:
                created_count += 1
            else:
                existing_count += 1
        
        # Set first year as active if no active year exists
        if not AcademicYear.objects.filter(is_active=True).exists():
            first_year = AcademicYear.objects.order_by('year').first()
            if first_year:
                first_year.is_active = True
                first_year.save()
        
        if created_count > 0:
            messages.success(request, f'បានបង្កើតឆ្នាំសិក្សា {created_count} ឆ្នាំ។')
        if existing_count > 0:
            messages.info(request, f'{existing_count} ឆ្នាំមានរួចហើយ។')
        
        return redirect('school:academic_year_list')
    
    return redirect('school:academic_year_list')

# ══════════════════════════════════════════════
@admin_or_teacher
def classroom_list(request):
    classrooms = Classroom.objects.select_related('grade','homeroom_teacher','academic_year').annotate(student_count=Count('students'))
    return render(request, 'school/classroom_list.html', {'classrooms': classrooms, 'role': request.user.profile.role})

@admin_required
def classroom_add(request):
    form = ClassroomForm(request.POST or None)
    if form.is_valid():
        form.save(); messages.success(request, 'ថ្នាក់បានបន្ថែម។')
        return redirect('school:classroom_list')
    return render(request, 'school/form.html', {'form': form, 'title': 'បន្ថែមថ្នាក់', 'back_url': reverse('school:classroom_list')})

@admin_required
def classroom_edit(request, pk):
    classroom = get_object_or_404(Classroom, pk=pk)
    form = ClassroomForm(request.POST or None, instance=classroom)
    if form.is_valid():
        form.save(); messages.success(request, 'ថ្នាក់បានកែប្រែ។')
        return redirect('school:classroom_list')
    return render(request, 'school/form.html', {'form': form, 'title': 'កែប្រែថ្នាក់', 'back_url': reverse('school:classroom_list')})

@admin_required
def classroom_delete(request, pk):
    classroom = get_object_or_404(Classroom, pk=pk)
    if request.method == 'POST':
        classroom.delete(); messages.success(request, 'ថ្នាក់បានលុប។')
        return redirect('school:classroom_list')
    return render(request, 'school/confirm_delete.html', {'object': classroom, 'title': 'លុបថ្នាក់', 'back_url': reverse('school:classroom_list')})

@admin_or_teacher
def subject_list(request):
    subjects = Subject.objects.select_related('teacher','grade')
    return render(request, 'school/subject_list.html', {'subjects': subjects, 'role': request.user.profile.role})

@admin_required
def subject_add(request):
    form = SubjectForm(request.POST or None)
    if form.is_valid():
        form.save(); messages.success(request, 'មុខវិជ្ជាបានបន្ថែម។')
        return redirect('school:subject_list')
    return render(request, 'school/form.html', {'form': form, 'title': 'បន្ថែមមុខវិជ្ជា', 'back_url': reverse('school:subject_list')})

@admin_required
def subject_edit(request, pk):
    subject = get_object_or_404(Subject, pk=pk)
    form = SubjectForm(request.POST or None, instance=subject)
    if form.is_valid():
        form.save(); messages.success(request, 'មុខវិជ្ជាបានកែប្រែ។')
        return redirect('school:subject_list')
    return render(request, 'school/form.html', {'form': form, 'title': 'កែប្រែមុខវិជ្ជា', 'back_url': reverse('school:subject_list')})

@admin_required
def subject_delete(request, pk):
    subject = get_object_or_404(Subject, pk=pk)
    if request.method == 'POST':
        subject.delete(); messages.success(request, 'មុខវិជ្ជាបានលុប។')
        return redirect('school:subject_list')
    return render(request, 'school/confirm_delete.html', {'object': subject, 'title': 'លុបមុខវិជ្ជា', 'back_url': reverse('school:subject_list')})

# ══════════════════════════════════════════════
#  ATTENDANCE (Admin+Teacher: record | Parent+Student: view own)
# ══════════════════════════════════════════════
@admin_or_teacher
def attendance_list(request):
    today        = timezone.now().date()
    date_filter  = request.GET.get('date', str(today))
    classroom_id = request.GET.get('classroom', '')
    role         = request.user.profile.role
    records = Attendance.objects.filter(date=date_filter).select_related('student__classroom__grade')
    if role == 'teacher':
        try:
            teacher    = request.user.profile.teacher
            my_classes = Classroom.objects.filter(homeroom_teacher=teacher)
            records    = records.filter(student__classroom__in=my_classes)
        except Exception:
            records = Attendance.objects.none()
    elif classroom_id:
        records = records.filter(student__classroom_id=classroom_id)
    classrooms = Classroom.objects.select_related('grade','academic_year')
    return render(request, 'school/attendance_list.html', {
        'records': records, 'date_filter': date_filter,
        'classrooms': classrooms, 'selected_classroom': classroom_id,
        'present': records.filter(status='P').count(),
        'absent':  records.filter(status='A').count(),
        'late':    records.filter(status='L').count(),
        'role': role,
    })

@admin_or_teacher
def attendance_add(request):
    form = AttendanceForm(request.POST or None)
    if form.is_valid():
        form.save(); messages.success(request, 'វត្តមានបានកត់ត្រា។')
        return redirect('school:attendance_list')
    return render(request, 'school/form.html', {'form': form, 'title': 'កត់ត្រាវត្តមាន', 'back_url': reverse('school:attendance_list')})

@admin_or_teacher
def attendance_bulk(request):
    classroom = None
    students  = []
    date_val  = timezone.now().date()
    if request.method == 'POST':
        classroom_id = request.POST.get('classroom')
        date_val     = request.POST.get('date')
        classroom    = get_object_or_404(Classroom, pk=classroom_id)
        students     = classroom.students.filter(is_active=True).order_by('last_name')
        if 'save_attendance' in request.POST:
            for student in students:
                status = request.POST.get(f'status_{student.pk}', 'P')
                note   = request.POST.get(f'note_{student.pk}', '')
                Attendance.objects.update_or_create(
                    student=student, date=date_val,
                    defaults={'status': status, 'note': note}
                )
            messages.success(request, f'វត្តមានបានរក្សាទុក — {classroom} — {date_val}')
            return redirect('school:attendance_list')
    classrooms = Classroom.objects.select_related('grade','academic_year')
    return render(request, 'school/attendance_bulk.html', {
        'classrooms': classrooms, 'classroom': classroom,
        'students': students, 'date_val': date_val,
        'status_choices': Attendance.STATUS_CHOICES,
    })

# ── Parent view child attendance ───────────────
@role_required('parent')
def parent_child_attendance(request):
    try:
        student = request.user.profile.student
    except Exception:
        student = None
    attendances = student.attendances.order_by('-date') if student else []
    present = student.attendances.filter(status='P').count() if student else 0
    absent  = student.attendances.filter(status='A').count() if student else 0
    return render(request, 'school/parent/child_attendance.html', {
        'student': student, 'attendances': attendances,
        'present': present, 'absent': absent,
    })

# ── Student view own attendance ────────────────
@role_required('student')
def student_my_attendance(request):
    try:
        student = request.user.profile.student
    except Exception:
        student = None
    attendances = student.attendances.order_by('-date') if student else []
    return render(request, 'school/student/my_attendance.html', {
        'student': student, 'attendances': attendances,
    })


# ══════════════════════════════════════════════
#  TEACHER ATTENDANCE (Admin: full | Teacher: view own)
# ══════════════════════════════════════════════
@admin_or_teacher
def teacher_attendance_list(request):
    today       = timezone.now().date()
    date_filter = request.GET.get('date', str(today))
    role        = request.user.profile.role
    records = TeacherAttendance.objects.filter(date=date_filter).select_related('teacher')
    if role == 'teacher':
        try:
            teacher = request.user.profile.teacher
            records = records.filter(teacher=teacher)
        except Exception:
            records = TeacherAttendance.objects.none()
    return render(request, 'school/teacher_attendance_list.html', {
        'records':      records,
        'date_filter':  date_filter,
        'present':      records.filter(status='P').count(),
        'absent':       records.filter(status='A').count(),
        'late':         records.filter(status='L').count(),
        'role':         role,
    })


@admin_required
def teacher_attendance_add(request):
    form = TeacherAttendanceForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'វត្តមានគ្រូបានកត់ត្រា។')
        return redirect('school:teacher_attendance_list')
    return render(request, 'school/form.html', {
        'form': form, 'title': 'កត់ត្រាវត្តមានគ្រូ',
        'back_url': reverse('school:teacher_attendance_list')
    })


@admin_required
def teacher_attendance_bulk(request):
    """Record attendance for all active teachers at once."""
    date_val = timezone.now().date()
    teachers = []
    if request.method == 'POST':
        date_val = request.POST.get('date', str(date_val))
        if 'save_attendance' in request.POST:
            active_teachers = Teacher.objects.filter(is_active=True).order_by('last_name', 'first_name')
            for teacher in active_teachers:
                status = request.POST.get(f'status_{teacher.pk}', 'P')
                note   = request.POST.get(f'note_{teacher.pk}', '')
                TeacherAttendance.objects.update_or_create(
                    teacher=teacher, date=date_val,
                    defaults={'status': status, 'note': note}
                )
            messages.success(request, f'វត្តមានគ្រូបានរក្សាទុក — {date_val}')
            return redirect('school:teacher_attendance_list')
        else:
            teachers = Teacher.objects.filter(is_active=True).order_by('last_name', 'first_name')
    return render(request, 'school/teacher_attendance_bulk.html', {
        'teachers':       teachers,
        'date_val':       date_val,
        'status_choices': TeacherAttendance.STATUS_CHOICES,
    })

# ══════════════════════════════════════════════
#  EXAMS & SCORES (Admin+Teacher: manage | Parent+Student: view)
# ══════════════════════════════════════════════
@admin_or_teacher
def exam_list(request):
    exams = Exam.objects.select_related('subject','classroom','exam_type','academic_year').order_by('-date')
    return render(request, 'school/exam_list.html', {'exams': exams, 'role': request.user.profile.role})

@admin_or_teacher
def exam_add(request):
    form = ExamForm(request.POST or None)
    if form.is_valid():
        form.save(); messages.success(request, 'ការប្រឡងបានបន្ថែម។')
        return redirect('school:exam_list')
    return render(request, 'school/form.html', {'form': form, 'title': 'បន្ថែមការប្រឡង', 'back_url': reverse('school:exam_list')})

@admin_or_teacher
def exam_edit(request, pk):
    exam = get_object_or_404(Exam, pk=pk)
    form = ExamForm(request.POST or None, instance=exam)
    if form.is_valid():
        form.save(); messages.success(request, 'ការប្រឡងបានកែប្រែ។')
        return redirect('school:exam_list')
    return render(request, 'school/form.html', {'form': form, 'title': 'កែប្រែការប្រឡង', 'back_url': reverse('school:exam_list')})

@admin_required
def exam_delete(request, pk):
    exam = get_object_or_404(Exam, pk=pk)
    if request.method == 'POST':
        exam.delete(); messages.success(request, 'ការប្រឡងបានលុប។')
        return redirect('school:exam_list')
    return render(request, 'school/confirm_delete.html', {'object': exam, 'title': 'លុបការប្រឡង', 'back_url': reverse('school:exam_list')})

@admin_or_teacher
def score_list(request):
    role = request.user.profile.role
    q    = request.GET.get('q','')
    scores = Score.objects.select_related('student','subject','exam_type','academic_year')
    if role == 'teacher':
        try:
            teacher    = request.user.profile.teacher
            my_classes = Classroom.objects.filter(homeroom_teacher=teacher)
            scores     = scores.filter(student__classroom__in=my_classes)
        except Exception:
            scores = Score.objects.none()
    if q:
        scores = scores.filter(Q(student__first_name__icontains=q)|Q(student__last_name__icontains=q)|Q(student__student_id__icontains=q))
    return render(request, 'school/score_list.html', {'scores': scores, 'q': q, 'role': role})

@admin_or_teacher
def score_add(request):
    form = ScoreForm(request.POST or None)
    if form.is_valid():
        form.save(); messages.success(request, 'ពិន្ទុបានកត់ត្រា។')
        return redirect('school:score_list')
    return render(request, 'school/form.html', {'form': form, 'title': 'បន្ថែមពិន្ទុ', 'back_url': reverse('school:score_list')})

@admin_or_teacher
def score_edit(request, pk):
    score = get_object_or_404(Score, pk=pk)
    form  = ScoreForm(request.POST or None, instance=score)
    if form.is_valid():
        form.save(); messages.success(request, 'ពិន្ទុបានកែប្រែ។')
        return redirect('school:score_list')
    return render(request, 'school/form.html', {'form': form, 'title': 'កែប្រែពិន្ទុ', 'back_url': reverse('school:score_list')})

@admin_required
def score_delete(request, pk):
    score = get_object_or_404(Score, pk=pk)
    if request.method == 'POST':
        score.delete(); messages.success(request, 'ពិន្ទុបានលុប។')
        return redirect('school:score_list')
    return render(request, 'school/confirm_delete.html', {'object': score, 'title': 'លុបពិន្ទុ', 'back_url': reverse('school:score_list')})

# ── Parent/Student view results ────────────────
@role_required('parent')
def parent_child_results(request):
    try:
        student = request.user.profile.student
    except Exception:
        student = None
    scores = student.scores.select_related('subject','exam_type','academic_year').order_by('subject__name') if student else []
    return render(request, 'school/parent/child_results.html', {'student': student, 'scores': scores})

@role_required('student')
def student_my_results(request):
    try:
        student = request.user.profile.student
    except Exception:
        student = None
    scores = student.scores.select_related('subject','exam_type','academic_year').order_by('subject__name') if student else []
    return render(request, 'school/student/my_results.html', {'student': student, 'scores': scores})

# ══════════════════════════════════════════════
#  TIMETABLE (Admin: manage | Teacher+Student: view)
# ══════════════════════════════════════════════
@login_required
def timetable_list(request):
    role         = request.user.profile.role
    classroom_id = request.GET.get('classroom','')
    year_id      = request.GET.get('year','')
    classrooms   = Classroom.objects.select_related('grade','academic_year')
    years        = AcademicYear.objects.all()
    timetables   = Timetable.objects.select_related('subject','teacher','time_slot','classroom__grade').order_by('time_slot__day','time_slot__start_time')
    # Student auto-filter to their class
    if role == 'student':
        try:
            student = request.user.profile.student
            if student and student.classroom:
                timetables = timetables.filter(classroom=student.classroom)
        except Exception:
            pass
    else:
        if classroom_id:
            timetables = timetables.filter(classroom_id=classroom_id)
        if year_id:
            timetables = timetables.filter(academic_year_id=year_id)
    days = {}
    for tt in timetables:
        days.setdefault(tt.time_slot.day, []).append(tt)
    day_names = {1:'ចន្ទ', 2:'អង្គារ', 3:'ពុធ', 4:'ព្រហស្បតិ៍', 5:'សុក្រ', 6:'សៅរ៍'}
    return render(request, 'school/timetable_list.html', {
        'timetables': timetables, 'classrooms': classrooms,
        'years': years, 'days': days, 'day_names': day_names,
        'selected_classroom': classroom_id, 'selected_year': year_id, 'role': role,
    })

@admin_required
def timetable_add(request):
    form = TimetableForm(request.POST or None)
    if form.is_valid():
        form.save(); messages.success(request, 'តារាងម៉ោងបានបន្ថែម។')
        return redirect('school:timetable_list')
    return render(request, 'school/form.html', {'form': form, 'title': 'បន្ថែមតារាងម៉ោង', 'back_url': reverse('school:timetable_list')})

@admin_required
def timetable_edit(request, pk):
    tt   = get_object_or_404(Timetable, pk=pk)
    form = TimetableForm(request.POST or None, instance=tt)
    if form.is_valid():
        form.save(); messages.success(request, 'តារាងម៉ោងបានកែប្រែ។')
        return redirect('school:timetable_list')
    return render(request, 'school/form.html', {'form': form, 'title': 'កែប្រែតារាងម៉ោង', 'back_url': reverse('school:timetable_list')})

@admin_required
def timetable_delete(request, pk):
    tt = get_object_or_404(Timetable, pk=pk)
    if request.method == 'POST':
        tt.delete(); messages.success(request, 'តារាងម៉ោងបានលុប។')
        return redirect('school:timetable_list')
    return render(request, 'school/confirm_delete.html', {'object': tt, 'title': 'លុបតារាងម៉ោង', 'back_url': reverse('school:timetable_list')})

# ══════════════════════════════════════════════
#  NOTIFICATIONS (Admin+Teacher: manage | All: receive)
# ══════════════════════════════════════════════
@login_required
def notification_list(request):
    role = request.user.profile.role
    notifs = Notification.objects.select_related('created_by').filter(is_active=True)
    # Filter by audience
    if role == 'teacher':
        notifs = notifs.filter(audience__in=['all','teachers'])
    elif role == 'parent':
        notifs = notifs.filter(audience__in=['all','parents'])
    elif role == 'student':
        notifs = notifs.filter(audience__in=['all','students'])
    return render(request, 'school/notification_list.html', {
        'notifications': notifs.order_by('-created_at'), 'role': role
    })

@admin_or_teacher
def notification_add(request):
    form = NotificationForm(request.POST or None)
    if form.is_valid():
        notif = form.save(commit=False)
        notif.created_by = request.user
        notif.save()
        messages.success(request, 'សេចក្ដីជូនដំណឹងបានផ្ញើ។')
        return redirect('school:notification_list')
    return render(request, 'school/form.html', {'form': form, 'title': 'ផ្ញើសេចក្ដីជូនដំណឹង', 'back_url': reverse('school:notification_list')})

@admin_or_teacher
def notification_edit(request, pk):
    notif = get_object_or_404(Notification, pk=pk)
    form  = NotificationForm(request.POST or None, instance=notif)
    if form.is_valid():
        form.save(); messages.success(request, 'សេចក្ដីជូនដំណឹងបានកែប្រែ។')
        return redirect('school:notification_list')
    return render(request, 'school/form.html', {'form': form, 'title': 'កែប្រែ', 'back_url': reverse('school:notification_list')})

@admin_required
def notification_delete(request, pk):
    notif = get_object_or_404(Notification, pk=pk)
    if request.method == 'POST':
        notif.delete(); messages.success(request, 'បានលុប។')
        return redirect('school:notification_list')
    return render(request, 'school/confirm_delete.html', {'object': notif, 'title': 'លុបសេចក្ដីជូនដំណឹង', 'back_url': reverse('school:notification_list')})

# ══════════════════════════════════════════════
#  EVENTS (Admin: manage | All: view)
# ══════════════════════════════════════════════
@login_required
def event_list(request):
    events = SchoolEvent.objects.order_by('start_date')
    return render(request, 'school/event_list.html', {'events': events, 'role': request.user.profile.role})

@admin_required
def event_add(request):
    form = SchoolEventForm(request.POST or None)
    if form.is_valid():
        ev = form.save(commit=False); ev.created_by = request.user; ev.save()
        messages.success(request, 'ព្រឹត្តិការណ៍បានបន្ថែម។')
        return redirect('school:event_list')
    return render(request, 'school/form.html', {'form': form, 'title': 'បន្ថែមព្រឹត្តិការណ៍', 'back_url': reverse('school:event_list')})

@admin_required
def event_edit(request, pk):
    ev   = get_object_or_404(SchoolEvent, pk=pk)
    form = SchoolEventForm(request.POST or None, instance=ev)
    if form.is_valid():
        form.save(); messages.success(request, 'ព្រឹត្តិការណ៍បានកែប្រែ។')
        return redirect('school:event_list')
    return render(request, 'school/form.html', {'form': form, 'title': 'កែប្រែព្រឹត្តិការណ៍', 'back_url': reverse('school:event_list')})

@admin_required
def event_delete(request, pk):
    ev = get_object_or_404(SchoolEvent, pk=pk)
    if request.method == 'POST':
        ev.delete(); messages.success(request, 'ព្រឹត្តិការណ៍បានលុប។')
        return redirect('school:event_list')
    return render(request, 'school/confirm_delete.html', {'object': ev, 'title': 'លុបព្រឹត្តិការណ៍', 'back_url': reverse('school:event_list')})

# ══════════════════════════════════════════════
#  REPORT CARDS (Admin+Teacher: manage | Parent+Student: view)
# ══════════════════════════════════════════════
@admin_or_teacher
def report_card_list(request):
    role = request.user.profile.role
    cards = ReportCard.objects.select_related('student__classroom__grade','academic_year').order_by('-generated_at')
    if role == 'teacher':
        try:
            teacher    = request.user.profile.teacher
            my_classes = Classroom.objects.filter(homeroom_teacher=teacher)
            cards      = cards.filter(student__classroom__in=my_classes)
        except Exception:
            cards = ReportCard.objects.none()
    return render(request, 'school/report_card_list.html', {'cards': cards, 'role': role})

@admin_or_teacher
def report_card_add(request):
    form = ReportCardForm(request.POST or None)
    if form.is_valid():
        card = form.save(commit=False); card.generated_by = request.user; card.save()
        messages.success(request, 'សៀវភៅប័ណ្ណបានបង្កើត។')
        return redirect('school:report_card_list')
    return render(request, 'school/form.html', {'form': form, 'title': 'បង្កើតសៀវភៅប័ណ្ណ', 'back_url': reverse('school:report_card_list')})

@login_required
def report_card_view(request, pk):
    card    = get_object_or_404(ReportCard, pk=pk)
    # Parent/Student can only view their own child/self
    role = request.user.profile.role
    if role == 'parent' or role == 'student':
        try:
            my_student = request.user.profile.student
            if card.student != my_student:
                messages.error(request, 'អ្នកមិនមានសិទ្ធិមើលប័ណ្ណនេះ។')
                return redirect('school:dashboard')
        except Exception:
            return redirect('school:dashboard')
    student      = card.student
    scores       = student.scores.filter(academic_year=card.academic_year).select_related('subject','exam_type').order_by('subject__name')
    present_days = card.attendance_days - card.absent_days
    avg_score    = scores.aggregate(avg=Avg('score'))['avg'] or 0
    return render(request, 'school/report_card_print.html', {
        'card': card, 'student': student, 'scores': scores,
        'total_att': card.attendance_days, 'absent_days': card.absent_days,
        'present_days': present_days, 'avg_score': round(avg_score, 2),
        'today': timezone.now().date(),
    })

@admin_required
def report_card_delete(request, pk):
    card = get_object_or_404(ReportCard, pk=pk)
    if request.method == 'POST':
        card.delete(); messages.success(request, 'សៀវភៅប័ណ្ណបានលុប។')
        return redirect('school:report_card_list')
    return render(request, 'school/confirm_delete.html', {'object': card, 'title': 'លុបសៀវភៅប័ណ្ណ', 'back_url': reverse('school:report_card_list')})

# ══════════════════════════════════════════════
#  PRINT REPORTS (Admin: all | Teacher: own class)
# ══════════════════════════════════════════════
@admin_or_teacher
def report_students(request):
    role = request.user.profile.role
    students = Student.objects.filter(is_active=True).select_related('classroom__grade').order_by('student_id')
    if role == 'teacher':
        try:
            teacher    = request.user.profile.teacher
            my_classes = Classroom.objects.filter(homeroom_teacher=teacher)
            students   = students.filter(classroom__in=my_classes)
        except Exception:
            students = Student.objects.none()
    return render(request, 'school/reports/report_students.html', {'students': students, 'today': timezone.now().date()})

@admin_required
def report_teachers(request):
    teachers = Teacher.objects.filter(is_active=True).order_by('teacher_id')
    return render(request, 'school/reports/report_teachers.html', {'teachers': teachers, 'today': timezone.now().date()})

@admin_or_teacher
def report_attendance(request):
    today       = timezone.now().date()
    date_filter = request.GET.get('date', str(today))
    records     = Attendance.objects.filter(date=date_filter).select_related('student').order_by('student__student_id')
    return render(request, 'school/reports/report_attendance.html', {
        'records': records, 'date_filter': date_filter,
        'present': records.filter(status='P').count(),
        'absent':  records.filter(status='A').count(),
        'late':    records.filter(status='L').count(),
        'excused': records.filter(status='E').count(),
        'today': today,
    })

@admin_or_teacher
def report_scores(request):
    academic_year_id = request.GET.get('year','')
    years  = AcademicYear.objects.all()
    scores = Score.objects.select_related('student','subject','exam_type','academic_year')
    selected_year = None
    if academic_year_id:
        scores        = scores.filter(academic_year_id=academic_year_id)
        selected_year = AcademicYear.objects.filter(pk=academic_year_id).first()
    return render(request, 'school/reports/report_scores.html', {
        'scores': scores, 'years': years,
        'selected_year': selected_year, 'today': timezone.now().date(),
    })

@admin_or_teacher
def report_student_detail(request, pk):
    student       = get_object_or_404(Student, pk=pk)
    attendances   = student.attendances.order_by('-date')
    scores        = student.scores.select_related('subject','exam_type','academic_year').order_by('subject__name')
    present_count = attendances.filter(status='P').count()
    absent_count  = attendances.filter(status='A').count()
    return render(request, 'school/reports/report_student_detail.html', {
        'student': student, 'attendances': attendances, 'scores': scores,
        'present_count': present_count, 'absent_count': absent_count,
        'today': timezone.now().date(),
    })
