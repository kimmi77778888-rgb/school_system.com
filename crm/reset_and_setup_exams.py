"""
Reset and Setup Exam System - Clean Installation
This script will:
1. Remove old exam data
2. Create fresh exam types
3. Create sample exams with proper classroom setup
4. Create exam results for testing
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crm.settings')
django.setup()

from school.models import (
    Exam, ExamResult, ExamType, Student, Subject, 
    Classroom, AcademicYear, User, Grade
)
from decimal import Decimal
from datetime import date, time

def reset_and_setup():
    print("=" * 80)
    print("RESET AND SETUP EXAM SYSTEM")
    print("=" * 80)
    
    # Step 1: Clean up old data
    print("\n1. Cleaning up old exam data...")
    old_results = ExamResult.objects.all().count()
    old_exams = Exam.objects.all().count()
    old_types = ExamType.objects.all().count()
    
    ExamResult.objects.all().delete()
    Exam.objects.all().delete()
    ExamType.objects.all().delete()
    
    print(f"   ✓ Deleted {old_results} exam results")
    print(f"   ✓ Deleted {old_exams} exams")
    print(f"   ✓ Deleted {old_types} exam types")
    
    # Step 2: Create Exam Types
    print("\n2. Creating Exam Types...")
    midterm = ExamType.objects.create(
        name='ប្រឡងកណ្តាលឆមាស (Midterm)',
        code='MIDTERM',
        description='Mid-semester examination',
        weight_percentage=Decimal('30.00'),
        is_active=True
    )
    print(f"   ✓ Created: {midterm.name}")
    
    final = ExamType.objects.create(
        name='ប្រឡងចុងឆមាស (Final)',
        code='FINAL',
        description='End of semester examination',
        weight_percentage=Decimal('70.00'),
        is_active=True
    )
    print(f"   ✓ Created: {final.name}")
    
    quiz = ExamType.objects.create(
        name='តេស្ត (Quiz)',
        code='QUIZ',
        description='Weekly quiz',
        weight_percentage=Decimal('10.00'),
        is_active=True
    )
    print(f"   ✓ Created: {quiz.name}")
    
    # Step 3: Find active classrooms with students
    print("\n3. Finding active classrooms...")
    classrooms = Classroom.objects.filter(
        students__is_active=True
    ).distinct()
    
    if not classrooms.exists():
        print("   ❌ No classrooms with active students found!")
        print("\n   Creating a sample classroom...")
        
        # Get or create academic year
        academic_year, created = AcademicYear.objects.get_or_create(
            year='2026',
            defaults={'is_active': True}
        )
        
        # Get or create grade
        grade, created = Grade.objects.get_or_create(
            name='ទី១',
            defaults={'section': 'A', 'level': 'primary', 'grade_number': 1}
        )
        
        # Create classroom
        classroom = Classroom.objects.create(
            grade=grade,
            academic_year=academic_year,
            room_number='101',
            capacity=30
        )
        print(f"   ✓ Created classroom: {classroom}")
        classrooms = [classroom]
    else:
        print(f"   ✓ Found {classrooms.count()} classrooms with students")
    
    # Step 4: Get admin user
    print("\n4. Getting Admin User...")
    admin_user = User.objects.filter(is_superuser=True).first()
    if not admin_user:
        admin_user = User.objects.filter(is_staff=True).first()
    
    if admin_user:
        print(f"   ✓ Using: {admin_user.username}")
    else:
        print("   ⚠ No admin user found, created_by will be None")
    
    # Step 5: Create Exams for each classroom
    print("\n5. Creating Exams...")
    total_exams = 0
    total_results = 0
    
    for classroom in classrooms[:3]:  # Limit to first 3 classrooms
        print(f"\n   Processing: {classroom}")
        
        # Get subjects for this classroom's grade
        subjects = Subject.objects.filter(grade=classroom.grade)[:2]
        
        if not subjects.exists():
            print(f"   ⚠ No subjects found for grade {classroom.grade}")
            continue
        
        # Get active students in this classroom
        students = classroom.students.filter(is_active=True)[:5]  # Max 5 students per exam
        
        if not students.exists():
            print(f"   ⚠ No active students in classroom")
            continue
        
        print(f"   Found {subjects.count()} subjects and {students.count()} students")
        
        # Create one exam per subject
        for subject in subjects:
            # Create Midterm Exam
            exam = Exam.objects.create(
                name=f'{subject.name} - កណ្តាលឆមាស',
                subject=subject,
                classroom=classroom,
                academic_year=classroom.academic_year,
                exam_type=midterm,
                date=date(2026, 7, 15),
                exam_time=time(8, 0),
                duration_minutes=90,
                max_score=Decimal('100.00'),
                passing_score=Decimal('50.00'),
                status='completed',
                description=f'Midterm exam for {subject.name}',
                instructions='Answer all questions carefully.',
                created_by=admin_user
            )
            total_exams += 1
            print(f"   ✓ Created Exam: {exam.name} (ID: {exam.pk})")
            
            # Create exam results for students
            sample_scores = [95, 88, 92, 78, 85]  # Varied scores
            
            for idx, student in enumerate(students):
                score = Decimal(str(sample_scores[idx % len(sample_scores)]))
                
                result = ExamResult.objects.create(
                    exam=exam,
                    student=student,
                    score=score,
                    was_present=True,
                    remarks='Good performance' if score >= 80 else 'Keep practicing',
                    strengths='Shows understanding' if score >= 80 else 'Making progress',
                    areas_to_improve='Practice more problems' if score < 80 else 'Continue good work',
                    recorded_by=admin_user
                )
                total_results += 1
            
            print(f"      ✓ Created {students.count()} results")
    
    # Step 6: Summary
    print("\n" + "=" * 80)
    print("SETUP COMPLETE!")
    print("=" * 80)
    print(f"\n✓ Created {total_exams} exams")
    print(f"✓ Created {total_results} exam results")
    print(f"✓ Using {classrooms.count()} classrooms")
    
    # Step 7: Show exam URLs
    print("\n" + "=" * 80)
    print("EXAM URLs - Ready to Use")
    print("=" * 80)
    
    exams = Exam.objects.all()
    if exams.exists():
        print("\nYou can now visit these URLs:")
        print(f"\n📋 Exam List: http://localhost:8000/exams/\n")
        
        for exam in exams:
            results_count = exam.exam_results.count()
            students_count = exam.classroom.students.filter(is_active=True).count()
            
            print(f"📝 {exam.name}")
            print(f"   ID: {exam.pk}")
            print(f"   Classroom: {exam.classroom}")
            print(f"   Results: {results_count}/{students_count} students")
            print(f"   URL: http://localhost:8000/exams/{exam.pk}/")
            print()
    else:
        print("\n❌ No exams were created. Check the errors above.")
    
    print("=" * 80)
    print("✅ ALL DONE! Open http://localhost:8000/exams/ to start!")
    print("=" * 80)

if __name__ == '__main__':
    try:
        reset_and_setup()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
