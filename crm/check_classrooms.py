#!/usr/bin/env python
import os
import sys
import django

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crm.settings')
django.setup()

from school.models import Classroom, Grade

classrooms = Classroom.objects.select_related('grade', 'academic_year').order_by('grade__grade_number')

print("\n" + "="*70)
print("ALL CLASSROOMS IN DATABASE")
print("="*70)
print(f"{'ID':<5} {'Grade #':<10} {'Classroom Name':<30} {'Year':<15}")
print("-"*70)

for c in classrooms:
    grade_num = c.grade.grade_number if c.grade else '?'
    year = c.academic_year.year if c.academic_year else 'N/A'
    print(f"{c.id:<5} Grade {grade_num:<3} {str(c)[:29]:<30} {year:<15}")

print("="*70)
print(f"Total classrooms: {classrooms.count()}")
print("="*70)

# Check for Grade 2 and Grade 3
grade_2 = classrooms.filter(grade__grade_number=2)
grade_3 = classrooms.filter(grade__grade_number=3)

print(f"\nGrade 2 classrooms: {grade_2.count()}")
for c in grade_2:
    print(f"  - {c}")

print(f"\nGrade 3 classrooms: {grade_3.count()}")
for c in grade_3:
    print(f"  - {c}")

if grade_2.exists() and not grade_3.exists():
    print("\n⚠️  PROBLEM: You have Grade 2 classrooms but NO Grade 3 classrooms!")
    print("   Students in Grade 2 cannot be promoted because there's nowhere to go.")
