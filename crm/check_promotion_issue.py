#!/usr/bin/env python
"""
Check Promotion System Issue
Diagnostic script to find why promotion feature is not working
"""
import os
import sys
import django

# Setup Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crm.settings')
django.setup()

from school.models import Grade, Classroom, Student, Score, AcademicYear

print("=" * 80)
print("🔍 PROMOTION SYSTEM DIAGNOSTIC")
print("=" * 80)

# Check Grades
print("\n1️⃣ CHECKING GRADES (ថ្នាក់)")
print("-" * 80)
grades = Grade.objects.all().order_by('grade_number')
print(f"Total Grades: {grades.count()}")
for g in grades:
    print(f"  • Grade {g.grade_number or 'N/A'}: {g.name} (Level: {g.level})")

# Check Classrooms
print("\n2️⃣ CHECKING CLASSROOMS (ថ្នាក់រៀន)")
print("-" * 80)
classrooms = Classroom.objects.all().select_related('grade', 'academic_year')
print(f"Total Classrooms: {classrooms.count()}")
for c in classrooms:
    grade_info = f"Grade {c.grade.grade_number}" if c.grade and c.grade.grade_number else "No Grade#"
    year_info = c.academic_year.year if c.academic_year else "No Year"
    print(f"  • {str(c)} ({grade_info}, {year_info})")

# Check Students
print("\n3️⃣ CHECKING STUDENTS (សិស្ស)")
print("-" * 80)
students = Student.objects.filter(is_active=True).select_related('classroom')
print(f"Total Active Students: {students.count()}")
student_by_classroom = {}
for s in students:
    classroom_name = str(s.classroom) if s.classroom else "No Classroom"
    if classroom_name not in student_by_classroom:
        student_by_classroom[classroom_name] = []
    student_by_classroom[classroom_name].append(s)

for classroom_name, student_list in student_by_classroom.items():
    print(f"  • {classroom_name}: {len(student_list)} students")

# Check if students have scores
print("\n4️⃣ CHECKING STUDENT SCORES (ពិន្ទុ)")
print("-" * 80)
students_with_scores = Student.objects.filter(is_active=True, scores__isnull=False).distinct().count()
students_without_scores = students.count() - students_with_scores
print(f"  • Students with scores: {students_with_scores}")
print(f"  • Students without scores: {students_without_scores}")

# Check sample student eligibility
print("\n5️⃣ CHECKING PROMOTION ELIGIBILITY (លក្ខខណ្ឌឡើងថ្នាក់)")
print("-" * 80)
sample_student = students.first()
if sample_student:
    print(f"Sample Student: {sample_student.last_name} {sample_student.first_name} ({sample_student.student_id})")
    print(f"  • Current Classroom: {sample_student.classroom}")
    
    # Check scores
    scores = sample_student.scores.all()
    if scores.exists():
        total_subjects = scores.count()
        avg_percentage = sum(score.percentage() for score in scores) / total_subjects
        print(f"  • Scores: {total_subjects} subjects, Average: {avg_percentage:.1f}%")
        
        # Check attendance
        attendances = sample_student.attendances.all()
        total_days = attendances.count()
        present_days = attendances.filter(status='P').count()
        attendance_rate = (present_days / total_days * 100) if total_days > 0 else 0
        print(f"  • Attendance: {present_days}/{total_days} days ({attendance_rate:.1f}%)")
        
        # Check eligibility
        passing_percentage = 50
        can_promote = (
            avg_percentage >= passing_percentage and 
            total_subjects > 0 and
            attendance_rate >= 80.0
        )
        
        print(f"\n  ELIGIBILITY CHECK:")
        print(f"    ✓ Score ≥ {passing_percentage}%: {'✅' if avg_percentage >= passing_percentage else '❌'} ({avg_percentage:.1f}%)")
        print(f"    ✓ Has subjects: {'✅' if total_subjects > 0 else '❌'} ({total_subjects})")
        print(f"    ✓ Attendance ≥ 80%: {'✅' if attendance_rate >= 80.0 else '❌'} ({attendance_rate:.1f}%)")
        print(f"    → CAN PROMOTE: {'✅ YES' if can_promote else '❌ NO'}")
    else:
        print(f"  • ❌ No scores found")

# Check next grade availability
print("\n6️⃣ CHECKING NEXT GRADE CLASSROOMS (ថ្នាក់បន្ទាប់)")
print("-" * 80)
for c in classrooms:
    if c.grade and c.grade.grade_number:
        current_grade_num = c.grade.grade_number
        next_grade_num = current_grade_num + 1
        
        # Find classrooms with next grade
        next_classrooms = Classroom.objects.filter(
            grade__grade_number=next_grade_num
        )
        
        if next_classrooms.exists():
            print(f"  • {str(c)} (Grade {current_grade_num}) → Can promote to:")
            for nc in next_classrooms:
                print(f"      ✅ {str(nc)} (Grade {nc.grade.grade_number})")
        else:
            print(f"  • {str(c)} (Grade {current_grade_num}) → ❌ No Grade {next_grade_num} classroom available")

print("\n" + "=" * 80)
print("✅ DIAGNOSTIC COMPLETE")
print("=" * 80)
