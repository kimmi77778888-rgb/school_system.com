#!/usr/bin/env python
"""Check promotion paths for 2026-2027"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crm.settings')
django.setup()

from school.models import Classroom, Grade, AcademicYear

print('=== ពិនិត្យផ្លូវឡើងថ្នាក់ 2026-2027 ===\n')

year = AcademicYear.objects.get(year='2026-2027')
print(f'Academic Year: {year.year} (ID: {year.id})\n')

for grade_num in range(1, 7):
    grade = Grade.objects.get(grade_number=grade_num)
    classroom = Classroom.objects.filter(grade=grade, academic_year=year).first()
    
    if classroom:
        print(f'✅ ថ្នាក់ទី{grade_num}: {classroom} (ID: {classroom.id})')
    else:
        print(f'❌ ថ្នាក់ទី{grade_num}: មិនមាន')

print('\n=== ផ្លូវឡើងថ្នាក់ ===\n')

for grade_num in range(1, 6):
    current_grade = Grade.objects.get(grade_number=grade_num)
    next_grade = Grade.objects.get(grade_number=grade_num + 1)
    
    current_cls = Classroom.objects.filter(grade=current_grade, academic_year=year).first()
    next_cls = Classroom.objects.filter(grade=next_grade, academic_year=year).first()
    
    if current_cls and next_cls:
        print(f'✅ {current_cls} → {next_cls}')
        print(f'   Current ID: {current_cls.id}, Next ID: {next_cls.id}')
    else:
        print(f'❌ ថ្នាក់ទី{grade_num} → ថ្នាក់ទី{grade_num+1}: មិនមានថ្នាក់')

print('\n=== រួចរាល់ ===')
