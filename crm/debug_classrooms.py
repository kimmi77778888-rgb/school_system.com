"""
Debug script to check classroom and grade relationships
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crm.settings')
django.setup()

from school.models import Classroom, Grade, AcademicYear

print("=" * 70)
print("CLASSROOM DEBUG REPORT")
print("=" * 70)

# List all grades
print("\n📚 ALL GRADES:")
print("-" * 70)
grades = Grade.objects.all().order_by('grade_number')
for grade in grades:
    print(f"  • {grade.name} (#{grade.grade_number}) - Level: {grade.level}")

# List all academic years
print("\n📅 ALL ACADEMIC YEARS:")
print("-" * 70)
years = AcademicYear.objects.all()
for year in years:
    print(f"  • {year.year}")

# List all classrooms
print("\n🏫 ALL CLASSROOMS:")
print("-" * 70)
classrooms = Classroom.objects.select_related('grade', 'academic_year').all()
print(f"Total: {classrooms.count()} classrooms\n")

for cls in classrooms:
    grade_num = cls.grade.grade_number if cls.grade else "?"
    year = cls.academic_year.year if cls.academic_year else "No year"
    print(f"  {cls.pk}. {cls} - Grade #{grade_num} - Year: {year}")

# Check promotion paths
print("\n🔄 PROMOTION PATHS:")
print("-" * 70)
for cls in classrooms:
    if cls.grade and cls.grade.grade_number:
        current_grade = cls.grade.grade_number
        next_grade = current_grade + 1
        
        # Find classrooms with next grade
        next_classrooms = Classroom.objects.filter(
            grade__grade_number=next_grade
        ).select_related('grade', 'academic_year')
        
        if next_classrooms.exists():
            print(f"✅ {cls} (Grade {current_grade}) → Can promote to:")
            for nc in next_classrooms:
                print(f"    • {nc} (Grade {nc.grade.grade_number})")
        else:
            print(f"❌ {cls} (Grade {current_grade}) → NO NEXT CLASSROOM (needs Grade {next_grade})")

# Check grade sequence
print("\n📊 GRADE SEQUENCE CHECK:")
print("-" * 70)
for i in range(1, 13):
    classrooms_at_grade = Classroom.objects.filter(grade__grade_number=i).count()
    status = "✅" if classrooms_at_grade > 0 else "❌"
    print(f"  {status} Grade {i}: {classrooms_at_grade} classroom(s)")

print("\n" + "=" * 70)
print("END OF REPORT")
print("=" * 70)
