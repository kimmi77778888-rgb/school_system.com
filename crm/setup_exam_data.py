"""
Setup script to create sample exam and exam result data
This will allow you to test the exam result detail system
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crm.settings')
django.setup()

from school.models import (
    Exam, ExamResult, ExamType, Student, Subject, 
    Classroom, AcademicYear, User
)
from decimal import Decimal
from datetime import date, time

def create_sample_exam_data():
    print("=" * 80)
    print("Creating Sample Exam Data for Testing")
    print("=" * 80)
    
    # Step 1: Get or create ExamType
    print("\n1. Creating/Getting Exam Types...")
    midterm, created = ExamType.objects.get_or_create(
        name='ប្រឡងកណ្តាលឆមាស (Midterm)',
        defaults={
            'code': 'MIDTERM',
            'description': 'Mid-semester examination',
            'weight_percentage': Decimal('30.00'),
            'is_active': True
        }
    )
    print(f"   {'Created' if created else 'Found'} ExamType: {midterm.name}")
    
    final, created = ExamType.objects.get_or_create(
        name='ប្រឡងចុងឆមាស (Final)',
        defaults={
            'code': 'FINAL',
            'description': 'End of semester examination',
            'weight_percentage': Decimal('70.00'),
            'is_active': True
        }
    )
    print(f"   {'Created' if created else 'Found'} ExamType: {final.name}")
    
    # Step 2: Get active classroom
    print("\n2. Getting Active Classroom...")
    classroom = Classroom.objects.filter(
        students__is_active=True
    ).distinct().first()
    
    if not classroom:
        print("   ❌ No classroom with active students found!")
        return
    
    print(f"   ✓ Using Classroom: {classroom}")
    
    # Step 3: Get subjects for this classroom's grade
    print("\n3. Getting Subjects...")
    subjects = Subject.objects.filter(grade=classroom.grade)[:2]
    
    if not subjects.exists():
        print("   ❌ No subjects found for this grade!")
        return
    
    print(f"   ✓ Found {subjects.count()} subjects")
    
    # Step 4: Get or create academic year
    print("\n4. Getting Academic Year...")
    academic_year = classroom.academic_year
    if not academic_year:
        academic_year = AcademicYear.objects.filter(is_active=True).first()
    
    if not academic_year:
        print("   ❌ No academic year found!")
        return
    
    print(f"   ✓ Using Academic Year: {academic_year.year}")
    
    # Step 5: Get admin user for created_by
    print("\n5. Getting Admin User...")
    admin_user = User.objects.filter(is_superuser=True).first()
    if not admin_user:
        admin_user = User.objects.filter(is_staff=True).first()
    
    print(f"   ✓ Using User: {admin_user.username if admin_user else 'None'}")
    
    # Step 6: Create Exams
    print("\n6. Creating Exams...")
    exams_created = 0
    
    for subject in subjects:
        # Create Midterm Exam
        exam, created = Exam.objects.get_or_create(
            name=f'ប្រឡងកណ្តាលឆមាស - {subject.name}',
            subject=subject,
            classroom=classroom,
            academic_year=academic_year,
            exam_type=midterm,
            defaults={
                'date': date(2026, 7, 15),
                'exam_time': time(8, 0),
                'duration_minutes': 90,
                'max_score': Decimal('100.00'),
                'passing_score': Decimal('50.00'),
                'status': 'completed',
                'description': f'Midterm examination for {subject.name}',
                'instructions': 'Answer all questions. Show your work.',
                'created_by': admin_user
            }
        )
        if created:
            exams_created += 1
            print(f"   ✓ Created: {exam.name}")
            
            # Step 7: Create ExamResults for this exam
            students = classroom.students.filter(is_active=True)[:10]  # Get first 10 students
            results_created = 0
            
            print(f"      Creating results for {students.count()} students...")
            
            # Sample scores (varied for realistic data)
            sample_scores = [95, 88, 92, 75, 68, 85, 78, 90, 82, 70]
            
            for idx, student in enumerate(students):
                score = Decimal(str(sample_scores[idx % len(sample_scores)]))
                
                result, result_created = ExamResult.objects.get_or_create(
                    exam=exam,
                    student=student,
                    defaults={
                        'score': score,
                        'was_present': True,
                        'remarks': 'Good effort!' if score >= 80 else 'Keep practicing',
                        'strengths': 'Strong understanding of concepts' if score >= 80 else 'Shows effort',
                        'areas_to_improve': 'Continue practicing' if score >= 80 else 'Need more practice on fundamentals',
                        'recorded_by': admin_user
                    }
                )
                
                if result_created:
                    results_created += 1
            
            print(f"      ✓ Created {results_created} exam results")
    
    print(f"\n✓ Created {exams_created} new exams")
    
    # Step 8: Summary
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Total Exams in database: {Exam.objects.count()}")
    print(f"Total ExamResults in database: {ExamResult.objects.count()}")
    
    # Show created exams
    print("\nCreated Exams:")
    for exam in Exam.objects.all():
        results_count = exam.exam_results.count()
        print(f"  - {exam.name}")
        print(f"    ID: {exam.pk}")
        print(f"    URL: http://localhost:8000/exams/{exam.pk}/")
        print(f"    Results: {results_count}/{exam.classroom.students.filter(is_active=True).count()}")
        print()
    
    print("=" * 80)
    print("✅ SETUP COMPLETE!")
    print("=" * 80)
    print("\nYou can now:")
    print("1. Go to: http://localhost:8000/exams/")
    print("2. Click the eye icon (👁️) to view exam details")
    print("3. Click eye icon next to students to see individual results")
    print("\nOr directly visit the URLs shown above!")

if __name__ == '__main__':
    try:
        create_sample_exam_data()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
