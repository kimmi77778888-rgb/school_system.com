#!/usr/bin/env python
"""Test script to diagnose classroom form issue"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crm.settings')
django.setup()

from school.forms import ClassroomForm
from school.models import Grade, AcademicYear

print("=" * 60)
print("TESTING CLASSROOM FORM")
print("=" * 60)

# Check database data
print("\n1. Database Data:")
print(f"   Grades: {Grade.objects.count()}")
for g in Grade.objects.all():
    print(f"      - {g.id}: {g.name}")

print(f"\n   Academic Years: {AcademicYear.objects.count()}")
for ay in AcademicYear.objects.all():
    print(f"      - {ay.id}: {ay.year}")

# Test form instantiation
print("\n2. Form Instantiation Test:")
form = ClassroomForm()

print("\n3. Form Fields:")
for field_name, field in form.fields.items():
    print(f"   {field_name}:")
    print(f"      Type: {field.__class__.__name__}")
    print(f"      Required: {field.required}")
    
    if hasattr(field, 'queryset'):
        qs = field.queryset
        print(f"      Queryset: {qs.model.__name__}")
        print(f"      Count: {qs.count()}")
        if qs.count() > 0:
            print(f"      Sample: {list(qs.values_list('id', flat=True))[:5]}")
        else:
            print(f"      ⚠️  EMPTY QUERYSET!")

print("\n4. Rendered HTML (Grade field):")
print(form['grade'])

print("\n" + "=" * 60)
print("TEST COMPLETE")
print("=" * 60)
