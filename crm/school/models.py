from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone


# ══════════════════════════════════════════════════════
#  USER PROFILE & ROLES
# ══════════════════════════════════════════════════════
class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('admin',   'Admin'),
        ('teacher', 'Teacher'),
        ('parent',  'Parent'),
        ('student', 'Student'),
    ]
    user     = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role     = models.CharField(max_length=20, choices=ROLE_CHOICES, default='student')
    phone    = models.CharField(max_length=20, blank=True)
    photo    = models.ImageField(upload_to='images/Users/', null=True, blank=True)
    # links
    teacher  = models.OneToOneField('Teacher', on_delete=models.SET_NULL, null=True, blank=True, related_name='user_profile')
    student  = models.ForeignKey('Student', on_delete=models.SET_NULL, null=True, blank=True, related_name='parent_profiles')

    def __str__(self):
        return f"{self.user.username} ({self.role})"


# ══════════════════════════════════════════════════════
#  LOGIN HISTORY - Track user logins with device info
# ══════════════════════════════════════════════════════
class LoginHistory(models.Model):
    user            = models.ForeignKey(User, on_delete=models.CASCADE, related_name='login_history')
    login_time      = models.DateTimeField(auto_now_add=True)
    ip_address      = models.GenericIPAddressField(null=True, blank=True)
    device_type     = models.CharField(max_length=50, blank=True)  # Mobile, Desktop, Tablet
    browser         = models.CharField(max_length=100, blank=True)
    operating_system = models.CharField(max_length=100, blank=True)
    device_name     = models.CharField(max_length=200, blank=True)  # e.g., iPhone 15 Pro
    location        = models.CharField(max_length=200, blank=True)
    user_agent      = models.TextField(blank=True)
    is_suspicious   = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.user.username} - {self.login_time.strftime('%Y-%m-%d %H:%M:%S')}"
    
    def get_device_icon(self):
        """Return Bootstrap icon class based on device type"""
        if 'mobile' in self.device_type.lower():
            return 'bi-phone'
        elif 'tablet' in self.device_type.lower():
            return 'bi-tablet'
        else:
            return 'bi-laptop'
    
    class Meta:
        ordering = ['-login_time']
        verbose_name = 'Login History'
        verbose_name_plural = 'Login Histories'


# ══════════════════════════════════════════════════════
#  ACADEMIC YEAR
# ══════════════════════════════════════════════════════
class AcademicYear(models.Model):
    year      = models.CharField(max_length=20)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.year

    class Meta:
        ordering = ['-year']


# ══════════════════════════════════════════════════════
#  GRADE
# ══════════════════════════════════════════════════════
class Grade(models.Model):
    # Cambodia Education System Levels
    LEVEL_CHOICES = [
        ('primary', 'បឋមសិក្សា (Primary: Grade 1-6)'),
        ('lower_secondary', 'បឋមភូមិ (Lower Secondary: Grade 7-9)'),
        ('upper_secondary', 'មធ្យមភូមិ (Upper Secondary: Grade 10-12)'),
    ]
    
    name    = models.CharField(max_length=50)
    section = models.CharField(max_length=10, blank=True)
    level   = models.CharField(max_length=20, choices=LEVEL_CHOICES, default='primary', verbose_name='កម្រិតថ្នាក់')
    grade_number = models.IntegerField(null=True, blank=True, verbose_name='លេខថ្នាក់', help_text='1-12')

    def __str__(self):
        return f"{self.name} {self.section}".strip()
    
    def get_next_grade_level(self):
        """Return the next level after this grade (for promotion logic)"""
        if self.grade_number == 6:
            return 'lower_secondary'
        elif self.grade_number == 9:
            return 'upper_secondary'
        elif self.grade_number == 12:
            return 'graduated'
        return self.level

    class Meta:
        ordering = ['grade_number', 'section']


# ══════════════════════════════════════════════════════
#  TEACHER
# ══════════════════════════════════════════════════════
class Teacher(models.Model):
    GENDER_CHOICES = [('M', 'Male'), ('F', 'Female')]
    
    # Cambodia Teacher Rank/Level (ជួរ)
    RANK_CHOICES = [
        ('primary', 'គ្រូបឋមសិក្សា (Primary Teacher)'),
        ('secondary', 'គ្រូមធ្យមសិក្សា (Secondary Teacher)'),
        ('senior', 'គ្រូជាន់ខ្ពស់ (Senior Teacher)'),
        ('master', 'គ្រូបណ្ឌិត (Master Teacher)'),
    ]

    teacher_id        = models.CharField(max_length=20, unique=True, blank=True)
    first_name        = models.CharField(max_length=100, verbose_name='នាមខ្លួន (ខ្មែរ)')
    last_name         = models.CharField(max_length=100, verbose_name='នាមត្រកូល (ខ្មែរ)')
    first_name_en     = models.CharField(max_length=100, blank=True, verbose_name='First Name (English)')
    last_name_en      = models.CharField(max_length=100, blank=True, verbose_name='Last Name (English)')
    gender            = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True, blank=True)
    phone             = models.CharField(max_length=20, blank=True)
    email             = models.EmailField(blank=True)
    address           = models.TextField(blank=True)
    
    # Professional Information
    subject_specialty = models.CharField(max_length=100, blank=True, verbose_name='ជំនាញមុខវិជ្ជា')
    hire_date         = models.DateField(null=True, blank=True, verbose_name='ថ្ងៃចូលបម្រើការងារ')
    photo             = models.ImageField(upload_to='images/Teachers/', null=True, blank=True)
    qualification     = models.CharField(max_length=200, blank=True, verbose_name='កម្រិតវប្បធម៌')
    is_active         = models.BooleanField(default=True)
    
    # Cambodia Teacher Standards
    teacher_rank      = models.CharField(max_length=20, choices=RANK_CHOICES, blank=True, verbose_name='ជួរគ្រូ')
    teacher_license   = models.CharField(max_length=50, blank=True, verbose_name='លេខអាជ្ញាប័ណ្ណគ្រូ')
    ministry_id       = models.CharField(max_length=50, blank=True, verbose_name='លេខសម្គាល់ក្រសួង')
    date_of_birth     = models.DateField(null=True, blank=True, verbose_name='ថ្ងៃខែឆ្នាំកំណើត')
    place_of_birth    = models.CharField(max_length=200, blank=True, verbose_name='ទីកន្លែងកំណើត')
    national_id       = models.CharField(max_length=20, blank=True, verbose_name='អត្តសញ្ញាណប័ណ្ណ')
    
    # Training & Certification
    teacher_training  = models.TextField(blank=True, verbose_name='បណ្តុះបណ្តាល')
    certifications    = models.TextField(blank=True, verbose_name='វិញ្ញាបនប័ត្រ')
    university        = models.CharField(max_length=200, blank=True, verbose_name='សាកលវិទ្យាល័យ')
    degree            = models.CharField(max_length=100, blank=True, verbose_name='សញ្ញាប័ត្រ')
    graduation_year   = models.IntegerField(null=True, blank=True, verbose_name='ឆ្នាំបញ្ចប់ការសិក្សា')
    
    # Employment Details
    contract_type     = models.CharField(max_length=50, blank=True, verbose_name='ប្រភេទកិច្ចសន្យា', 
                                        help_text='អចិន្ត្រៃយ៍, កិច្ចសន្យា, ល្បែ')
    salary_scale      = models.CharField(max_length=50, blank=True, verbose_name='ជួរប្រាក់ខែ')
    years_experience  = models.IntegerField(default=0, verbose_name='ឆ្នាំបទពិសោធន៍')
    
    # Emergency Contact
    emergency_contact = models.CharField(max_length=100, blank=True, verbose_name='អ្នកទំនាក់ទំនងបន្ទាន់')
    emergency_phone   = models.CharField(max_length=20, blank=True, verbose_name='ទូរស័ព្ទបន្ទាន់')
    emergency_relation = models.CharField(max_length=50, blank=True, verbose_name='ទំនាក់ទំនង')
    
    # Legacy single file fields (kept for backward compatibility)
    id_card_file      = models.FileField(upload_to='documents/teachers/id_cards/', null=True, blank=True, verbose_name='ឯកសារអត្តសញ្ញាណប័ណ្ណ')
    certificate_file  = models.FileField(upload_to='documents/teachers/certificates/', null=True, blank=True, verbose_name='ឯកសារវិញ្ញាបនប័ត្រ')

    def save(self, *args, **kwargs):
        if not self.teacher_id:
            super().save(*args, **kwargs)
            self.teacher_id = f"TCH-{self.pk:04d}"
            Teacher.objects.filter(pk=self.pk).update(teacher_id=self.teacher_id)
        else:
            super().save(*args, **kwargs)
    
    def get_age(self):
        if self.date_of_birth:
            from datetime import date
            today = date.today()
            return today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
        return None

    def __str__(self):
        return f"{self.last_name} {self.first_name}"

    class Meta:
        ordering = ['last_name', 'first_name']


# ══════════════════════════════════════════════════════
#  TEACHER DOCUMENT - For multiple file uploads
# ══════════════════════════════════════════════════════
class TeacherDocument(models.Model):
    DOCUMENT_TYPES = [
        ('id_card', 'អត្តសញ្ញាណប័ណ្ណ (ID Card)'),
        ('certificate', 'វិញ្ញាបនប័ត្រ (Certificate)'),
        ('degree', 'សញ្ញាប័ត្រសិក្សា (Degree)'),
        ('license', 'អាជ្ញាប័ណ្ណគ្រូ (Teacher License)'),
        ('contract', 'កិច្ចសន្យា (Contract)'),
        ('training', 'វិញ្ញាបនប័ត្របណ្តុះបណ្តាល (Training Certificate)'),
        ('other', 'ផ្សេងៗ (Other)'),
    ]
    
    teacher       = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='documents')
    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPES, verbose_name='ប្រភេទឯកសារ')
    document_file = models.FileField(upload_to='documents/teachers/', verbose_name='ឯកសារ')
    title         = models.CharField(max_length=200, blank=True, verbose_name='ចំណងជើង')
    description   = models.TextField(blank=True, verbose_name='ការពិពណ៌នា')
    uploaded_at   = models.DateTimeField(auto_now_add=True, verbose_name='ថ្ងៃបញ្ចូល')
    uploaded_by   = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='បញ្ចូលដោយ')
    
    def __str__(self):
        return f"{self.teacher} - {self.get_document_type_display()} - {self.title or 'No Title'}"
    
    def get_file_extension(self):
        import os
        return os.path.splitext(self.document_file.name)[1].lower()
    
    def is_pdf(self):
        return self.get_file_extension() == '.pdf'
    
    def is_image(self):
        return self.get_file_extension() in ['.jpg', '.jpeg', '.png', '.gif']
    
    class Meta:
        ordering = ['-uploaded_at']
        verbose_name = 'ឯកសារគ្រូ'
        verbose_name_plural = 'ឯកសារគ្រូ'


# ══════════════════════════════════════════════════════
#  CLASSROOM
# ══════════════════════════════════════════════════════
class Classroom(models.Model):
    classroom_id     = models.CharField(max_length=20, unique=True, blank=True, null=True)
    grade            = models.ForeignKey(Grade, on_delete=models.CASCADE, related_name='classrooms')
    homeroom_teacher = models.ForeignKey(
        Teacher, on_delete=models.SET_NULL, null=True, blank=True, related_name='homeroom_classes'
    )
    academic_year    = models.ForeignKey(AcademicYear, on_delete=models.CASCADE, related_name='classrooms')
    room_number      = models.CharField(max_length=20, blank=True)
    capacity         = models.PositiveIntegerField(default=30)

    def save(self, *args, **kwargs):
        if not self.classroom_id:
            super().save(*args, **kwargs)
            self.classroom_id = f"CLS-{self.pk:04d}"
            Classroom.objects.filter(pk=self.pk).update(classroom_id=self.classroom_id)
        else:
            super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.grade} | {self.academic_year}"

    class Meta:
        ordering = ['grade__name']


# ══════════════════════════════════════════════════════
#  STUDENT
# ══════════════════════════════════════════════════════
class Student(models.Model):
    GENDER_CHOICES = [('M', 'Male'), ('F', 'Female')]
    
    STATUS_CHOICES = [
        ('ACTIVE', 'សកម្ម (Active)'),
        ('PROMOTED', 'ឡើងថ្នាក់ (Promoted)'),
        ('GRADUATED', 'បញ្ចប់ការសិក្សា (Graduated)'),
        ('TRANSFERRED', 'ផ្ទេរសាលា (Transferred)'),
        ('WITHDRAWN', 'ឈប់រៀន (Withdrawn)'),
        ('SUSPENDED', 'ផ្អាកការសិក្សា (Suspended)'),
    ]

    student_id    = models.CharField(max_length=20, unique=True, blank=True)
    first_name    = models.CharField(max_length=100, verbose_name='នាមខ្លួន (ខ្មែរ)')
    last_name     = models.CharField(max_length=100, verbose_name='នាមត្រកូល (ខ្មែរ)')
    first_name_en = models.CharField(max_length=100, blank=True, verbose_name='First Name (English)')
    last_name_en  = models.CharField(max_length=100, blank=True, verbose_name='Last Name (English)')
    gender        = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True, verbose_name='ថ្ងៃខែឆ្នាំកំណើត')
    place_of_birth = models.CharField(max_length=200, blank=True, verbose_name='ទីកន្លែងកំណើត')
    
    # Birth Certificate Information
    birth_certificate_number = models.CharField(max_length=50, blank=True, verbose_name='លេខសំបុត្រកំណើត')
    birth_certificate_file = models.FileField(upload_to='documents/students/birth_certificates/', null=True, blank=True, verbose_name='សំបុត្រកំណើត')
    
    # Personal Information
    nationality = models.CharField(max_length=50, blank=True, default='ខ្មែរ', verbose_name='សញ្ជាតិ')
    religion = models.CharField(max_length=50, blank=True, verbose_name='សាសនា')
    address       = models.TextField(blank=True, verbose_name='អាសយដ្ឋាន')
    phone         = models.CharField(max_length=20, blank=True, verbose_name='ទូរស័ព្ទ')
    
    # Parent/Guardian Information
    parent_name   = models.CharField(max_length=200, blank=True, verbose_name='ឈ្មោះឪពុកម្តាយ')
    parent_phone  = models.CharField(max_length=20, blank=True, verbose_name='ទូរស័ព្ទឪពុកម្តាយ')
    parent_email  = models.EmailField(blank=True, verbose_name='អ៊ីម៉ែលឪពុកម្តាយ')
    parent_occupation = models.CharField(max_length=100, blank=True, verbose_name='មុខរបរឪពុកម្តាយ')
    
    # Father Information
    father_name = models.CharField(max_length=200, blank=True, verbose_name='ឈ្មោះឪពុក')
    father_phone = models.CharField(max_length=20, blank=True, verbose_name='ទូរស័ព្ទឪពុក')
    father_occupation = models.CharField(max_length=100, blank=True, verbose_name='មុខរបរឪពុក')
    
    # Mother Information
    mother_name = models.CharField(max_length=200, blank=True, verbose_name='ឈ្មោះម្តាយ')
    mother_phone = models.CharField(max_length=20, blank=True, verbose_name='ទូរស័ព្ទម្តាយ')
    mother_occupation = models.CharField(max_length=100, blank=True, verbose_name='មុខរបរម្តាយ')
    
    # Emergency Contact
    emergency_contact_name = models.CharField(max_length=200, blank=True, verbose_name='ឈ្មោះអ្នកទំនាក់ទំនងបន្ទាន់')
    emergency_contact_phone = models.CharField(max_length=20, blank=True, verbose_name='ទូរស័ព្ទបន្ទាន់')
    emergency_contact_relation = models.CharField(max_length=50, blank=True, verbose_name='ទំនាក់ទំនង')
    
    # School Information
    classroom     = models.ForeignKey(Classroom, on_delete=models.SET_NULL, null=True, blank=True, related_name='students')
    enrolled_date = models.DateField(auto_now_add=True, verbose_name='ថ្ងៃចុះឈ្មោះ')
    previous_school = models.CharField(max_length=200, blank=True, verbose_name='សាលារៀនមុន')
    
    # Health Information
    photo         = models.ImageField(upload_to='images/Students/', null=True, blank=True, verbose_name='រូបថត')
    blood_group   = models.CharField(max_length=5, blank=True, verbose_name='ក្រុមឈាម')
    medical_notes = models.TextField(blank=True, verbose_name='កំណត់សម្គាល់សុខភាព')
    allergies = models.TextField(blank=True, verbose_name='ប្រតិកម្មحساសភាព')
    
    # Additional Documents
    id_card_file = models.FileField(upload_to='documents/students/id_cards/', null=True, blank=True, verbose_name='អត្តសញ្ញាណប័ណ្ណ/លិខិតឆ្លងដែន')
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ACTIVE', verbose_name='ស្ថានភាព')
    is_active     = models.BooleanField(default=True, verbose_name='សកម្ម')
    
    # History tracking
    previous_classroom = models.CharField(max_length=200, blank=True, verbose_name='ថ្នាក់មុន', help_text='ថ្នាក់រៀនមុននេះ')
    promotion_date = models.DateField(null=True, blank=True, verbose_name='ថ្ងៃឡើងថ្នាក់')
    graduation_date = models.DateField(null=True, blank=True, verbose_name='ថ្ងៃបញ្ចប់ការសិក្សា')
    notes = models.TextField(blank=True, verbose_name='កំណត់ចំណាំ', help_text='ព័ត៌មានបន្ថែមអំពីសិស្ស')

    def save(self, *args, **kwargs):
        # Clean Khmer text to remove invisible characters
        from .utils_khmer import clean_khmer_text
        
        if self.first_name:
            self.first_name = clean_khmer_text(self.first_name)
        if self.last_name:
            self.last_name = clean_khmer_text(self.last_name)
        if self.place_of_birth:
            self.place_of_birth = clean_khmer_text(self.place_of_birth)
        if self.address:
            self.address = clean_khmer_text(self.address)
        
        # Generate student_id if not exists
        if not self.student_id:
            super().save(*args, **kwargs)
            self.student_id = f"STU-{self.pk:04d}"
            Student.objects.filter(pk=self.pk).update(student_id=self.student_id)
        else:
            super().save(*args, **kwargs)
    
    def get_age(self):
        if self.date_of_birth:
            from datetime import date
            today = date.today()
            return today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
        return None

    def __str__(self):
        return f"{self.student_id} - {self.last_name} {self.first_name}"

    class Meta:
        ordering = ['last_name', 'first_name']


# ══════════════════════════════════════════════════════
#  SUBJECT
# ══════════════════════════════════════════════════════
class Subject(models.Model):
    subject_id  = models.CharField(max_length=20, unique=True, blank=True, null=True)
    name    = models.CharField(max_length=100)
    code    = models.CharField(max_length=20, blank=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True, related_name='subjects')
    grade   = models.ForeignKey(Grade, on_delete=models.CASCADE, related_name='subjects')
    credit  = models.PositiveSmallIntegerField(default=1)
    description = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        if not self.subject_id:
            super().save(*args, **kwargs)
            self.subject_id = f"SUB-{self.pk:04d}"
            Subject.objects.filter(pk=self.pk).update(subject_id=self.subject_id)
        else:
            super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.grade})"

    class Meta:
        ordering = ['name']


# ══════════════════════════════════════════════════════
#  TIMETABLE
# ══════════════════════════════════════════════════════
class TimeSlot(models.Model):
    DAY_CHOICES = [
        (1, 'Monday'), (2, 'Tuesday'), (3, 'Wednesday'),
        (4, 'Thursday'), (5, 'Friday'), (6, 'Saturday'),
    ]
    day        = models.PositiveSmallIntegerField(choices=DAY_CHOICES)
    start_time = models.TimeField()
    end_time   = models.TimeField()
    period     = models.PositiveSmallIntegerField(default=1, help_text="Period number")

    def __str__(self):
        return f"{self.get_day_display()} P{self.period} ({self.start_time:%H:%M}–{self.end_time:%H:%M})"

    class Meta:
        ordering = ['day', 'start_time']
        unique_together = ('day', 'period')


class Timetable(models.Model):
    classroom     = models.ForeignKey(Classroom, on_delete=models.CASCADE, related_name='timetables')
    subject       = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='timetables')
    teacher       = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True, related_name='timetables')
    time_slot     = models.ForeignKey(TimeSlot, on_delete=models.CASCADE, related_name='timetables')
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE, related_name='timetables')
    room          = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f"{self.classroom} | {self.subject} | {self.time_slot}"

    class Meta:
        unique_together = ('classroom', 'time_slot', 'academic_year')
        ordering = ['time_slot__day', 'time_slot__start_time']


# ══════════════════════════════════════════════════════
#  ATTENDANCE
# ══════════════════════════════════════════════════════
class Attendance(models.Model):
    STATUS_CHOICES = [
        ('P', 'Present'),
        ('A', 'Absent'),
        ('L', 'Late'),
        ('E', 'Excused'),
    ]
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendances')
    date    = models.DateField()
    status  = models.CharField(max_length=1, choices=STATUS_CHOICES, default='P')
    note    = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.student} | {self.date} | {self.get_status_display()}"

    class Meta:
        unique_together = ('student', 'date')
        ordering = ['-date']


# ══════════════════════════════════════════════════════
#  EXAM & SCORE
# ══════════════════════════════════════════════════════
class ExamType(models.Model):
    """
    Types of exams (ប្រភេទប្រឡង)
    Examples: Midterm (កណ្តាលឆមាស), Final (ចុងឆមាស), Quiz (តេស្តតូច)
    """
    name = models.CharField(max_length=100, verbose_name='ឈ្មោះប្រភេទប្រឡង')
    code = models.CharField(max_length=20, blank=True, verbose_name='លេខកូដ')
    description = models.TextField(blank=True, verbose_name='ការពិពណ៌នា')
    weight_percentage = models.DecimalField(
        max_digits=5, decimal_places=2, default=100, 
        verbose_name='ភាគរយទម្ងន់',
        help_text='Weight in final grade calculation (e.g., Midterm=30%, Final=70%)'
    )
    is_active = models.BooleanField(default=True, verbose_name='ដំណើរការ')
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'ប្រភេទប្រឡង'
        verbose_name_plural = 'ប្រភេទប្រឡង'
        ordering = ['name']


class Exam(models.Model):
    """
    Exam Schedule (កាលវិភាគប្រឡង)
    Represents a specific exam session for a subject and classroom
    """
    exam_id       = models.CharField(max_length=20, unique=True, blank=True, null=True)
    name          = models.CharField(max_length=200, verbose_name='ឈ្មោះប្រឡង')
    exam_type     = models.ForeignKey(ExamType, on_delete=models.CASCADE, related_name='exams', verbose_name='ប្រភេទប្រឡង')
    subject       = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='exams', verbose_name='មុខវិជ្ជា')
    classroom     = models.ForeignKey(Classroom, on_delete=models.CASCADE, related_name='exams', verbose_name='ថ្នាក់')
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE, related_name='exams', verbose_name='ឆ្នាំសិក្សា')
    date          = models.DateField(verbose_name='ថ្ងៃប្រឡង')
    exam_time     = models.TimeField(null=True, blank=True, verbose_name='ម៉ោងប្រឡង')
    duration_minutes = models.IntegerField(default=60, verbose_name='រយៈពេល (នាទី)')
    max_score     = models.DecimalField(max_digits=5, decimal_places=2, default=100, verbose_name='ពិន្ទុអតិបរមា')
    passing_score = models.DecimalField(max_digits=5, decimal_places=2, default=50, verbose_name='ពិន្ទុជាប់')
    description   = models.TextField(blank=True, verbose_name='ការពិពណ៌នា')
    instructions  = models.TextField(blank=True, verbose_name='សេចក្តីណែនាំ')
    
    # Exam status
    STATUS_CHOICES = [
        ('scheduled', 'កំណត់ពេល (Scheduled)'),
        ('ongoing', 'កំពុងប្រឡង (Ongoing)'),
        ('completed', 'បានបញ្ចប់ (Completed)'),
        ('cancelled', 'បោះបង់ (Cancelled)'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled', verbose_name='ស្ថានភាព')
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='exams_created', verbose_name='បង្កើតដោយ')

    def save(self, *args, **kwargs):
        if not self.exam_id:
            super().save(*args, **kwargs)
            self.exam_id = f"EXM-{self.pk:04d}"
            Exam.objects.filter(pk=self.pk).update(exam_id=self.exam_id)
        else:
            super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} – {self.subject} ({self.classroom})"
    
    def passing_percentage(self):
        """Calculate passing percentage"""
        if self.max_score > 0:
            return round((self.passing_score / self.max_score) * 100, 2)
        return 50
    
    def total_students(self):
        """Count total students in classroom"""
        return self.classroom.students.filter(is_active=True).count()
    
    def total_results_submitted(self):
        """Count how many results have been submitted"""
        return self.exam_results.count()
    
    def completion_percentage(self):
        """Calculate what percentage of students have results"""
        total = self.total_students()
        if total > 0:
            return round((self.total_results_submitted() / total) * 100, 1)
        return 0
    
    def average_score(self):
        """Calculate average score of all results"""
        from django.db.models import Avg
        avg = self.exam_results.aggregate(Avg('score'))['score__avg']
        return round(avg, 2) if avg else 0
    
    def pass_rate(self):
        """Calculate percentage of students who passed"""
        total = self.total_results_submitted()
        if total > 0:
            passed = self.exam_results.filter(score__gte=self.passing_score).count()
            return round((passed / total) * 100, 1)
        return 0

    class Meta:
        ordering = ['-date', 'exam_time']
        verbose_name = 'ប្រឡង'
        verbose_name_plural = 'ប្រឡង'


class ExamResult(models.Model):
    """
    Individual Exam Results (លទ្ធផលប្រឡង)
    Stores detailed exam results for each student
    """
    exam          = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='exam_results', verbose_name='ប្រឡង')
    student       = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='exam_results', verbose_name='សិស្ស')
    score         = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='ពិន្ទុ')
    
    # Additional grading info
    grade_letter  = models.CharField(max_length=2, blank=True, verbose_name='ពិន្ទុអក្សរ', help_text='A, B, C, D, F')
    is_passed     = models.BooleanField(default=False, verbose_name='ជាប់')
    rank_in_class = models.IntegerField(null=True, blank=True, verbose_name='ចំណាត់ថ្នាក់')
    
    # Attendance for this exam
    was_present   = models.BooleanField(default=True, verbose_name='មកប្រឡង')
    absent_reason = models.CharField(max_length=255, blank=True, verbose_name='មូលហេតុអវត្តមាន')
    
    # Teacher feedback
    remarks       = models.TextField(blank=True, verbose_name='មតិយោបល់')
    strengths     = models.TextField(blank=True, verbose_name='ចំណុចខ្លាំង')
    areas_to_improve = models.TextField(blank=True, verbose_name='ចំណុចត្រូវកែលម្អ')
    
    # Metadata
    recorded_at   = models.DateTimeField(auto_now_add=True, verbose_name='ថ្ងៃបញ្ចូលពិន្ទុ')
    updated_at    = models.DateTimeField(auto_now=True)
    recorded_by   = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='exam_results_recorded', verbose_name='បញ្ចូលដោយ')
    
    def save(self, *args, **kwargs):
        """Auto-calculate grade letter and pass/fail on save"""
        # Calculate percentage
        percentage = self.percentage()
        
        # Determine grade letter (A-F scale)
        if percentage >= 90:
            self.grade_letter = 'A'
        elif percentage >= 80:
            self.grade_letter = 'B'
        elif percentage >= 70:
            self.grade_letter = 'C'
        elif percentage >= 60:
            self.grade_letter = 'D'
        else:
            self.grade_letter = 'F'
        
        # Determine pass/fail
        self.is_passed = self.score >= self.exam.passing_score and self.was_present
        
        super().save(*args, **kwargs)
    
    def percentage(self):
        """Calculate percentage score"""
        if self.exam.max_score > 0:
            return round((self.score / self.exam.max_score) * 100, 2)
        return 0
    
    def grade_color(self):
        """Return Bootstrap color class for grade"""
        grade_colors = {
            'A': 'success',
            'B': 'info',
            'C': 'primary',
            'D': 'warning',
            'F': 'danger'
        }
        return grade_colors.get(self.grade_letter, 'secondary')
    
    def pass_fail_khmer(self):
        """Return 'ជាប់' or 'ធ្លាក់'"""
        return 'ជាប់' if self.is_passed else 'ធ្លាក់'
    
    def __str__(self):
        return f"{self.student} - {self.exam.name}: {self.score}/{self.exam.max_score}"
    
    class Meta:
        unique_together = ('exam', 'student')
        ordering = ['-score']
        verbose_name = 'លទ្ធផលប្រឡង'
        verbose_name_plural = 'លទ្ធផលប្រឡង'


class StudentHistory(models.Model):
    """
    Track student progression through grades - one record per academic year
    រក្សាទុកប្រវត្តិសិស្ស - កំណត់ត្រាមួយសម្រាប់មួយឆ្នាំសិក្សា
    
    Cambodia Education System:
    - Primary (បឋមសិក្សា): Grade 1-6
    - Lower Secondary (បឋមភូមិ): Grade 7-9  
    - Upper Secondary (មធ្យមភូមិ): Grade 10-12
    """
    student        = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='history_records')
    academic_year  = models.ForeignKey(AcademicYear, on_delete=models.CASCADE, related_name='student_histories')
    classroom      = models.ForeignKey(Classroom, on_delete=models.SET_NULL, null=True, related_name='student_histories')
    grade_name     = models.CharField(max_length=100, verbose_name='ឈ្មោះថ្នាក់', help_text='Stored for historical reference')
    grade_number   = models.IntegerField(null=True, blank=True, verbose_name='លេខថ្នាក់', help_text='1-12')
    grade_level    = models.CharField(max_length=20, blank=True, verbose_name='កម្រិតថ្នាក់', help_text='primary, lower_secondary, upper_secondary')
    status         = models.CharField(max_length=20, choices=Student.STATUS_CHOICES, default='ACTIVE', verbose_name='ស្ថានភាព')
    
    # Academic performance
    average_score  = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name='ពិន្ទុមធ្យម')
    total_subjects = models.IntegerField(default=0, verbose_name='ចំនួនមុខវិជ្ជា')
    passed_subjects = models.IntegerField(default=0, verbose_name='ជាប់មុខវិជ្ជា')
    failed_subjects = models.IntegerField(default=0, verbose_name='ធ្លាក់មុខវិជ្ជា')
    
    # Attendance tracking
    total_days     = models.IntegerField(default=0, verbose_name='ថ្ងៃសរុប')
    present_days   = models.IntegerField(default=0, verbose_name='ថ្ងៃមកវត្តមាន')
    absent_days    = models.IntegerField(default=0, verbose_name='ថ្ងៃអវត្តមាន')
    
    # Dates
    start_date     = models.DateField(null=True, blank=True, verbose_name='ថ្ងៃចាប់ផ្តើម')
    end_date       = models.DateField(null=True, blank=True, verbose_name='ថ្ងៃបញ្ចប់')
    
    # Promotion details
    promoted_to    = models.CharField(max_length=200, blank=True, verbose_name='ឡើងថ្នាក់ទៅ', help_text='Next grade/classroom after promotion')
    promotion_note = models.TextField(blank=True, verbose_name='កំណត់សំគាល់ការឡើងថ្នាក់')
    
    # Notes
    notes          = models.TextField(blank=True, verbose_name='កំណត់ចំណាំ')
    
    # Metadata
    created_at     = models.DateTimeField(auto_now_add=True)
    updated_at     = models.DateTimeField(auto_now=True)
    
    def attendance_percentage(self):
        if self.total_days > 0:
            return round((self.present_days / self.total_days) * 100, 1)
        return 0
    
    def pass_percentage(self):
        if self.total_subjects > 0:
            return round((self.passed_subjects / self.total_subjects) * 100, 1)
        return 0
    
    def __str__(self):
        return f"{self.student.student_id} - {self.grade_name} ({self.academic_year.year})"
    
    class Meta:
        ordering = ['-academic_year__year', 'student']
        unique_together = ('student', 'academic_year')
        verbose_name = 'ប្រវត្តិសិស្ស'
        verbose_name_plural = 'ប្រវត្តិសិស្ស'


class Score(models.Model):
    student       = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='scores')
    subject       = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='scores')
    exam_type     = models.ForeignKey(ExamType, on_delete=models.CASCADE, related_name='scores')
    exam          = models.ForeignKey(Exam, on_delete=models.SET_NULL, null=True, blank=True, related_name='scores')
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE, related_name='scores')
    score         = models.DecimalField(max_digits=5, decimal_places=2)
    max_score     = models.DecimalField(max_digits=5, decimal_places=2, default=100)
    date_recorded = models.DateField(auto_now_add=True)
    remarks       = models.CharField(max_length=255, blank=True)

    def percentage(self):
        if self.max_score > 0:
            return round((self.score / self.max_score) * 100, 2)
        return 0

    def grade_letter(self):
        p = self.percentage()
        if p >= 90: return 'A'
        elif p >= 80: return 'B'
        elif p >= 70: return 'C'
        elif p >= 60: return 'D'
        return 'F'

    def grade_color(self):
        p = self.percentage()
        if p >= 90: return 'success'
        elif p >= 80: return 'info'
        elif p >= 70: return 'primary'
        elif p >= 60: return 'warning'
        return 'danger'
    
    def is_passing(self, passing_percentage=50):
        """Check if student passed (default: 50% or above)"""
        return self.percentage() >= passing_percentage
    
    def pass_fail_status(self, passing_percentage=50):
        """Return 'Pass' or 'Fail' based on percentage"""
        return 'Pass' if self.is_passing(passing_percentage) else 'Fail'
    
    def pass_fail_khmer(self, passing_percentage=50):
        """Return 'ជាប់' or 'ធ្លាក់' based on percentage"""
        return 'ជាប់' if self.is_passing(passing_percentage) else 'ធ្លាក់'
    
    def pass_fail_color(self, passing_percentage=50):
        """Return Bootstrap color class for pass/fail"""
        return 'success' if self.is_passing(passing_percentage) else 'danger'

    def __str__(self):
        return f"{self.student} | {self.subject} | {self.exam_type} | {self.score}"

    class Meta:
        unique_together = ('student', 'subject', 'exam_type', 'academic_year')
        ordering = ['-date_recorded']


# ══════════════════════════════════════════════════════
#  TEACHER ATTENDANCE
# ══════════════════════════════════════════════════════
class TeacherAttendance(models.Model):
    STATUS_CHOICES = [
        ('P', 'Present'),
        ('A', 'Absent'),
        ('L', 'Late'),
        ('E', 'Excused'),
    ]
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='attendances')
    date    = models.DateField()
    status  = models.CharField(max_length=1, choices=STATUS_CHOICES, default='P')
    note    = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.teacher} | {self.date} | {self.get_status_display()}"

    class Meta:
        unique_together = ('teacher', 'date')
        ordering = ['-date']


# ══════════════════════════════════════════════════════
#  TEACHER EMPLOYMENT HISTORY (ប្រវត្តិការងារ)
# ══════════════════════════════════════════════════════
class TeacherEmploymentHistory(models.Model):
    teacher       = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='employment_history', verbose_name='គ្រូ')
    school_name   = models.CharField(max_length=200, verbose_name='ឈ្មោះសាលា')
    position      = models.CharField(max_length=100, verbose_name='តួនាទី')
    start_date    = models.DateField(verbose_name='ថ្ងៃចាប់ផ្តើម')
    end_date      = models.DateField(null=True, blank=True, verbose_name='ថ្ងៃបញ្ចប់')
    is_current    = models.BooleanField(default=False, verbose_name='បច្ចុប្បន្ន')
    location      = models.CharField(max_length=200, blank=True, verbose_name='ទីតាំង')
    responsibilities = models.TextField(blank=True, verbose_name='ភារកិច្ច')
    achievements  = models.TextField(blank=True, verbose_name='សមិទ្ធផល')
    reason_leaving = models.CharField(max_length=200, blank=True, verbose_name='មូលហេតុចាកចេញ')
    
    def duration_years(self):
        from datetime import date
        end = self.end_date if self.end_date else date.today()
        delta = end - self.start_date
        return round(delta.days / 365.25, 1)
    
    def __str__(self):
        return f"{self.teacher} - {self.school_name} ({self.start_date.year})"
    
    class Meta:
        ordering = ['-start_date']
        verbose_name = 'ប្រវត្តិការងារ'
        verbose_name_plural = 'ប្រវត្តិការងារ'


# ══════════════════════════════════════════════════════
#  NOTIFICATION
# ══════════════════════════════════════════════════════
class Notification(models.Model):
    TYPE_CHOICES = [
        ('announcement', 'Announcement'),
        ('reminder',     'Reminder'),
        ('alert',        'Alert'),
        ('message',      'Message'),
        ('event',        'Event'),
    ]
    AUDIENCE_CHOICES = [
        ('all',      'Everyone'),
        ('teachers', 'Teachers Only'),
        ('parents',  'Parents Only'),
        ('students', 'Students Only'),
        ('admin',    'Admin Only'),
    ]
    notification_id   = models.CharField(max_length=20, unique=True, blank=True, null=True)
    title         = models.CharField(max_length=255)
    message       = models.TextField()
    notification_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='announcement')
    audience      = models.CharField(max_length=20, choices=AUDIENCE_CHOICES, default='all')
    created_by    = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='notifications_sent')
    created_at    = models.DateTimeField(auto_now_add=True)
    is_active     = models.BooleanField(default=True)
    scheduled_at  = models.DateTimeField(null=True, blank=True)
    # optional targets
    classroom     = models.ForeignKey(Classroom, on_delete=models.SET_NULL, null=True, blank=True, related_name='notifications')
    student       = models.ForeignKey(Student, on_delete=models.SET_NULL, null=True, blank=True, related_name='notifications')

    def save(self, *args, **kwargs):
        if not self.notification_id:
            super().save(*args, **kwargs)
            self.notification_id = f"NOT-{self.pk:04d}"
            Notification.objects.filter(pk=self.pk).update(notification_id=self.notification_id)
        else:
            super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']


class NotificationRead(models.Model):
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE, related_name='reads')
    user         = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notification_reads')
    read_at      = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('notification', 'user')


# ══════════════════════════════════════════════════════
#  REPORT CARD
# ══════════════════════════════════════════════════════
class ReportCard(models.Model):
    STATUS_CHOICES = [
        ('draft',     'Draft'),
        ('published', 'Published'),
    ]
    report_id       = models.CharField(max_length=20, unique=True, blank=True, null=True)
    student         = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='report_cards')
    academic_year   = models.ForeignKey(AcademicYear, on_delete=models.CASCADE, related_name='report_cards')
    term            = models.CharField(max_length=50, default='Term 1')
    generated_at    = models.DateTimeField(auto_now_add=True)
    generated_by    = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    status          = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    teacher_remarks = models.TextField(blank=True)
    principal_remarks = models.TextField(blank=True)
    conduct         = models.CharField(max_length=50, blank=True, help_text="e.g. Excellent / Good / Fair")
    attendance_days = models.PositiveIntegerField(default=0)
    absent_days     = models.PositiveIntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.report_id:
            super().save(*args, **kwargs)
            self.report_id = f"RPT-{self.pk:04d}"
            ReportCard.objects.filter(pk=self.pk).update(report_id=self.report_id)
        else:
            super().save(*args, **kwargs)

    def __str__(self):
        return f"Report: {self.student} | {self.academic_year} | {self.term}"

    class Meta:
        unique_together = ('student', 'academic_year', 'term')
        ordering = ['-generated_at']


# ══════════════════════════════════════════════════════
#  SCHOOL EVENT / CALENDAR
# ══════════════════════════════════════════════════════
class SchoolEvent(models.Model):
    TYPE_CHOICES = [
        ('holiday',  'Holiday'),
        ('exam',     'Exam'),
        ('sport',    'Sport Day'),
        ('meeting',  'Meeting'),
        ('activity', 'Activity'),
        ('other',    'Other'),
    ]
    event_id    = models.CharField(max_length=20, unique=True, blank=True, null=True)
    title       = models.CharField(max_length=255)
    event_type  = models.CharField(max_length=20, choices=TYPE_CHOICES, default='activity')
    start_date  = models.DateField()
    end_date    = models.DateField(null=True, blank=True)
    description = models.TextField(blank=True)
    created_by  = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.event_id:
            super().save(*args, **kwargs)
            self.event_id = f"EVT-{self.pk:04d}"
            SchoolEvent.objects.filter(pk=self.pk).update(event_id=self.event_id)
        else:
            super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} ({self.start_date})"

    class Meta:
        ordering = ['start_date']


# ══════════════════════════════════════════════════════
#  SIGNAL — auto-create UserProfile when User is created
# ══════════════════════════════════════════════════════
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        role = 'admin' if instance.is_superuser else 'student'
        # Only create if it doesn't already exist
        UserProfile.objects.get_or_create(user=instance, defaults={'role': role})

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, created, **kwargs):
    # Only sync on updates (not creates — handled by create_user_profile above).
    # Use update() instead of save() to avoid triggering this signal again.
    if not created:
        try:
            profile = instance.profile
            # Sync only if the profile already exists — no save() call to avoid
            # re-triggering post_save and causing infinite recursion.
            UserProfile.objects.filter(pk=profile.pk).update()
        except UserProfile.DoesNotExist:
            role = 'admin' if instance.is_superuser else 'student'
            UserProfile.objects.create(user=instance, role=role)


# ══════════════════════════════════════════════════════
#  SCHOOL SETTINGS (dynamic branding)
# ══════════════════════════════════════════════════════
class SchoolSettings(models.Model):
    school_name     = models.CharField(max_length=200, default='សាលាបឋមសិក្សា')
    school_name_en  = models.CharField(max_length=200, default='Primary School', blank=True)
    school_slogan   = models.CharField(max_length=300, blank=True, default='Primary School MS')
    logo            = models.ImageField(upload_to='school/logo/', null=True, blank=True)
    favicon         = models.ImageField(upload_to='school/favicon/', null=True, blank=True)
    address         = models.TextField(blank=True)
    phone           = models.CharField(max_length=50, blank=True)
    email           = models.EmailField(blank=True)
    website         = models.URLField(blank=True)
    primary_color   = models.CharField(max_length=7, default='#2563eb', help_text='Hex color e.g. #2563eb')
    secondary_color = models.CharField(max_length=7, default='#4f46e5', help_text='Hex color e.g. #4f46e5')
    sidebar_bg      = models.CharField(max_length=7, default='#0b1120', help_text='Sidebar background color')
    updated_at      = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'School Settings'
        verbose_name_plural = 'School Settings'

    def __str__(self):
        return self.school_name

    @classmethod
    def get(cls):
        """Always return the single settings object, creating if needed."""
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj
