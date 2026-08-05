import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crm.settings')
django.setup()

from school.models import Exam, ExamResult, Score, Attendance, Student

print("=" * 60)
print("SYSTEM STATUS")
print("=" * 60)
print(f"Exams: {Exam.objects.count()}")
print(f"Exam Results: {ExamResult.objects.count()}")
print(f"Scores: {Score.objects.count()}")
print(f"Attendance Records: {Attendance.objects.count()}")
print(f"Active Students: {Student.objects.filter(is_active=True).count()}")

student = Student.objects.filter(is_active=True).first()
if student:
    print(f"\nStudent: {student}")
    print(f"  Classroom: {student.classroom}")
    print(f"  Exam Results: {student.exam_results.count()}")
    print(f"  Scores: {student.scores.count()}")
    print(f"  Attendance: {student.attendances.count()}")
    
    # Calculate average
    if student.scores.exists():
        avg = sum([float(s.percentage()) for s in student.scores.all()]) / student.scores.count()
        print(f"  Average Score: {avg:.1f}%")
    
    # Attendance rate
    if student.attendances.exists():
        present = student.attendances.filter(status='P').count()
        total = student.attendances.count()
        rate = (present / total * 100) if total > 0 else 0
        print(f"  Attendance Rate: {rate:.1f}% ({present}/{total})")

print("\n" + "=" * 60)
print("SYSTEM IS READY!")
print("=" * 60)
