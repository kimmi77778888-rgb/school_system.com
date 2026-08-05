"""
Quick Setup Script for New Exam System
ស្គ្រីបជួយបង្កើតប្រព័ន្ធប្រឡងថ្មីយ៉ាងលឿន

This script helps you quickly set up exams after resetting the system.
It will create exams for all subjects in selected classrooms.
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crm.settings')
django.setup()

from django.utils import timezone
from school.models import (
    Exam, ExamType, Subject, Classroom, AcademicYear, Student
)


def list_exam_types():
    """List available exam types"""
    exam_types = ExamType.objects.filter(is_active=True)
    print("\n📝 Available Exam Types:")
    for et in exam_types:
        print(f"   {et.id}. {et.name} ({et.code}) - Weight: {et.weight_percentage}%")
    return exam_types


def list_classrooms():
    """List available classrooms"""
    classrooms = Classroom.objects.all()
    print("\n🏫 Available Classrooms:")
    for c in classrooms:
        student_count = c.students.filter(is_active=True).count()
        print(f"   {c.id}. {c} - {student_count} students")
    return classrooms


def list_subjects():
    """List available subjects"""
    subjects = Subject.objects.all()
    print("\n📚 Available Subjects:")
    for s in subjects:
        print(f"   {s.id}. {s.name}")
    return subjects


def create_exams_for_classroom(classroom_id, exam_type_id, exam_date, max_score=100, passing_score=50):
    """
    Create exams for all subjects in a classroom
    
    Args:
        classroom_id: ID of the classroom
        exam_type_id: ID of the exam type (midterm, final, etc.)
        exam_date: Date of the exam (YYYY-MM-DD format or datetime object)
        max_score: Maximum score for the exam (default: 100)
        passing_score: Passing score for the exam (default: 50)
    """
    try:
        classroom = Classroom.objects.get(id=classroom_id)
        exam_type = ExamType.objects.get(id=exam_type_id)
        
        if not classroom.academic_year:
            print(f"❌ Classroom {classroom} has no academic year assigned!")
            return
        
        # Get all subjects
        subjects = Subject.objects.all()
        
        print(f"\n🔨 Creating exams for {classroom}...")
        print(f"   Exam Type: {exam_type.name}")
        print(f"   Date: {exam_date}")
        print(f"   Max Score: {max_score}")
        print(f"   Passing Score: {passing_score}")
        
        created_count = 0
        skipped_count = 0
        
        for subject in subjects:
            # Check if exam already exists
            existing = Exam.objects.filter(
                classroom=classroom,
                subject=subject,
                exam_type=exam_type,
                academic_year=classroom.academic_year
            ).exists()
            
            if existing:
                print(f"   ⚠️  Skipped {subject.name} (already exists)")
                skipped_count += 1
                continue
            
            # Create exam
            exam = Exam.objects.create(
                name=f"{exam_type.name} - {subject.name}",
                exam_type=exam_type,
                subject=subject,
                classroom=classroom,
                academic_year=classroom.academic_year,
                date=exam_date,
                max_score=max_score,
                passing_score=passing_score,
                status='scheduled',
                description=f"{exam_type.name} examination for {subject.name} in {classroom}"
            )
            print(f"   ✅ Created {exam.exam_id}: {subject.name}")
            created_count += 1
        
        print(f"\n✅ Summary:")
        print(f"   Created: {created_count} exams")
        print(f"   Skipped: {skipped_count} exams (already exist)")
        
    except Classroom.DoesNotExist:
        print(f"❌ Classroom with ID {classroom_id} not found!")
    except ExamType.DoesNotExist:
        print(f"❌ Exam Type with ID {exam_type_id} not found!")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()


def create_exams_for_multiple_classrooms(classroom_ids, exam_type_id, exam_date, max_score=100, passing_score=50):
    """Create exams for multiple classrooms at once"""
    print("=" * 80)
    print("🚀 BULK EXAM CREATION")
    print("=" * 80)
    
    for classroom_id in classroom_ids:
        create_exams_for_classroom(classroom_id, exam_type_id, exam_date, max_score, passing_score)
        print()


def interactive_setup():
    """Interactive setup wizard"""
    print("=" * 80)
    print("🧙 EXAM CREATION WIZARD")
    print("=" * 80)
    
    # List and select exam type
    exam_types = list_exam_types()
    if not exam_types:
        print("❌ No exam types found! Please create exam types first.")
        return
    
    exam_type_id = input("\n📝 Enter Exam Type ID: ")
    try:
        exam_type_id = int(exam_type_id)
        exam_type = ExamType.objects.get(id=exam_type_id)
    except (ValueError, ExamType.DoesNotExist):
        print("❌ Invalid Exam Type ID!")
        return
    
    # List and select classrooms
    classrooms = list_classrooms()
    if not classrooms:
        print("❌ No classrooms found!")
        return
    
    print("\n🏫 Select Classrooms:")
    print("   Enter classroom IDs separated by commas (e.g., 1,2,3)")
    print("   Or enter 'all' to create exams for all classrooms")
    
    classroom_input = input("\n🏫 Classroom IDs: ")
    
    if classroom_input.lower() == 'all':
        classroom_ids = [c.id for c in classrooms]
    else:
        try:
            classroom_ids = [int(x.strip()) for x in classroom_input.split(',')]
        except ValueError:
            print("❌ Invalid classroom IDs!")
            return
    
    # Get exam date
    exam_date_str = input("\n📅 Exam Date (YYYY-MM-DD, or press Enter for today): ")
    if not exam_date_str:
        exam_date = timezone.now().date()
    else:
        try:
            from datetime import datetime
            exam_date = datetime.strptime(exam_date_str, '%Y-%m-%d').date()
        except ValueError:
            print("❌ Invalid date format! Use YYYY-MM-DD")
            return
    
    # Get scores
    max_score_str = input("\n💯 Max Score (press Enter for 100): ")
    max_score = float(max_score_str) if max_score_str else 100
    
    passing_score_str = input("✅ Passing Score (press Enter for 50): ")
    passing_score = float(passing_score_str) if passing_score_str else 50
    
    # Confirm
    print("\n" + "=" * 80)
    print("📋 SUMMARY")
    print("=" * 80)
    print(f"   Exam Type: {exam_type.name}")
    print(f"   Classrooms: {len(classroom_ids)} selected")
    print(f"   Date: {exam_date}")
    print(f"   Max Score: {max_score}")
    print(f"   Passing Score: {passing_score}")
    print(f"   Subjects: All subjects will be included")
    
    confirm = input("\n✅ Proceed? (yes/no): ")
    if confirm.lower() not in ['yes', 'y']:
        print("❌ Cancelled!")
        return
    
    # Create exams
    create_exams_for_multiple_classrooms(
        classroom_ids,
        exam_type_id,
        exam_date,
        max_score,
        passing_score
    )


def quick_create_example():
    """Quick example for common scenarios"""
    print("=" * 80)
    print("⚡ QUICK EXAMPLES")
    print("=" * 80)
    
    print("\n1. Create Midterm Exams for Grade 7A")
    print("   create_exams_for_classroom(1, 1, '2026-08-15', 100, 50)")
    
    print("\n2. Create Final Exams for Multiple Classrooms")
    print("   create_exams_for_multiple_classrooms([1, 2, 3], 2, '2026-12-15', 100, 50)")
    
    print("\n3. Use Interactive Wizard")
    print("   interactive_setup()")


if __name__ == '__main__':
    print("\n" + "=" * 80)
    print("🚀 QUICK EXAM SETUP TOOL")
    print("=" * 80)
    
    print("\nOPTIONS:")
    print("1. Interactive Setup Wizard (Recommended)")
    print("2. Create exams for single classroom")
    print("3. Create exams for multiple classrooms")
    print("4. View examples")
    print("5. Exit")
    
    choice = input("\nEnter your choice (1-5): ")
    
    if choice == '1':
        interactive_setup()
    
    elif choice == '2':
        list_exam_types()
        list_classrooms()
        
        try:
            classroom_id = int(input("\n🏫 Classroom ID: "))
            exam_type_id = int(input("📝 Exam Type ID: "))
            exam_date = input("📅 Exam Date (YYYY-MM-DD): ")
            max_score = float(input("💯 Max Score (default 100): ") or 100)
            passing_score = float(input("✅ Passing Score (default 50): ") or 50)
            
            create_exams_for_classroom(classroom_id, exam_type_id, exam_date, max_score, passing_score)
        except (ValueError, KeyboardInterrupt):
            print("\n❌ Invalid input!")
    
    elif choice == '3':
        list_exam_types()
        list_classrooms()
        
        try:
            classroom_ids = [int(x.strip()) for x in input("\n🏫 Classroom IDs (comma-separated): ").split(',')]
            exam_type_id = int(input("📝 Exam Type ID: "))
            exam_date = input("📅 Exam Date (YYYY-MM-DD): ")
            max_score = float(input("💯 Max Score (default 100): ") or 100)
            passing_score = float(input("✅ Passing Score (default 50): ") or 50)
            
            create_exams_for_multiple_classrooms(classroom_ids, exam_type_id, exam_date, max_score, passing_score)
        except (ValueError, KeyboardInterrupt):
            print("\n❌ Invalid input!")
    
    elif choice == '4':
        quick_create_example()
    
    else:
        print("👋 Goodbye!")
