"""
Direct deletion script - No interaction required
លុបទិន្នន័យប្រឡងភ្លាមៗ - គ្មានការសួរសំណួរ
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crm.settings')
django.setup()

from django.db import transaction
from school.models import Exam, ExamResult, Score, Student, StudentHistory

print("=" * 80)
print("🗑️  DELETING ALL EXAM & PROMOTION DATA")
print("=" * 80)

# Show before counts
print("\n📊 BEFORE DELETION:")
exam_count = Exam.objects.count()
exam_result_count = ExamResult.objects.count()
score_count = Score.objects.count()
student_history_count = StudentHistory.objects.count()
students_with_promotion = Student.objects.exclude(promotion_date__isnull=True).count()

print(f"   • Exams: {exam_count}")
print(f"   • ExamResults: {exam_result_count}")
print(f"   • Scores: {score_count}")
print(f"   • StudentHistory: {student_history_count}")
print(f"   • Students with promotion data: {students_with_promotion}")

try:
    with transaction.atomic():
        print("\n🗑️  Deleting...\n")
        
        # Delete ExamResult
        deleted_exam_results = ExamResult.objects.all().delete()
        print(f"   ✅ Deleted {deleted_exam_results[0]} ExamResult records")
        
        # Delete Exam
        deleted_exams = Exam.objects.all().delete()
        print(f"   ✅ Deleted {deleted_exams[0]} Exam records")
        
        # Delete Score
        deleted_scores = Score.objects.all().delete()
        print(f"   ✅ Deleted {deleted_scores[0]} Score records")
        
        # Delete StudentHistory
        deleted_histories = StudentHistory.objects.all().delete()
        print(f"   ✅ Deleted {deleted_histories[0]} StudentHistory records")
        
        # Reset student promotion fields
        print(f"\n   🔄 Resetting student promotion fields...")
        students = Student.objects.all()
        reset_count = 0
        for student in students:
            if student.promotion_date or student.previous_classroom or student.graduation_date:
                student.promotion_date = None
                student.previous_classroom = ''
                student.graduation_date = None
                # Clean promotion notes
                if student.notes and 'ឡើងថ្នាក់' in student.notes:
                    lines = student.notes.split('\n')
                    student.notes = '\n'.join([line for line in lines if 'ឡើងថ្នាក់' not in line])
                student.save()
                reset_count += 1
        print(f"   ✅ Reset {reset_count} student records")
    
    print("\n" + "=" * 80)
    print("✅ DELETION COMPLETED SUCCESSFULLY!")
    print("=" * 80)
    
    # Show after counts
    print("\n📊 AFTER DELETION:")
    print(f"   • Exams: {Exam.objects.count()}")
    print(f"   • ExamResults: {ExamResult.objects.count()}")
    print(f"   • Scores: {Score.objects.count()}")
    print(f"   • StudentHistory: {StudentHistory.objects.count()}")
    print(f"   • Students with promotion data: {Student.objects.exclude(promotion_date__isnull=True).count()}")
    
    print("\n✅ All exam and promotion data has been deleted!")
    print("📋 Core data preserved (Students, Classrooms, Subjects, etc.)")
    
except Exception as e:
    print(f"\n❌ ERROR: {str(e)}")
    import traceback
    traceback.print_exc()
