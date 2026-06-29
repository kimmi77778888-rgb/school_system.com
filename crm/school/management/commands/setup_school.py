"""
Management command: python manage.py setup_school
Seeds essential initial data:
  - TimeSlots (6 periods × 6 days)
  - AcademicYear (current year)
  - Grades (ទី១–ទី៦)
  - ExamTypes (តេស្ត, ប្រឡងពាក់កណ្ដាលឆ្នាំ, ប្រឡងចុងឆ្នាំ)
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import time


class Command(BaseCommand):
    help = 'Seed essential school data (time slots, grades, academic year, exam types)'

    def handle(self, *args, **options):
        from school.models import TimeSlot, AcademicYear, Grade, ExamType

        self.stdout.write('\n📚  Setting up school data...\n')

        # ── 1. Academic Year ──────────────────────────────
        year_str = str(timezone.now().year)
        ay, created = AcademicYear.objects.get_or_create(
            year=year_str,
            defaults={'is_active': True}
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'  ✓  ឆ្នាំសិក្សា {year_str} បានបង្កើត'))
        else:
            ay.is_active = True; ay.save()
            self.stdout.write(f'  –  ឆ្នាំសិក្សា {year_str} មានស្រាប់')

        # ── 2. Grades ─────────────────────────────────────
        grade_names = ['ទី១', 'ទី២', 'ទី៣', 'ទី៤', 'ទី៥', 'ទី៦']
        for name in grade_names:
            g, created = Grade.objects.get_or_create(name=name)
            status = '✓' if created else '–'
            self.stdout.write(f'  {status}  ថ្នាក់ {name}')

        # ── 3. TimeSlots ──────────────────────────────────
        # Monday=1 … Saturday=6, 6 periods per day
        schedule = [
            (1, '07:00', '07:45'),
            (2, '07:45', '08:30'),
            (3, '08:30', '09:15'),
            (4, '09:30', '10:15'),
            (5, '10:15', '11:00'),
            (6, '11:00', '11:45'),
        ]
        days = [1, 2, 3, 4, 5, 6]  # Mon–Sat
        day_names = {1:'ចន្ទ',2:'អង្គារ',3:'ពុធ',4:'ព្រហស្បតិ៍',5:'សុក្រ',6:'សៅរ៍'}
        created_count = 0
        for day in days:
            for period, start_str, end_str in schedule:
                h_s, m_s = map(int, start_str.split(':'))
                h_e, m_e = map(int, end_str.split(':'))
                ts, created = TimeSlot.objects.get_or_create(
                    day=day, period=period,
                    defaults={'start_time': time(h_s, m_s), 'end_time': time(h_e, m_e)}
                )
                if created: created_count += 1
        total = len(days) * len(schedule)
        self.stdout.write(self.style.SUCCESS(
            f'  ✓  TimeSlot: {created_count} បង្កើតថ្មី / {total} សរុប'
        ))

        # ── 4. Exam Types ─────────────────────────────────
        exam_types = ['តេស្ត', 'ប្រឡងពាក់កណ្ដាលឆ្នាំ', 'ប្រឡងចុងឆ្នាំ', 'លំហាត់']
        for name in exam_types:
            et, created = ExamType.objects.get_or_create(name=name)
            status = '✓' if created else '–'
            self.stdout.write(f'  {status}  ប្រភេទប្រឡង: {name}')

        self.stdout.write('\n' + self.style.SUCCESS('✅  រួចរាល់! ទិន្នន័យដំបូងបានដំឡើងរួច។\n'))
        self.stdout.write('  ▶  ចូលទៅ /school/ ហើយចាប់ផ្ដើមប្រើប្រាស់\n')
