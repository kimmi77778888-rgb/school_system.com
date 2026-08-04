#!/usr/bin/env python
import os
import sys
import django

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crm.settings')
django.setup()

from school.models import Classroom

# Simulate what happens when you select Grade 2 | 2026
current_classroom = Classroom.objects.get(grade__grade_number=2, academic_year__year='2026')

print("\n" + "="*70)
print("DEBUGGING PROMOTION ISSUE")
print("="*70)
print(f"\nCurrent classroom selected: {current_classroom}")
print(f"  ID: {current_classroom.id}")
print(f"  Grade number: {current_classroom.grade.grade_number}")
print(f"  Academic year: {current_classroom.academic_year.year}")

# Get all classrooms
all_classrooms = Classroom.objects.all().select_related('grade', 'academic_year')

print(f"\nLooking for next grade classrooms (Grade {current_classroom.grade.grade_number + 1})...")
print("-"*70)

next_classrooms = []
for classroom in all_classrooms:
    if classroom.grade and classroom.grade.grade_number:
        if classroom.grade.grade_number == current_classroom.grade.grade_number + 1:
            next_classrooms.append(classroom)
            print(f"✅ Found: {classroom} (ID: {classroom.id})")

print("-"*70)
print(f"\nTotal next classrooms found: {len(next_classrooms)}")

if len(next_classrooms) == 0:
    print("\n❌ NO CLASSROOMS FOUND! This is why the dropdown is empty.")
else:
    print(f"\n✅ Found {len(next_classrooms)} classroom(s). Dropdown should work!")
    print("\nClassrooms that should appear in dropdown:")
    for c in next_classrooms:
        print(f"  - {c}")
