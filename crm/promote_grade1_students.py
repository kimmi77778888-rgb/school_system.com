"""
Promote Grade 1 Students to Grade 2
====================================
This script identifies Grade 1 students who passed and promotes them to Grade 2
for the next academic year.

Criteria for passing:
- Average score across all subjects >= 50%
"""

import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crm.settings')
django.setup()

from django.db.models import Avg, Count, Q
from school.models import (
    Student, Grade, Classroom, AcademicYear, Score, Subject
)
from datetime import date


def get_student_average_score(student, academic_year):
    """
    Calculate the average score percentage for a student in the given academic year.
    Returns None if no scores found.
    """
    scores = Score.objects.filter(
        student=student,
        academic_year=academic_year
    )
    
    if not scores.exists():
        return None
    
    # Calculate average percentage across all subjects
    total_percentage = 0
    count = 0
    
    for score in scores:
        if score.max_score > 0:
            percentage = (score.score / score.max_score) * 100
            total_percentage += percentage
            count += 1
    
    if count == 0:
        return None
    
    return total_percentage / count


def list_and_promote_grade1_students(passing_percentage=50, create_classrooms=True):
    """
    List Grade 1 students who passed and optionally promote them to Grade 2.
    
    Args:
        passing_percentage: Minimum average percentage to pass (default: 50%)
        create_classrooms: Whether to create Grade 2 classrooms and promote students
    
    Returns:
        Dictionary with lists of passing and failing students
    """
    
    # Get current academic year
    current_year = AcademicYear.objects.filter(is_active=True).first()
    if not current_year:
        print("❌ No active academic year found!")
        return None
    
    print(f"\n{'='*70}")
    print(f"📚 GRADE 1 STUDENT PROMOTION REPORT")
    print(f"{'='*70}")
    print(f"📅 Current Academic Year: {current_year.year}")
    print(f"✓ Passing Threshold: {passing_percentage}%")
    print(f"{'='*70}\n")
    
    # Get Grade 1
    try:
        grade1 = Grade.objects.get(name__iexact='Grade 1')
    except Grade.DoesNotExist:
        print("❌ Grade 1 not found in database!")
        return None
    
    # Get all Grade 1 classrooms in current year
    grade1_classrooms = Classroom.objects.filter(
        grade=grade1,
        academic_year=current_year
    )
    
    if not grade1_classrooms.exists():
        print(f"❌ No Grade 1 classrooms found for {current_year.year}")
        return None
    
    # Get all students in Grade 1 classrooms
    grade1_students = Student.objects.filter(
        classroom__in=grade1_classrooms,
        is_active=True
    ).order_by('last_name', 'first_name')
    
    if not grade1_students.exists():
        print("❌ No active students found in Grade 1")
        return None
    
    print(f"📊 Total Grade 1 Students: {grade1_students.count()}\n")
    
    # Categorize students
    passing_students = []
    failing_students = []
    no_scores_students = []
    
    print(f"{'Student ID':<15} {'Name':<30} {'Average':<10} {'Status':<10}")
    print(f"{'-'*70}")
    
    for student in grade1_students:
        avg_score = get_student_average_score(student, current_year)
        full_name = f"{student.first_name} {student.last_name}"
        
        if avg_score is None:
            no_scores_students.append(student)
            print(f"{student.student_id:<15} {full_name:<30} {'N/A':<10} {'⚠ No Scores':<10}")
        elif avg_score >= passing_percentage:
            passing_students.append({
                'student': student,
                'average': avg_score,
                'classroom': student.classroom
            })
            print(f"{student.student_id:<15} {full_name:<30} {avg_score:>6.2f}%   {'✓ PASS':<10}")
        else:
            failing_students.append({
                'student': student,
                'average': avg_score,
                'classroom': student.classroom
            })
            print(f"{student.student_id:<15} {full_name:<30} {avg_score:>6.2f}%   {'✗ FAIL':<10}")
    
    print(f"\n{'='*70}")
    print(f"📈 SUMMARY")
    print(f"{'='*70}")
    print(f"✓ Passing Students: {len(passing_students)}")
    print(f"✗ Failing Students: {len(failing_students)}")
    print(f"⚠ Students with No Scores: {len(no_scores_students)}")
    print(f"{'='*70}\n")
    
    # Promotion to Grade 2
    if create_classrooms and passing_students:
        print(f"\n{'='*70}")
        print(f"🎓 PROMOTION TO GRADE 2")
        print(f"{'='*70}\n")
        
        # Check if next academic year exists
        next_year_name = str(int(current_year.year.split('-')[0]) + 1) + '-' + str(int(current_year.year.split('-')[1]) + 1)
        next_year, created = AcademicYear.objects.get_or_create(
            year=next_year_name,
            defaults={'is_active': False}
        )
        
        if created:
            print(f"✓ Created new academic year: {next_year_name}")
        else:
            print(f"✓ Found existing academic year: {next_year_name}")
        
        # Get or create Grade 2
        grade2, created = Grade.objects.get_or_create(
            name='Grade 2',
            defaults={'section': ''}
        )
        if created:
            print(f"✓ Created Grade 2")
        
        # Create Grade 2 classrooms for next year
        # Group students by current classroom to maintain sections
        classroom_groups = {}
        for item in passing_students:
            classroom = item['classroom']
            if classroom not in classroom_groups:
                classroom_groups[classroom] = []
            classroom_groups[classroom].append(item['student'])
        
        print(f"\n📋 Creating Grade 2 Classrooms for {next_year.year}...\n")
        
        promoted_count = 0
        
        for old_classroom, students_list in classroom_groups.items():
            # Create corresponding Grade 2 classroom
            section = old_classroom.grade.section if old_classroom.grade.section else ''
            
            # Update Grade object to include section
            grade2_section, created = Grade.objects.get_or_create(
                name='Grade 2',
                section=section
            )
            
            new_classroom, created = Classroom.objects.get_or_create(
                grade=grade2_section,
                academic_year=next_year,
                defaults={
                    'homeroom_teacher': old_classroom.homeroom_teacher,
                    'room_number': old_classroom.room_number,
                    'capacity': old_classroom.capacity
                }
            )
            
            if created:
                print(f"✓ Created classroom: {new_classroom}")
            else:
                print(f"✓ Using existing classroom: {new_classroom}")
            
            # Promote students
            for student in students_list:
                student.classroom = new_classroom
                student.save()
                promoted_count += 1
                print(f"  → Promoted {student.student_id} - {student.first_name} {student.last_name}")
        
        print(f"\n{'='*70}")
        print(f"✅ PROMOTION COMPLETE")
        print(f"{'='*70}")
        print(f"🎓 Total students promoted to Grade 2: {promoted_count}")
        print(f"📅 Academic Year: {next_year.year}")
        print(f"{'='*70}\n")
    
    return {
        'passing': passing_students,
        'failing': failing_students,
        'no_scores': no_scores_students,
        'current_year': current_year,
        'next_year': next_year if create_classrooms else None
    }


if __name__ == '__main__':
    print("\n" + "="*70)
    print("🎓 GRADE 1 TO GRADE 2 PROMOTION SYSTEM")
    print("="*70)
    
    # Display menu
    print("\nOptions:")
    print("1. List passing students only (no promotion)")
    print("2. List and PROMOTE passing students to Grade 2")
    print()
    
    choice = input("Enter your choice (1 or 2): ").strip()
    
    if choice == '1':
        result = list_and_promote_grade1_students(
            passing_percentage=50,
            create_classrooms=False
        )
    elif choice == '2':
        confirm = input("\n⚠️  This will promote passing students to Grade 2. Continue? (yes/no): ").strip().lower()
        if confirm == 'yes':
            result = list_and_promote_grade1_students(
                passing_percentage=50,
                create_classrooms=True
            )
        else:
            print("\n❌ Promotion cancelled.")
            result = None
    else:
        print("\n❌ Invalid choice!")
        result = None
    
    if result:
        print("\n✅ Operation completed successfully!")
    
    print()
