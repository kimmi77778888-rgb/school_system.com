"""
Management command to setup grade numbers for existing grades
Run: python manage.py setup_grade_numbers
"""
from django.core.management.base import BaseCommand
from school.models import Grade
import re


class Command(BaseCommand):
    help = 'Setup grade numbers for existing grades'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('Setting up grade numbers...'))
        
        grades = Grade.objects.all()
        updated_count = 0
        
        # Mapping for Khmer numbers to grade numbers
        khmer_mapping = {
            'ទី១': (1, 'primary'),
            'ទី២': (2, 'primary'),
            'ទី៣': (3, 'primary'),
            'ទី៤': (4, 'primary'),
            'ទី៥': (5, 'primary'),
            'ទី៦': (6, 'primary'),
            'ទី៧': (7, 'lower_secondary'),
            'ទី៨': (8, 'lower_secondary'),
            'ទី៩': (9, 'lower_secondary'),
            'ទី១០': (10, 'upper_secondary'),
            'ទី១១': (11, 'upper_secondary'),
            'ទី១២': (12, 'upper_secondary'),
        }
        
        # English mapping
        english_mapping = {
            'Grade 1': (1, 'primary'),
            'Grade 2': (2, 'primary'),
            'Grade 3': (3, 'primary'),
            'Grade 4': (4, 'primary'),
            'Grade 5': (5, 'primary'),
            'Grade 6': (6, 'primary'),
            'Grade 7': (7, 'lower_secondary'),
            'Grade 8': (8, 'lower_secondary'),
            'Grade 9': (9, 'lower_secondary'),
            'Grade 10': (10, 'upper_secondary'),
            'Grade 11': (11, 'upper_secondary'),
            'Grade 12': (12, 'upper_secondary'),
        }
        
        for grade in grades:
            grade_name = grade.name.strip()
            
            # Check Khmer mapping
            if grade_name in khmer_mapping:
                grade_num, level = khmer_mapping[grade_name]
                grade.grade_number = grade_num
                grade.level = level
                grade.save()
                updated_count += 1
                self.stdout.write(self.style.SUCCESS(f'  ✓ {grade_name} → Grade {grade_num} ({level})'))
            
            # Check English mapping
            elif grade_name in english_mapping:
                grade_num, level = english_mapping[grade_name]
                grade.grade_number = grade_num
                grade.level = level
                grade.save()
                updated_count += 1
                self.stdout.write(self.style.SUCCESS(f'  ✓ {grade_name} → Grade {grade_num} ({level})'))
            
            # Try to extract number from name
            else:
                # Try to find digit
                match = re.search(r'\d+', grade_name)
                if match:
                    grade_num = int(match.group())
                    if 1 <= grade_num <= 12:
                        # Determine level based on grade number
                        if grade_num <= 6:
                            level = 'primary'
                        elif grade_num <= 9:
                            level = 'lower_secondary'
                        else:
                            level = 'upper_secondary'
                        
                        grade.grade_number = grade_num
                        grade.level = level
                        grade.save()
                        updated_count += 1
                        self.stdout.write(self.style.SUCCESS(f'  ✓ {grade_name} → Grade {grade_num} ({level})'))
                    else:
                        self.stdout.write(self.style.WARNING(f'  ⚠ {grade_name} - invalid grade number: {grade_num}'))
                else:
                    self.stdout.write(self.style.WARNING(f'  ⚠ {grade_name} - could not determine grade number'))
        
        self.stdout.write(self.style.SUCCESS(''))
        self.stdout.write(self.style.SUCCESS(f'✓ Updated {updated_count} grades'))
        self.stdout.write(self.style.SUCCESS(''))
        self.stdout.write(self.style.SUCCESS('Grade Structure:'))
        self.stdout.write(self.style.SUCCESS('━━━━━━━━━━━━━━━━━━━━━━━━━━━━'))
        
        # Show summary
        primary = Grade.objects.filter(level='primary').order_by('grade_number')
        if primary.exists():
            self.stdout.write(self.style.SUCCESS('📚 បឋមសិក្សា (Primary):'))
            for g in primary:
                self.stdout.write(self.style.SUCCESS(f'   {g.name} - Grade {g.grade_number}'))
        
        lower = Grade.objects.filter(level='lower_secondary').order_by('grade_number')
        if lower.exists():
            self.stdout.write(self.style.SUCCESS(''))
            self.stdout.write(self.style.SUCCESS('📖 បឋមភូមិ (Lower Secondary):'))
            for g in lower:
                self.stdout.write(self.style.SUCCESS(f'   {g.name} - Grade {g.grade_number}'))
        
        upper = Grade.objects.filter(level='upper_secondary').order_by('grade_number')
        if upper.exists():
            self.stdout.write(self.style.SUCCESS(''))
            self.stdout.write(self.style.SUCCESS('🎓 មធ្យមភូមិ (Upper Secondary):'))
            for g in upper:
                self.stdout.write(self.style.SUCCESS(f'   {g.name} - Grade {g.grade_number}'))
        
        self.stdout.write(self.style.SUCCESS('━━━━━━━━━━━━━━━━━━━━━━━━━━━━'))
        self.stdout.write(self.style.SUCCESS(''))
        self.stdout.write(self.style.SUCCESS('✓ Setup complete! You can now promote students.'))
