#!/usr/bin/env python
"""
Interactive Student Promotion Tool
ឧបករណ៍ដាក់សិស្សឡើងថ្នាក់

Simple script to promote students between grades.
"""

import os
import sys
import django

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crm.settings')
django.setup()

from school.models import Student, Classroom, Grade
from process_promotion import PromotionProcessor


def list_classrooms():
    """Display all classrooms"""
    classrooms = Classroom.objects.select_related('grade', 'academic_year').order_by(
        'grade__grade_number', 'name'
    )
    
    print("\n" + "="*70)
    print("AVAILABLE CLASSROOMS")
    print("="*70)
    print(f"{'ID':<5} {'Grade':<10} {'Classroom Name':<30} {'Year':<15}")
    print("-"*70)
    
    for cls in classrooms:
        grade_num = cls.grade.grade_number if cls.grade else '?'
        year = cls.academic_year.year if cls.academic_year else 'N/A'
        print(f"{cls.pk:<5} Grade {grade_num:<3} {str(cls)[:29]:<30} {year:<15}")
    
    print("="*70 + "\n")


def preview_students(classroom_id, passing_score=50, min_attendance=80):
    """Preview students in a classroom"""
    try:
        classroom = Classroom.objects.get(pk=classroom_id)
        students = Student.objects.filter(classroom=classroom, is_active=True)
        
        print(f"\n{'='*70}")
        print(f"STUDENTS IN: {classroom}")
        print(f"{'='*70}")
        print(f"Total: {students.count()} students")
        
        processor = PromotionProcessor(passing_score, min_attendance)
        
        eligible = 0
        for student in students:
            is_eligible, _ = processor.check_eligibility(student, classroom.academic_year)
            if is_eligible:
                eligible += 1
        
        print(f"Eligible for promotion: {eligible} students")
        print(f"{'='*70}\n")
        
    except Classroom.DoesNotExist:
        print(f"❌ Classroom {classroom_id} not found\n")



def main():
    """Interactive main menu"""
    print("\n" + "="*70)
    print("STUDENT PROMOTION TOOL")
    print("ឧបករណ៍ដាក់សិស្សឡើងថ្នាក់")
    print("="*70)
    
    while True:
        print("\nOPTIONS:")
        print("1. List all classrooms")
        print("2. Preview students in a classroom")
        print("3. Promote students (DRY RUN)")
        print("4. Promote students (LIVE - makes changes)")
        print("5. Exit")
        
        choice = input("\nSelect option (1-5): ").strip()
        
        if choice == '1':
            list_classrooms()
        
        elif choice == '2':
            classroom_id = input("Enter classroom ID: ").strip()
            if classroom_id.isdigit():
                preview_students(int(classroom_id))
            else:
                print("❌ Invalid ID\n")
        
        elif choice in ['3', '4']:
            dry_run = (choice == '3')
            
            list_classrooms()
            
            from_id = input("Enter FROM classroom ID: ").strip()
            to_id = input("Enter TO classroom ID: ").strip()
            
            if not from_id.isdigit() or not to_id.isdigit():
                print("❌ Invalid IDs\n")
                continue
            
            from_id = int(from_id)
            to_id = int(to_id)
            
            # Get criteria
            passing = input("Passing score % (default 50): ").strip()
            passing = float(passing) if passing else 50.0
            
            attendance = input("Minimum attendance % (default 80): ").strip()
            attendance = float(attendance) if attendance else 80.0
            
            # Confirm
            if not dry_run:
                print("\n⚠️  WARNING: This will make permanent changes!")
                confirm = input("Type 'YES' to confirm: ").strip()
                if confirm != 'YES':
                    print("❌ Cancelled\n")
                    continue
            
            # Process
            processor = PromotionProcessor(passing, attendance)
            processor.process_classroom(from_id, to_id, dry_run)
            
            if not dry_run:
                print("\n✅ Promotion completed!")
        
        elif choice == '5':
            print("\nGoodbye! លាហើយ!\n")
            break
        
        else:
            print("❌ Invalid option\n")


if __name__ == '__main__':
    main()
