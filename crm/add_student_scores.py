#!/usr/bin/env python
"""
Add Student Scores for Promotion
បន្ថែមពិន្ទុសិស្សដើម្បីឡើងថ្នាក់
"""
import os
import sys
import django

# Setup Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crm.settings')
django.setup()

from school.models import Student, Subject, Score, AcademicYear, Attendance
from datetime import date, timedelta

print("=" * 80)
print("📝 ADD STUDENT SCORES FOR PROMOTION")
print("=" * 80)

# Get the student
students = Student.objects.filter(is_active=True)
if not students.exists():
    print("\n❌ No active students found!")
    sys.exit(1)

print(f"\n✅ Found {students.count()} active student(s)")
for student in students:
    print(f"  • {student.student_id}: {student.last_name} {student.first_name}")
    print(f"    Current Classroom: {student.classroom}")
    
    # Get or create academic year
    academic_year, created = AcademicYear.objects.get_or_create(
        year="2026",
        defaults={'start_date': date(2026, 1, 1), 'end_date': date(2026, 12, 31)}
    )
    if created:
        print(f"    ✅ Created academic year: {academic_year.year}")
    else:
        print(f"    ✅ Using academic year: {academic_year.year}")
    
    # Check if student already has scores
    existing_scores = student.scores.filter(academic_year=academic_year)
    if existing_scores.exists():
        print(f"\n    ⚠️  Student already has {existing_scores.count()} scores:")
        for score in existing_scores:
            print(f"        • {score.subject}: {score.score}/{score.max_score} ({score.percentage():.1f}%)")
        
        response = input("\n    Do you want to add more scores? (y/n): ")
        if response.lower() != 'y':
            print("    Skipping...")
            continue
    
    # Get available subjects
    subjects = Subject.objects.all()
    if not subjects.exists():
        print("\n    Creating default subjects...")
        default_subjects = [
            ('ភាសាខ្មែរ', 'Khmer Language'),
            ('គណិតវិទ្យា', 'Mathematics'),
            ('វិទ្យាសាស្ត្រ', 'Science'),
            ('សង្គមវិទ្យា', 'Social Studies'),
            ('ភាសាអង់គ្លេស', 'English'),
        ]
        for khmer_name, english_name in default_subjects:
            Subject.objects.create(name=khmer_name, name_en=english_name)
        subjects = Subject.objects.all()
        print(f"    ✅ Created {subjects.count()} subjects")
    
    print(f"\n    Available subjects:")
    for i, subject in enumerate(subjects, 1):
        print(f"      {i}. {subject.name}")
    
    # Add scores
    print(f"\n    Adding scores for {student.last_name} {student.first_name}...")
    print("    (Press Enter to skip a subject)")
    
    scores_added = 0
    for subject in subjects:
        try:
            score_input = input(f"      {subject.name} score (0-100): ").strip()
            if not score_input:
                continue
            
            score_value = float(score_input)
            if 0 <= score_value <= 100:
                Score.objects.create(
                    student=student,
                    subject=subject,
                    score=score_value,
                    max_score=100,
                    academic_year=academic_year
                )
                scores_added += 1
                print(f"        ✅ Added: {score_value}/100 ({score_value:.1f}%)")
            else:
                print(f"        ❌ Invalid score (must be 0-100)")
        except ValueError:
            print(f"        ❌ Invalid input")
    
    if scores_added > 0:
        print(f"\n    ✅ Added {scores_added} scores")
        
        # Calculate average
        all_scores = student.scores.filter(academic_year=academic_year)
        total = all_scores.count()
        avg = sum(s.percentage() for s in all_scores) / total if total > 0 else 0
        print(f"    📊 Average: {avg:.1f}% (from {total} subjects)")
    else:
        print(f"\n    ⚠️  No scores added")
    
    # Check/Add attendance
    print(f"\n    Checking attendance...")
    attendances = student.attendances.all()
    if not attendances.exists():
        print(f"    ⚠️  No attendance records found")
        response = input("    Do you want to add sample attendance? (y/n): ")
        if response.lower() == 'y':
            # Add 90 days of attendance (85% present)
            start_date = date(2026, 1, 1)
            for i in range(100):
                attendance_date = start_date + timedelta(days=i)
                # 85% present, 15% absent
                status = 'P' if i % 7 != 0 else 'A'  # Absent every 7th day
                Attendance.objects.create(
                    student=student,
                    date=attendance_date,
                    status=status
                )
            
            # Recalculate
            attendances = student.attendances.all()
            total_days = attendances.count()
            present_days = attendances.filter(status='P').count()
            attendance_rate = (present_days / total_days * 100) if total_days > 0 else 0
            print(f"    ✅ Added {total_days} attendance records")
            print(f"    📊 Attendance: {present_days}/{total_days} days ({attendance_rate:.1f}%)")
    else:
        total_days = attendances.count()
        present_days = attendances.filter(status='P').count()
        attendance_rate = (present_days / total_days * 100) if total_days > 0 else 0
        print(f"    ✅ Attendance: {present_days}/{total_days} days ({attendance_rate:.1f}%)")
    
    # Check promotion eligibility
    print(f"\n    📋 PROMOTION ELIGIBILITY:")
    scores = student.scores.filter(academic_year=academic_year)
    if scores.exists():
        total_subjects = scores.count()
        avg_percentage = sum(score.percentage() for score in scores) / total_subjects
        
        attendances = student.attendances.all()
        total_days = attendances.count()
        present_days = attendances.filter(status='P').count()
        attendance_rate = (present_days / total_days * 100) if total_days > 0 else 0
        
        passing_percentage = 50
        can_promote = (
            avg_percentage >= passing_percentage and 
            total_subjects > 0 and
            attendance_rate >= 80.0
        )
        
        print(f"      ✓ Score ≥ 50%: {'✅' if avg_percentage >= passing_percentage else '❌'} ({avg_percentage:.1f}%)")
        print(f"      ✓ Has subjects: {'✅' if total_subjects > 0 else '❌'} ({total_subjects})")
        print(f"      ✓ Attendance ≥ 80%: {'✅' if attendance_rate >= 80.0 else '❌'} ({attendance_rate:.1f}%)")
        print(f"      → CAN PROMOTE: {'✅ YES' if can_promote else '❌ NO'}")
        
        if can_promote:
            print(f"\n    🎉 Student is eligible for promotion!")
            print(f"    📝 Next step: Go to Student Promotion page to promote")
        else:
            print(f"\n    ⚠️  Student needs:")
            if avg_percentage < passing_percentage:
                print(f"        • Higher scores (current: {avg_percentage:.1f}%, need ≥ {passing_percentage}%)")
            if attendance_rate < 80.0:
                print(f"        • Better attendance (current: {attendance_rate:.1f}%, need ≥ 80%)")
    else:
        print(f"      ❌ No scores found - cannot check eligibility")

print("\n" + "=" * 80)
print("✅ COMPLETE")
print("=" * 80)
print("\n📝 Next steps:")
print("   1. Go to Django admin or app to verify scores")
print("   2. Navigate to: /school/students/promote/")
print("   3. Select current classroom and check results")
print("   4. Select next classroom and promote eligible students")
print("\n" + "=" * 80)
