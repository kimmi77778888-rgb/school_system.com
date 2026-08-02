"""
Management command to clean Khmer text in database
Removes invisible characters and normalizes Unicode
"""

from django.core.management.base import BaseCommand
from school.models import Student, Teacher
from school.utils_khmer import clean_khmer_text, detect_invisible_chars


class Command(BaseCommand):
    help = 'Clean Khmer text in database by removing invisible characters'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be changed without actually changing it',
        )
        parser.add_argument(
            '--verbose',
            action='store_true',
            help='Show detailed information about changes',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        verbose = options['verbose']
        
        self.stdout.write(self.style.SUCCESS('=' * 70))
        self.stdout.write(self.style.SUCCESS('🧹 CLEANING KHMER TEXT IN DATABASE'))
        self.stdout.write(self.style.SUCCESS('=' * 70))
        
        if dry_run:
            self.stdout.write(self.style.WARNING('⚠️  DRY RUN MODE - No changes will be saved'))
        
        # Clean Students
        self.stdout.write('\n📚 Cleaning Student records...')
        student_count = 0
        
        for student in Student.objects.all():
            changed = False
            changes = []
            
            # Check and clean first_name
            if student.first_name:
                cleaned = clean_khmer_text(student.first_name)
                if cleaned != student.first_name:
                    if verbose:
                        invisible = detect_invisible_chars(student.first_name)
                        if invisible:
                            self.stdout.write(f'  Found invisible chars in {student.student_id} first_name: {invisible}')
                    changes.append(f'first_name: "{student.first_name}" → "{cleaned}"')
                    student.first_name = cleaned
                    changed = True
            
            # Check and clean last_name
            if student.last_name:
                cleaned = clean_khmer_text(student.last_name)
                if cleaned != student.last_name:
                    if verbose:
                        invisible = detect_invisible_chars(student.last_name)
                        if invisible:
                            self.stdout.write(f'  Found invisible chars in {student.student_id} last_name: {invisible}')
                    changes.append(f'last_name: "{student.last_name}" → "{cleaned}"')
                    student.last_name = cleaned
                    changed = True
            
            # Check and clean address
            if student.address:
                cleaned = clean_khmer_text(student.address)
                if cleaned != student.address:
                    changes.append('address (cleaned)')
                    student.address = cleaned
                    changed = True
            
            # Check and clean place_of_birth
            if student.place_of_birth:
                cleaned = clean_khmer_text(student.place_of_birth)
                if cleaned != student.place_of_birth:
                    changes.append('place_of_birth (cleaned)')
                    student.place_of_birth = cleaned
                    changed = True
            
            if changed:
                student_count += 1
                if verbose:
                    self.stdout.write(f'  ✓ {student.student_id}: {", ".join(changes)}')
                if not dry_run:
                    student.save()
        
        self.stdout.write(self.style.SUCCESS(f'✓ Cleaned {student_count} student records'))
        
        # Clean Teachers
        self.stdout.write('\n👨‍🏫 Cleaning Teacher records...')
        teacher_count = 0
        
        for teacher in Teacher.objects.all():
            changed = False
            changes = []
            
            # Check and clean first_name
            if teacher.first_name:
                cleaned = clean_khmer_text(teacher.first_name)
                if cleaned != teacher.first_name:
                    changes.append(f'first_name: "{teacher.first_name}" → "{cleaned}"')
                    teacher.first_name = cleaned
                    changed = True
            
            # Check and clean last_name
            if teacher.last_name:
                cleaned = clean_khmer_text(teacher.last_name)
                if cleaned != teacher.last_name:
                    changes.append(f'last_name: "{teacher.last_name}" → "{cleaned}"')
                    teacher.last_name = cleaned
                    changed = True
            
            # Check and clean address
            if teacher.address:
                cleaned = clean_khmer_text(teacher.address)
                if cleaned != teacher.address:
                    changes.append('address (cleaned)')
                    teacher.address = cleaned
                    changed = True
            
            if changed:
                teacher_count += 1
                if verbose:
                    self.stdout.write(f'  ✓ {teacher.teacher_id}: {", ".join(changes)}')
                if not dry_run:
                    teacher.save()
        
        self.stdout.write(self.style.SUCCESS(f'✓ Cleaned {teacher_count} teacher records'))
        
        # Summary
        self.stdout.write('\n' + '=' * 70)
        self.stdout.write(self.style.SUCCESS('📊 SUMMARY'))
        self.stdout.write('=' * 70)
        self.stdout.write(f'Students cleaned: {student_count}')
        self.stdout.write(f'Teachers cleaned: {teacher_count}')
        self.stdout.write(f'Total records cleaned: {student_count + teacher_count}')
        
        if dry_run:
            self.stdout.write(self.style.WARNING('\n⚠️  DRY RUN - No changes were saved'))
            self.stdout.write('Run without --dry-run to apply changes')
        else:
            self.stdout.write(self.style.SUCCESS('\n✅ All changes saved successfully!'))
