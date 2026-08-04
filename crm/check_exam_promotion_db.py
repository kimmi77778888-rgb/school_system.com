#!/usr/bin/env python
"""
Script to check and fix Exam, ExamResult database issues for promotion system
ស្គ្រីបពិនិត្យ និងកែបញ្ហាមូលដ្ឋានទិន្នន័យប្រឡង និងឡើងថ្នាក់
"""

import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crm.settings')
django.setup()

from django.db import connection
from school.models import (
    Exam, ExamResult, ExamType, Student, Subject, 
    Classroom, AcademicYear, Grade
)

def check_database_tables():
    """Check if all required tables exist"""
    print("=" * 80)
    print("🔍 ពិនិត្យតារាងមូលដ្ឋានទិន្នន័យ | Checking Database Tables")
    print("=" * 80)
    
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name LIKE 'school_%'
            ORDER BY name;
        """)
        tables = cursor.fetchall()
        
        print("\n✅ តារាងដែលមាន | Available Tables:")
        for table in tables:
            print(f"   - {table[0]}")
    
    print("\n")

def check_exam_tables():
    """Check Exam-related table structure"""
    print("=" * 80)
    print("🔍 ពិនិត្យរចនាសម្ព័ន្ធតារាងប្រឡង | Checking Exam Table Structure")
    print("=" * 80)
    
    with connection.cursor() as cursor:
        # Check Exam table
        cursor.execute("PRAGMA table_info(school_exam);")
        exam_columns = cursor.fetchall()
        
        print("\n📊 school_exam columns:")
        for col in exam_columns:
            print(f"   {col[1]:20s} {col[2]:15s} {'NOT NULL' if col[3] else ''}")
        
        # Check ExamResult table
        cursor.execute("PRAGMA table_info(school_examresult);")
        result_columns = cursor.fetchall()
        
        print("\n📊 school_examresult columns:")
        for col in result_columns:
            print(f"   {col[1]:20s} {col[2]:15s} {'NOT NULL' if col[3] else ''}")
        
        # Check ExamType table
        cursor.execute("PRAGMA table_info(school_examtype);")
        type_columns = cursor.fetchall()
        
        print("\n📊 school_examtype columns:")
        for col in type_columns:
            print(f"   {col[1]:20s} {col[2]:15s} {'NOT NULL' if col[3] else ''}")

def check_exam_data():
    """Check existing exam data"""
    print("\n" + "=" * 80)
    print("📈 ពិនិត្យទិន្នន័យប្រឡង | Checking Exam Data")
    print("=" * 80)
    
    # Count exams
    exam_count = Exam.objects.count()
    print(f"\n📝 ចំនួនប្រឡងសរុប | Total Exams: {exam_count}")
    
    if exam_count > 0:
        print("\n   Recent Exams:")
        for exam in Exam.objects.select_related('exam_type', 'subject', 'classroom')[:5]:
            print(f"   - {exam.exam_id}: {exam.name} | {exam.subject.name} | {exam.classroom}")
    
    # Count exam results
    result_count = ExamResult.objects.count()
    print(f"\n📊 ចំនួនលទ្ធផលប្រឡងសរុប | Total Exam Results: {result_count}")
    
    if result_count > 0:
        print("\n   Recent Results:")
        for result in ExamResult.objects.select_related('exam', 'student')[:5]:
            print(f"   - {result.student.get_full_name()}: {result.score}/{result.exam.max_score} ({result.percentage()}%)")
    
    # Count exam types
    type_count = ExamType.objects.count()
    print(f"\n🏷️  ចំនួនប្រភេទប្រឡង | Total Exam Types: {type_count}")
    
    if type_count > 0:
        print("\n   Exam Types:")
        for exam_type in ExamType.objects.all():
            print(f"   - {exam_type.name} ({exam_type.code}) - Weight: {exam_type.weight_percentage}%")

def check_promotion_readiness():
    """Check if system is ready for promotion based on exam data"""
    print("\n" + "=" * 80)
    print("🎓 ពិនិត្យស្ថានភាពឡើងថ្នាក់ | Checking Promotion Readiness")
    print("=" * 80)
    
    # Get active students
    active_students = Student.objects.filter(is_active=True).count()
    print(f"\n👥 សិស្សសកម្ម | Active Students: {active_students}")
    
    # Check how many students have exam results
    students_with_results = Student.objects.filter(
        exam_results__isnull=False
    ).distinct().count()
    
    print(f"📝 សិស្សមានលទ្ធផលប្រឡង | Students with Exam Results: {students_with_results}")
    
    # Check students by classroom
    print("\n📚 សិស្សតាមថ្នាក់រៀន | Students by Classroom:")
    classrooms = Classroom.objects.filter(students__is_active=True).distinct()
    
    for classroom in classrooms:
        student_count = classroom.students.filter(is_active=True).count()
        results_count = ExamResult.objects.filter(
            student__classroom=classroom,
            student__is_active=True
        ).distinct('student').count()
        
        print(f"   {classroom}: {student_count} សិស្ស, {results_count} មានលទ្ធផល")

def check_missing_data():
    """Check for missing or problematic data"""
    print("\n" + "=" * 80)
    print("⚠️  ពិនិត្យទិន្នន័យខ្វះ | Checking Missing Data")
    print("=" * 80)
    
    # Check students without exam results
    students_without_results = Student.objects.filter(
        is_active=True,
        exam_results__isnull=True
    ).count()
    
    if students_without_results > 0:
        print(f"\n⚠️  {students_without_results} សិស្សមិនទាន់មានលទ្ធផលប្រឡង")
        print("   Students without exam results - they cannot be promoted yet")
    
    # Check exams without results
    exams_without_results = Exam.objects.filter(
        exam_results__isnull=True,
        status='completed'
    ).count()
    
    if exams_without_results > 0:
        print(f"\n⚠️  {exams_without_results} ប្រឡងបានបញ្ចប់ប៉ុន្តែមិនទាន់បញ្ចូលពិន្ទុ")
        print("   Completed exams without results entered")
    
    # Check exam results without passing status calculated
    results_without_pass = ExamResult.objects.filter(
        is_passed=False,
        score__gte=50
    ).count()
    
    if results_without_pass > 0:
        print(f"\n⚠️  {results_without_pass} លទ្ធផលប្រឡងមានបញ្ហាគណនា is_passed")
        print("   Exam results with incorrect pass/fail calculation")

def fix_exam_results_calculation():
    """Fix any exam results that have incorrect calculated fields"""
    print("\n" + "=" * 80)
    print("🔧 កែលម្អការគណនាលទ្ធផលប្រឡង | Fixing Exam Result Calculations")
    print("=" * 80)
    
    fixed_count = 0
    
    for result in ExamResult.objects.all():
        original_passed = result.is_passed
        original_grade = result.grade_letter
        
        # Recalculate by saving (triggers save() method logic)
        result.save()
        
        if original_passed != result.is_passed or original_grade != result.grade_letter:
            fixed_count += 1
            print(f"   ✓ Fixed {result.student.get_full_name()}: "
                  f"Grade {original_grade}→{result.grade_letter}, "
                  f"Pass {original_passed}→{result.is_passed}")
    
    if fixed_count > 0:
        print(f"\n✅ បានកែលម្អ {fixed_count} លទ្ធផល | Fixed {fixed_count} results")
    else:
        print("\n✅ លទ្ធផលទាំងអស់ត្រឹមត្រូវ | All results are correct")

def suggest_fixes():
    """Suggest what needs to be fixed"""
    print("\n" + "=" * 80)
    print("💡 ការណែនាំកែលម្អ | Suggestions for Fixes")
    print("=" * 80)
    
    exam_count = Exam.objects.count()
    result_count = ExamResult.objects.count()
    type_count = ExamType.objects.count()
    
    if type_count == 0:
        print("\n❌ បញ្ហា | ISSUE: មិនមានប្រភេទប្រឡង")
        print("   ដំណោះស្រាយ | Solution: បង្កើតប្រភេទប្រឡង (Midterm, Final, Quiz)")
        print("   Command: python manage.py shell")
        print("   >>> from school.models import ExamType")
        print("   >>> ExamType.objects.create(name='Midterm', code='MID', weight_percentage=30)")
        print("   >>> ExamType.objects.create(name='Final', code='FINAL', weight_percentage=70)")
    
    if exam_count == 0:
        print("\n❌ បញ្ហា | ISSUE: មិនមានប្រឡង")
        print("   ដំណោះស្រាយ | Solution: បង្កើតប្រឡងនៅក្នុង Admin Panel")
        print("   URL: /admin/school/exam/add/")
    
    if result_count == 0 and exam_count > 0:
        print("\n❌ បញ្ហា | ISSUE: មានប្រឡងប៉ុន្តែមិនមានលទ្ធផល")
        print("   ដំណោះស្រាយ | Solution: បញ្ចូលពិន្ទុប្រឡងនៅក្នុង Admin Panel")
        print("   URL: /admin/school/examresult/add/")
    
    # Check if we can promote
    students_can_promote = 0
    for student in Student.objects.filter(is_active=True):
        scores = student.scores.all()
        if scores.exists():
            avg = sum(s.percentage() for s in scores) / scores.count()
            if avg >= 50:
                students_can_promote += 1
    
    print(f"\n✅ សិស្សអាចឡើងថ្នាក់បាន | Students eligible for promotion: {students_can_promote}")

def main():
    """Main execution"""
    print("\n")
    print("╔" + "=" * 78 + "╗")
    print("║" + " " * 78 + "║")
    print("║" + " ពិនិត្យប្រព័ន្ធប្រឡង និងឡើងថ្នាក់ ".center(78) + "║")
    print("║" + " Exam and Promotion System Database Check ".center(78) + "║")
    print("║" + " " * 78 + "║")
    print("╚" + "=" * 78 + "╝")
    
    try:
        check_database_tables()
        check_exam_tables()
        check_exam_data()
        check_promotion_readiness()
        check_missing_data()
        fix_exam_results_calculation()
        suggest_fixes()
        
        print("\n" + "=" * 80)
        print("✅ ការពិនិត្យបានបញ្ចប់ | Check Complete!")
        print("=" * 80)
        print("\n")
        
    except Exception as e:
        print(f"\n❌ កំហុស | Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
