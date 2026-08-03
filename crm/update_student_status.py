#!/usr/bin/env python
"""
Script to update existing students to ACTIVE status
Run this once after deploying the new status field
"""

import os
import sys
import django

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crm.settings')
django.setup()

from school.models import Student

def update_student_status():
    """Set all existing students to ACTIVE status"""
    
    # Get all students
    students = Student.objects.all()
    total = students.count()
    
    print(f"\n{'='*60}")
    print(f"  កំពុងធ្វើបច្ចុប្បន្នភាពស្ថានភាពសិស្ស")
    print(f"  Updating Student Status")
    print(f"{'='*60}\n")
    
    print(f"រកឃើញសិស្ស {total} នាក់")
    print(f"Found {total} students\n")
    
    # Update students without status or with null status
    updated = 0
    for student in students:
        if not student.status or student.status == '':
            student.status = 'ACTIVE'
            student.save(update_fields=['status'])
            updated += 1
            print(f"  ✓ {student.student_id} - {student.first_name} {student.last_name} → ACTIVE")
    
    print(f"\n{'='*60}")
    print(f"  ✅ បានធ្វើបច្ចុប្បន្នភាពសិស្ស {updated}/{total} នាក់")
    print(f"  ✅ Updated {updated}/{total} students")
    print(f"{'='*60}\n")
    
    # Show status summary
    print("\nស្ថិតិស្ថានភាព (Status Summary):")
    print("-" * 40)
    
    from django.db.models import Count
    status_summary = Student.objects.values('status').annotate(count=Count('id'))
    
    for item in status_summary:
        status = item['status'] or 'NULL'
        count = item['count']
        status_display = dict(Student.STATUS_CHOICES).get(status, status)
        print(f"  {status_display}: {count} នាក់")
    
    print()

if __name__ == '__main__':
    try:
        update_student_status()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
