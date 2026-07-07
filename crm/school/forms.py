from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from .models import (
    Student, Teacher, Classroom, Attendance, Score, Subject,
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
