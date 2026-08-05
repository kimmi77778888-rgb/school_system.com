"""
Complete System Setup - Make it Ready!
ដំឡើងប្រព័ន្ធពេញលេញ - រៀបចំអោយបានស្រេច!

This script will:
1. Create exams for all subjects in all classrooms
2. Add sample exam results for students
3. Make the system ready for promotion
"""

import os
import django
from datetime import date, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crm.settings')
django.setup()

from django.db import transaction
from school.models import (
    Exam, ExamResult, ExamType, Subject, Classroom, 
    Student, AcademicYear, Score, Attendance
)

print("=" * 80)
print("🚀 COMPLETE SYSTEM SETUP")
print("=" * 80)

# Get data
exam_types = ExamType.objects.all()
classrooms = Classroom.objects.all()
subjects = Subject.objects.all()
students = Student.objects.filter(is_active=True)
academic_years = AcademicYear.objects.all()

print(f"\n📊 CURRENT DATA:")
print(f"   • Exam Types: {exam_types.count()}")
print(f"   • Classrooms: {classrooms.count()}")
print(f"   • Subjects: {subjects.count()}")
print(f"   • Active Students: {students.count()}")
print(f"   • Academic Years: {academic_years.count()}")

if not exam_types.exists():
    print("\n❌ No exam types found! Creating default exam types...")
    with transaction.atomic():
        ExamType.objects.create(name="ប្រឡងកណ្តាលឆមាស (Midterm)", code="MID", weight_percentage=30)
        ExamType.objects.create(name="ប្រឡងចុងឆមាស (Final)", code="FINAL", weight_percentage=70)
        ExamType.objects.create(name="តេស្ត (Quiz)", code="QUIZ", weight_percentage=10)
    exam_types = ExamType.objects.all()
    print(f"   ✅ Created {exam_types.count()} exam types")

if not students.exists():
    print("\n❌ No active students found! Cannot create exam results.")
    print("   Please add students first.")
    exit(1)

# Setup configuration
print("\n⚙️  SETUP CONFIGURATION:")
print("   • Will create exams for ALL classrooms")
print("   • Will use Midterm exam type")
print("   • Exam date: 2026-08-15")
print("   • Max score: 100")
print("   • Passing score: 50")

exam_date = date(2026, 8, 15)
midterm_exam_type = exam_types.filter(name__contains='Midterm').first() or exam_types.first()

print(f"\n   Using Exam Type: {midterm_exam_type.name}")

try:
    with transaction.atomic():
        print("\n" + "=" * 80)
        print("📝 STEP 1: CREATING EXAMS")
        print("=" * 80)
        
        created_exams = 0
        skipped_exams = 0
        
        for classroom in classrooms:
            if not classroom.academic_year:
                print(f"   ⚠️  Skipped {classroom} (no academic year)")
                continue
            
            print(f"\n   📚 {classroom}:")
            
            for subject in subjects:
                # Check if exam already exists
                existing = Exam.objects.filter(
                    classroom=classroom,
                    subject=subject,
                    exam_type=midterm_exam_type,
                    academic_year=classroom.academic_year
                ).exists()
                
                if existing:
                    print(f"      ⚠️  {subject.name} (already exists)")
                    skipped_exams += 1
                    continue
                
                # Create exam
                exam = Exam.objects.create(
                    name=f"{midterm_exam_type.name} - {subject.name}",
                    exam_type=midterm_exam_type,
                    subject=subject,
                    classroom=classroom,
                    academic_year=classroom.academic_year,
                    date=exam_date,
                    max_score=100,
                    passing_score=50,
                    status='completed',
                    description=f"{midterm_exam_type.name} for {subject.name} in {classroom}"
                )
                print(f"      ✅ {subject.name} ({exam.exam_id})")
                created_exams += 1
        
        print(f"\n   📊 Created: {created_exams} exams")
        print(f"   ⚠️  Skipped: {skipped_exams} exams (already exist)")
        
        # Step 2: Create exam results for students
        print("\n" + "=" * 80)
        print("📝 STEP 2: CREATING EXAM RESULTS")
        print("=" * 80)
        
        created_results = 0
        skipped_results = 0
        
        # Get all exams
        all_exams = Exam.objects.all()
        
        for student in students:
            if not student.classroom:
                print(f"   ⚠️  Skipped {student} (no classroom)")
                continue
            
            print(f"\n   👨‍🎓 {student}:")
            
            # Get exams for this student's classroom
            classroom_exams = all_exams.filter(classroom=student.classroom)
            
            for exam in classroom_exams:
                # Check if result exists
                existing = ExamResult.objects.filter(exam=exam, student=student).exists()
                
                if existing:
                    print(f"      ⚠️  {exam.subject.name} (already exists)")
                    skipped_results += 1
                    continue
                
                # Generate realistic score (60-95 for passing, 30-45 for failing)
                import random
                from decimal import Decimal
                # 80% chance of passing
                if random.random() < 0.8:
                    score = Decimal(str(round(random.uniform(60, 95), 2)))
                else:
                    score = Decimal(str(round(random.uniform(30, 45), 2)))
                
                # Create exam result
                ExamResult.objects.create(
                    exam=exam,
                    student=student,
                    score=score,
                    was_present=True,
                    remarks="Automatically generated sample result"
                )
                
                # Also create or update Score record for compatibility
                Score.objects.update_or_create(
                    student=student,
                    subject=exam.subject,
                    exam_type=exam.exam_type,
                    academic_year=exam.academic_year,
                    defaults={
                        'exam': exam,
                        'score': score,
                        'max_score': Decimal('100'),
                        'remarks': "Automatically generated sample score"
                    }
                )
                
                status = "✅" if score >= 50 else "❌"
                print(f"      {status} {exam.subject.name}: {score:.1f}/100")
                created_results += 1
        
        print(f"\n   📊 Created: {created_results} exam results")
        print(f"   ⚠️  Skipped: {skipped_results} results (already exist)")
        
        # Step 3: Create attendance records
        print("\n" + "=" * 80)
        print("📝 STEP 3: CREATING ATTENDANCE RECORDS")
        print("=" * 80)
        
        created_attendance = 0
        
        for student in students:
            print(f"\n   👨‍🎓 {student}:")
            
            # Create attendance for last 180 days (school year)
            start_date = date.today() - timedelta(days=180)
            
            attendance_count = 0
            for i in range(180):
                current_date = start_date + timedelta(days=i)
                
                # Skip weekends
                if current_date.weekday() in [5, 6]:
                    continue
                
                # Check if attendance exists
                if Attendance.objects.filter(student=student, date=current_date).exists():
                    continue
                
                # 90% chance of being present
                import random
                status = 'P' if random.random() < 0.90 else 'A'
                
                Attendance.objects.create(
                    student=student,
                    date=current_date,
                    status=status
                )
                attendance_count += 1
            
            created_attendance += attendance_count
            print(f"      ✅ Created {attendance_count} attendance records")
        
        print(f"\n   📊 Total attendance records created: {created_attendance}")
    
    print("\n" + "=" * 80)
    print("✅ SYSTEM SETUP COMPLETED SUCCESSFULLY!")
    print("=" * 80)
    
    # Final summary
    print("\n📊 FINAL SUMMARY:")
    print(f"   • Total Exams: {Exam.objects.count()}")
    print(f"   • Total Exam Results: {ExamResult.objects.count()}")
    print(f"   • Total Scores: {Score.objects.count()}")
    print(f"   • Total Attendance Records: {Attendance.objects.count()}")
    
    print("\n🎯 NEXT STEPS:")
    print("   1. Check exams in web interface: /exams/")
    print("   2. View student scores: /students/")
    print("   3. Check promotion eligibility: POST /api/students/check_promotion_eligibility/")
    print("   4. Promote students: POST /api/students/bulk_promote/")
    
    print("\n✨ Your system is now ready to use!")
    
except Exception as e:
    print(f"\n❌ ERROR: {str(e)}")
    import traceback
    traceback.print_exc()
