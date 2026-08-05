"""
Reset Exam, ExamResult, and Student Promotion System
ការលុបប្រព័ន្ធប្រឡង លទ្ធផលប្រឡង និងការឡើងថ្នាក់សិស្ស

This script will:
1. Delete all ExamResult records (លទ្ធផលប្រឡង)
2. Delete all Exam records (ប្រឡង)
3. Delete all Score records (ពិន្ទុ)
4. Delete all StudentHistory records (ប្រវត្តិសិស្ស)
5. Reset student promotion fields (កំណត់ឡើងវិញទិន្នន័យឡើងថ្នាក់)
6. Keep ExamType records (keep exam types for reuse)
7. Keep Student, Classroom, Subject, AcademicYear (core data intact)

After running this script, you'll have a clean slate to:
- Create new exams
- Record new exam results
- Promote students based on fresh data
"""

import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crm.settings')
django.setup()

from django.db import transaction
from school.models import (
    Exam, ExamResult, Score, Student, StudentHistory, 
    ExamType, Classroom, Subject, AcademicYear
)


def reset_exam_promotion_system():
    """Delete all exam, exam result, and promotion data"""
    
    print("=" * 80)
    print("🔄 RESET EXAM & PROMOTION SYSTEM")
    print("=" * 80)
    
    # Get counts before deletion
    exam_result_count = ExamResult.objects.count()
    exam_count = Exam.objects.count()
    score_count = Score.objects.count()
    student_history_count = StudentHistory.objects.count()
    students_with_promotion = Student.objects.exclude(promotion_date__isnull=True).count()
    
    print("\n📊 CURRENT DATA COUNTS:")
    print(f"   • ExamResult records: {exam_result_count}")
    print(f"   • Exam records: {exam_count}")
    print(f"   • Score records: {score_count}")
    print(f"   • StudentHistory records: {student_history_count}")
    print(f"   • Students with promotion data: {students_with_promotion}")
    
    print("\n⚠️  WARNING: This will DELETE ALL exam and promotion data!")
    print("   The following will be kept:")
    print("   ✅ ExamType (exam types)")
    print("   ✅ Students (with promotion fields reset)")
    print("   ✅ Classrooms")
    print("   ✅ Subjects")
    print("   ✅ Academic Years")
    print("   ✅ Teachers")
    
    # Confirm deletion
    confirmation = input("\n❓ Type 'DELETE' to confirm: ")
    if confirmation != 'DELETE':
        print("❌ Operation cancelled.")
        return
    
    try:
        with transaction.atomic():
            print("\n🗑️  Starting deletion process...\n")
            
            # Step 1: Delete ExamResult records
            print("1️⃣  Deleting ExamResult records...")
            deleted_exam_results = ExamResult.objects.all().delete()
            print(f"   ✅ Deleted {deleted_exam_results[0]} ExamResult records")
            
            # Step 2: Delete Exam records
            print("\n2️⃣  Deleting Exam records...")
            deleted_exams = Exam.objects.all().delete()
            print(f"   ✅ Deleted {deleted_exams[0]} Exam records")
            
            # Step 3: Delete Score records
            print("\n3️⃣  Deleting Score records...")
            deleted_scores = Score.objects.all().delete()
            print(f"   ✅ Deleted {deleted_scores[0]} Score records")
            
            # Step 4: Delete StudentHistory records
            print("\n4️⃣  Deleting StudentHistory records...")
            deleted_histories = StudentHistory.objects.all().delete()
            print(f"   ✅ Deleted {deleted_histories[0]} StudentHistory records")
            
            # Step 5: Reset student promotion fields
            print("\n5️⃣  Resetting student promotion fields...")
            students = Student.objects.all()
            reset_count = 0
            for student in students:
                if student.promotion_date or student.previous_classroom or student.graduation_date:
                    student.promotion_date = None
                    student.previous_classroom = ''
                    student.graduation_date = None
                    # Clean promotion notes from student notes
                    if student.notes and 'ឡើងថ្នាក់' in student.notes:
                        # Remove promotion notes but keep other notes
                        lines = student.notes.split('\n')
                        student.notes = '\n'.join([line for line in lines if 'ឡើងថ្នាក់' not in line])
                    student.save()
                    reset_count += 1
            print(f"   ✅ Reset promotion data for {reset_count} students")
            
        print("\n" + "=" * 80)
        print("✅ RESET COMPLETED SUCCESSFULLY!")
        print("=" * 80)
        
        # Show final counts
        print("\n📊 FINAL DATA COUNTS:")
        print(f"   • ExamResult records: {ExamResult.objects.count()}")
        print(f"   • Exam records: {Exam.objects.count()}")
        print(f"   • Score records: {Score.objects.count()}")
        print(f"   • StudentHistory records: {StudentHistory.objects.count()}")
        print(f"   • Students with promotion data: {Student.objects.exclude(promotion_date__isnull=True).count()}")
        
        print("\n✨ PRESERVED DATA:")
        print(f"   • ExamType records: {ExamType.objects.count()}")
        print(f"   • Student records: {Student.objects.count()}")
        print(f"   • Classroom records: {Classroom.objects.count()}")
        print(f"   • Subject records: {Subject.objects.count()}")
        print(f"   • AcademicYear records: {AcademicYear.objects.count()}")
        
        print("\n🎯 NEXT STEPS:")
        print("   1. Create new exams using the web interface or API")
        print("   2. Record exam results for students")
        print("   3. Use check_promotion_eligibility API to verify students")
        print("   4. Use bulk_promote API to promote eligible students")
        print("\n   API Endpoints:")
        print("   • POST /api/exams/ - Create exams")
        print("   • POST /api/students/check_promotion_eligibility/ - Check eligibility")
        print("   • POST /api/students/bulk_promote/ - Promote students")
        
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        print("   Transaction rolled back. No data was deleted.")
        import traceback
        traceback.print_exc()


def show_statistics():
    """Show current system statistics"""
    print("\n" + "=" * 80)
    print("📊 CURRENT SYSTEM STATISTICS")
    print("=" * 80)
    
    print("\n🏫 CORE DATA:")
    print(f"   • Academic Years: {AcademicYear.objects.count()}")
    print(f"   • Classrooms: {Classroom.objects.count()}")
    print(f"   • Students: {Student.objects.count()} (Active: {Student.objects.filter(is_active=True).count()})")
    print(f"   • Subjects: {Subject.objects.count()}")
    
    print("\n📝 EXAM DATA:")
    print(f"   • Exam Types: {ExamType.objects.count()}")
    print(f"   • Exams: {Exam.objects.count()}")
    print(f"   • Exam Results: {ExamResult.objects.count()}")
    print(f"   • Scores: {Score.objects.count()}")
    
    print("\n📈 PROMOTION DATA:")
    print(f"   • Student History Records: {StudentHistory.objects.count()}")
    print(f"   • Students with promotion date: {Student.objects.exclude(promotion_date__isnull=True).count()}")
    print(f"   • Students with previous classroom: {Student.objects.exclude(previous_classroom='').count()}")
    
    # Show distribution by grade
    print("\n📊 STUDENT DISTRIBUTION BY GRADE:")
    from django.db.models import Count
    classrooms = Classroom.objects.annotate(student_count=Count('students')).filter(student_count__gt=0)
    for classroom in classrooms:
        print(f"   • {classroom}: {classroom.student_count} students")


if __name__ == '__main__':
    print("\n" + "=" * 80)
    print("🔧 EXAM & PROMOTION SYSTEM RESET TOOL")
    print("=" * 80)
    
    # Show current statistics first
    show_statistics()
    
    print("\n" + "=" * 80)
    print("OPTIONS:")
    print("=" * 80)
    print("1. Reset all exam and promotion data")
    print("2. Show statistics only")
    print("3. Exit")
    
    choice = input("\nEnter your choice (1-3): ")
    
    if choice == '1':
        reset_exam_promotion_system()
    elif choice == '2':
        show_statistics()
    else:
        print("👋 Goodbye!")
