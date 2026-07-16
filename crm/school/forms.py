from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from .models import (
    Student, Teacher, Classroom, Attendance, TeacherAttendance, Score, Subject,
    Grade, AcademicYear, ExamType, Exam, Timetable, TimeSlot,
    Notification, ReportCard, SchoolEvent, UserProfile
)


class PhotoInput(forms.FileInput):
    """
    Plain FileInput — no 'Clear' checkbox, no accidental image deletion.
    The existing image is preserved when the user submits without choosing a new file.
    """
    pass


# ── Custom widget mixin ─────────────────────────────────────────
class BootstrapMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            cls = field.widget.__class__.__name__
            if cls in ('TextInput', 'EmailInput', 'NumberInput',
                       'PasswordInput', 'URLInput', 'DateInput',
                       'TimeInput', 'DateTimeInput', 'Textarea'):
                field.widget.attrs.setdefault('class', 'form-control')
            elif cls in ('Select', 'SelectMultiple'):
                field.widget.attrs.setdefault('class', 'form-select')
            elif cls == 'CheckboxInput':
                field.widget.attrs.setdefault('class', 'form-check-input')
            elif cls == 'FileInput':
                field.widget.attrs.setdefault('class', 'form-control')
            elif cls == 'PhotoInput':
                field.widget.attrs.setdefault('class', 'form-control')


# ── Login Form ──────────────────────────────────────────────────
class LoginForm(BootstrapMixin, AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Username', 'autofocus': True})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'})
    )


# ── User Profile Form ───────────────────────────────────────────
class UserProfileForm(BootstrapMixin, forms.ModelForm):
    class Meta:
        model  = UserProfile
        fields = ['role', 'phone', 'photo', 'teacher', 'student']


class ProfileUpdateForm(BootstrapMixin, forms.ModelForm):
    """Form for any logged-in user to update their own profile."""
    first_name = forms.CharField(max_length=150, required=False, label='ឈ្មោះដំបូង')
    last_name  = forms.CharField(max_length=150, required=False, label='នាមត្រកូល')
    email      = forms.EmailField(required=False, label='អ៊ីម៉ែល')

    class Meta:
        model  = UserProfile
        fields = ['phone', 'photo']
        labels = {'phone': 'ទូរស័ព្ទ', 'photo': 'រូបភាពប្រវត្តិរូប'}
        widgets = {'photo': PhotoInput()}

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['first_name'].initial = user.first_name
            self.fields['last_name'].initial  = user.last_name
            self.fields['email'].initial      = user.email

    def save_user(self, user, commit=True):
        user.first_name = self.cleaned_data.get('first_name', '')
        user.last_name  = self.cleaned_data.get('last_name', '')
        user.email      = self.cleaned_data.get('email', '')
        if commit:
            user.save()
        return user


class UserCreateForm(BootstrapMixin, forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)
    role      = forms.ChoiceField(choices=UserProfile.ROLE_CHOICES)

    class Meta:
        model  = User
        fields = ['username', 'first_name', 'last_name', 'email']

    def clean(self):
        cleaned = super().clean()
        p1 = cleaned.get('password1')
        p2 = cleaned.get('password2')
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError('Passwords do not match.')
        return cleaned

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
            # Signal may have already created the profile — use update_or_create
            UserProfile.objects.update_or_create(
                user=user,
                defaults={'role': self.cleaned_data['role']}
            )
        return user


# ── Student Form ────────────────────────────────────────────────
class StudentForm(BootstrapMixin, forms.ModelForm):
    class Meta:
        model  = Student
        fields = [
            'first_name', 'last_name',
            'first_name_en', 'last_name_en',
            'gender', 'date_of_birth',
            'address', 'phone', 'parent_name', 'parent_phone', 'parent_email',
            'classroom', 'photo', 'is_active', 'blood_group', 'medical_notes'
        ]
        labels = {
            'first_name':    'នាមខ្លួន (ខ្មែរ)',
            'last_name':     'នាមត្រកូល (ខ្មែរ)',
            'first_name_en': 'First Name (English)',
            'last_name_en':  'Last Name (English)',
        }
        widgets = {
            'date_of_birth':  forms.DateInput(attrs={'type': 'date'}),
            'address':        forms.Textarea(attrs={'rows': 2}),
            'medical_notes':  forms.Textarea(attrs={'rows': 2}),
            'photo':          PhotoInput(),
        }


# ── Teacher Form ────────────────────────────────────────────────
class TeacherForm(BootstrapMixin, forms.ModelForm):
    # Add fields for creating a user account
    create_account = forms.BooleanField(
        required=False, 
        initial=True,
        label='បង្កើតគណនីអ្នកប្រើ (Create User Account)',
        help_text='បើធីកនឹងបង្កើតគណនីដើម្បីឱ្យគ្រូអាចចូលប្រព័ន្ធបាន'
    )
    username = forms.CharField(
        max_length=150, 
        required=False,
        label='ឈ្មោះអ្នកប្រើ (Username)',
        help_text='បើទុកទទេ នឹងប្រើឈ្មោះអ្នកប្រើដោយស្វ័យប្រវត្តិ'
    )
    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput,
        label='ពាក្យសម្ងាត់ (Password)',
        help_text='បើទុកទទេ នឹងប្រើពាក្យសម្ងាត់លំនាំដើម: teacher123'
    )
    
    class Meta:
        model  = Teacher
        fields = [
            'first_name', 'last_name',
            'first_name_en', 'last_name_en',
            'gender', 'phone', 'email',
            'address', 'subject_specialty', 'hire_date', 'photo',
            'qualification', 'is_active'
        ]
        labels = {
            'first_name':    'នាមខ្លួន (ខ្មែរ)',
            'last_name':     'នាមត្រកូល (ខ្មែរ)',
            'first_name_en': 'First Name (English)',
            'last_name_en':  'Last Name (English)',
        }
        widgets = {
            'hire_date': forms.DateInput(attrs={'type': 'date'}),
            'address':   forms.Textarea(attrs={'rows': 2}),
            'photo':     PhotoInput(),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # If editing existing teacher, check if user account already exists
        if self.instance.pk:
            try:
                profile = UserProfile.objects.get(teacher=self.instance)
                self.fields['create_account'].initial = False
                self.fields['create_account'].help_text = f'គណនីមានរួចហើយ: {profile.user.username}'
                self.fields['username'].widget.attrs['readonly'] = True
                self.fields['password'].widget.attrs['readonly'] = True
            except UserProfile.DoesNotExist:
                pass
    
    def save(self, commit=True):
        teacher = super().save(commit=commit)
        
        # Create user account if requested and teacher is being created (not edited)
        if commit and self.cleaned_data.get('create_account'):
            # Check if teacher already has a user account
            existing_profile = UserProfile.objects.filter(teacher=teacher).first()
            
            if not existing_profile:
                # Generate username from teacher name
                username = self.cleaned_data.get('username') or f"{teacher.first_name_en or teacher.first_name}{teacher.last_name_en or teacher.last_name}".replace(' ', '').lower()
                
                # Make username unique if it already exists
                base_username = username
                counter = 1
                while User.objects.filter(username=username).exists():
                    username = f"{base_username}{counter}"
                    counter += 1
                
                # Get password or use default
                password = self.cleaned_data.get('password') or 'teacher123'
                
                # Create user
                user = User.objects.create_user(
                    username=username,
                    password=password,
                    first_name=teacher.first_name,
                    last_name=teacher.last_name,
                    email=teacher.email or ''
                )
                
                # Link user profile to teacher
                UserProfile.objects.update_or_create(
                    user=user,
                    defaults={'role': 'teacher', 'teacher': teacher, 'phone': teacher.phone}
                )
        
        return teacher


# ── Classroom Form ──────────────────────────────────────────────
class ClassroomForm(BootstrapMixin, forms.ModelForm):
    class Meta:
        model  = Classroom
        fields = ['grade', 'homeroom_teacher', 'academic_year', 'room_number', 'capacity']


# ── Attendance Forms ────────────────────────────────────────────
class AttendanceForm(BootstrapMixin, forms.ModelForm):
    class Meta:
        model  = Attendance
        fields = ['student', 'date', 'status', 'note']
        widgets = {'date': forms.DateInput(attrs={'type': 'date'})}


class BulkAttendanceForm(BootstrapMixin, forms.Form):
    classroom = forms.ModelChoiceField(queryset=Classroom.objects.all())
    date      = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))


# ── Teacher Attendance Forms ────────────────────────────────────
class TeacherAttendanceForm(BootstrapMixin, forms.ModelForm):
    class Meta:
        model  = TeacherAttendance
        fields = ['teacher', 'date', 'status', 'note']
        widgets = {'date': forms.DateInput(attrs={'type': 'date'})}


class BulkTeacherAttendanceForm(BootstrapMixin, forms.Form):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))


# ── Score / Exam Forms ──────────────────────────────────────────
class ScoreForm(BootstrapMixin, forms.ModelForm):
    class Meta:
        model  = Score
        fields = ['student', 'subject', 'exam_type', 'exam', 'academic_year', 'score', 'max_score', 'remarks']


class ExamForm(BootstrapMixin, forms.ModelForm):
    class Meta:
        model  = Exam
        fields = ['name', 'exam_type', 'subject', 'classroom', 'academic_year', 'date', 'max_score', 'description']
        widgets = {
            'date':        forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 2}),
        }


class ExamTypeForm(BootstrapMixin, forms.ModelForm):
    class Meta:
        model  = ExamType
        fields = ['name']


# ── Subject Form ────────────────────────────────────────────────
class SubjectForm(BootstrapMixin, forms.ModelForm):
    class Meta:
        model  = Subject
        fields = ['subject_id', 'name', 'code', 'teacher', 'grade', 'credit', 'description']
        widgets = {'description': forms.Textarea(attrs={'rows': 2})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make subject_id read-only — auto-generated, never edited by user
        self.fields['subject_id'].required = False
        self.fields['subject_id'].label = 'Subject ID'
        self.fields['subject_id'].widget.attrs.update({
            'readonly':    True,
            'placeholder': 'Auto-generated',
            'class':       'form-control',
            'style':       'background:#f3f4f6;color:#6b7280;cursor:not-allowed;',
        })

    def clean_subject_id(self):
        # Ignore user input — preserve existing value or leave blank for new records
        return self.instance.subject_id if self.instance.pk else None


# ── Grade / Academic Year ────────────────────────────────────────
class GradeForm(BootstrapMixin, forms.ModelForm):
    class Meta:
        model  = Grade
        fields = ['name', 'section']


class AcademicYearForm(BootstrapMixin, forms.ModelForm):
    class Meta:
        model  = AcademicYear
        fields = ['year', 'is_active']


# ── Timetable Forms ─────────────────────────────────────────────
class TimeSlotForm(BootstrapMixin, forms.ModelForm):
    class Meta:
        model  = TimeSlot
        fields = ['day', 'period', 'start_time', 'end_time']
        widgets = {
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time':   forms.TimeInput(attrs={'type': 'time'}),
        }


class TimetableForm(BootstrapMixin, forms.ModelForm):
    class Meta:
        model  = Timetable
        fields = ['classroom', 'subject', 'teacher', 'time_slot', 'academic_year', 'room']


# ── Notification Form ────────────────────────────────────────────
class NotificationForm(BootstrapMixin, forms.ModelForm):
    class Meta:
        model  = Notification
        fields = ['title', 'message', 'notification_type', 'audience', 'classroom', 'student', 'scheduled_at', 'is_active']
        widgets = {
            'message':      forms.Textarea(attrs={'rows': 4}),
            'scheduled_at': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }


# ── Report Card Form ─────────────────────────────────────────────
class ReportCardForm(BootstrapMixin, forms.ModelForm):
    class Meta:
        model  = ReportCard
        fields = [
            'student', 'academic_year', 'term', 'status',
            'teacher_remarks', 'principal_remarks', 'conduct',
            'attendance_days', 'absent_days'
        ]
        widgets = {
            'teacher_remarks':    forms.Textarea(attrs={'rows': 3}),
            'principal_remarks':  forms.Textarea(attrs={'rows': 3}),
        }


# ── School Event Form ────────────────────────────────────────────
class SchoolEventForm(BootstrapMixin, forms.ModelForm):
    class Meta:
        model  = SchoolEvent
        fields = ['title', 'event_type', 'start_date', 'end_date', 'description']
        widgets = {
            'start_date':  forms.DateInput(attrs={'type': 'date'}),
            'end_date':    forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }


# ── Student Self-Registration Form ──────────────────────────────
class StudentRegisterForm(BootstrapMixin, forms.Form):
    """Public form: a student creates their own login account."""
    username   = forms.CharField(max_length=150, label='ឈ្មោះអ្នកប្រើ')
    password1  = forms.CharField(label='ពាក្យសម្ងាត់', widget=forms.PasswordInput)
    password2  = forms.CharField(label='បញ្ជាក់ពាក្យសម្ងាត់', widget=forms.PasswordInput)
    student_id = forms.CharField(max_length=20, label='លេខសម្គាល់សិស្ស (ឧ. STU-0001)')

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('ឈ្មោះអ្នកប្រើនេះត្រូវបានប្រើរួចហើយ។')
        return username

    def clean_student_id(self):
        sid = self.cleaned_data['student_id'].strip().upper()
        from .models import Student
        try:
            student = Student.objects.get(student_id=sid)
        except Student.DoesNotExist:
            raise forms.ValidationError('រកមិនឃើញលេខសម្គាល់សិស្សនេះទេ។')
        # Prevent duplicate accounts
        from .models import UserProfile
        if UserProfile.objects.filter(student=student).exists():
            raise forms.ValidationError('គណនីសម្រាប់សិស្សនេះត្រូវបានបង្កើតរួចហើយ។')
        return sid

    def clean(self):
        cleaned = super().clean()
        p1 = cleaned.get('password1')
        p2 = cleaned.get('password2')
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError('ពាក្យសម្ងាត់មិនត្រូវគ្នា។')
        return cleaned

    def save(self):
        from .models import Student, UserProfile
        data    = self.cleaned_data
        student = Student.objects.get(student_id=data['student_id'].upper())
        user    = User.objects.create_user(
            username   = data['username'],
            password   = data['password1'],
            first_name = student.first_name,
            last_name  = student.last_name,
            email      = student.parent_email,
        )
        UserProfile.objects.update_or_create(
            user=user,
            defaults={'role': 'student', 'student': student}
        )
        return user


# ── Parent Self-Registration Form ────────────────────────────────
class ParentRegisterForm(BootstrapMixin, forms.Form):
    """Public form: a mom or dad creates their own login account."""
    RELATIONSHIP_CHOICES = [
        ('mom', 'ម្ដាយ (Mom)'),
        ('dad', 'ឪពុក (Dad)'),
    ]
    username      = forms.CharField(max_length=150, label='ឈ្មោះអ្នកប្រើ')
    first_name    = forms.CharField(max_length=150, label='ឈ្មោះ')
    last_name     = forms.CharField(max_length=150, label='នាមត្រកូល')
    email         = forms.EmailField(required=False, label='អ៊ីម៉ែល')
    phone         = forms.CharField(max_length=20, required=False, label='លេខទូរស័ព្ទ')
    relationship  = forms.ChoiceField(choices=RELATIONSHIP_CHOICES, label='ទំនាក់ទំនង')
    password1     = forms.CharField(label='ពាក្យសម្ងាត់', widget=forms.PasswordInput)
    password2     = forms.CharField(label='បញ្ជាក់ពាក្យសម្ងាត់', widget=forms.PasswordInput)
    student_id    = forms.CharField(max_length=20, label='លេខសម្គាល់កូន (ឧ. STU-0001)')

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('ឈ្មោះអ្នកប្រើនេះត្រូវបានប្រើរួចហើយ។')
        return username

    def clean_student_id(self):
        sid = self.cleaned_data['student_id'].strip().upper()
        from .models import Student
        if not Student.objects.filter(student_id=sid).exists():
            raise forms.ValidationError('រកមិនឃើញលេខសម្គាល់សិស្សនេះទេ។')
        return sid

    def clean(self):
        cleaned = super().clean()
        p1 = cleaned.get('password1')
        p2 = cleaned.get('password2')
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError('ពាក្យសម្ងាត់មិនត្រូវគ្នា។')
        return cleaned

    def save(self):
        from .models import Student, UserProfile
        data    = self.cleaned_data
        student = Student.objects.get(student_id=data['student_id'].upper())
        user    = User.objects.create_user(
            username   = data['username'],
            password   = data['password1'],
            first_name = data['first_name'],
            last_name  = data['last_name'],
            email      = data.get('email', ''),
        )
        UserProfile.objects.update_or_create(
            user=user,
            defaults={
                'role':    'parent',
                'phone':   data.get('phone', ''),
                'student': student,   # link to the child
            }
        )
        return user


# ── School Settings Form ─────────────────────────────────────────
from .models import SchoolSettings

class SchoolSettingsForm(BootstrapMixin, forms.ModelForm):
    class Meta:
        model  = SchoolSettings
        fields = ['school_name', 'school_name_en', 'school_slogan', 'logo', 'favicon',
                  'address', 'phone', 'email', 'website',
                  'primary_color', 'secondary_color', 'sidebar_bg']
        widgets = {
            'address':         forms.Textarea(attrs={'rows': 2}),
            'primary_color':   forms.TextInput(attrs={'type': 'color', 'class': 'form-control form-control-color'}),
            'secondary_color': forms.TextInput(attrs={'type': 'color', 'class': 'form-control form-control-color'}),
            'sidebar_bg':      forms.TextInput(attrs={'type': 'color', 'class': 'form-control form-control-color'}),
            'logo':            PhotoInput(),
            'favicon':         PhotoInput(),
        }
