"""
Bulk Import Exam Results from CSV
នាំចូលលទ្ធផលប្រឡងជាច្រើនពី CSV

This script allows you to import exam results from CSV files.
Useful for importing data from Excel or other systems.
"""

import os
import django
import csv
from datetime import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crm.settings')
django.setup()

from school.models import Exam, ExamResult, Student


def create_sample_csv():
    """Create a sample CSV template for exam results"""
    sample_file = 'exam_results_template.csv'
    
    with open(sample_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            'exam_id', 'student_id', 'score', 'was_present', 'absent_reason', 'remarks'
        ])
        writer.writerow(['EXM-0001', 'STU-0001', '85.00', 'TRUE', '', 'Good performance'])
        writer.writerow(['EXM-0001', 'STU-0002', '92.00', 'TRUE', '', 'Excellent work'])
        writer.writerow(['EXM-0001', 'STU-0003', '45.00', 'TRUE', '', 'Needs improvement'])
        writer.writerow(['EXM-0001', 'STU-0004', '0.00', 'FALSE', 'Sick', 'Was absent due to illness'])
    
    print(f"✅ Created sample CSV template: {sample_file}")
    print("\nCSV Format:")
    print("  • exam_id: Exam ID (e.g., EXM-0001)")
    print("  • student_id: Student ID (e.g., STU-0001)")
    print("  • score: Exam score (e.g., 85.00)")
    print("  • was_present: TRUE or FALSE")
    print("  • absent_reason: Reason if absent (optional)")
    print("  • remarks: Teacher comments (optional)")


def import_exam_results(csv_file, update_existing=False):
    """
    Import exam results from CSV file
    
    Args:
        csv_file: Path to CSV file
        update_existing: If True, update existing results; if False, skip existing
    """
    print("=" * 80)
    print("📥 IMPORTING EXAM RESULTS")
    print("=" * 80)
    print(f"File: {csv_file}")
    print(f"Update existing: {update_existing}")
    
    if not os.path.exists(csv_file):
        print(f"❌ File not found: {csv_file}")
        return
    
    success_count = 0
    skip_count = 0
    error_count = 0
    errors = []
    
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        
        print("\n📊 Processing records...\n")
        
        for row_num, row in enumerate(reader, start=2):
            try:
                # Get exam
                exam_id = row['exam_id'].strip()
                try:
                    exam = Exam.objects.get(exam_id=exam_id)
                except Exam.DoesNotExist:
                    errors.append(f"Row {row_num}: Exam {exam_id} not found")
                    error_count += 1
                    continue
                
                # Get student
                student_id = row['student_id'].strip()
                try:
                    student = Student.objects.get(student_id=student_id)
                except Student.DoesNotExist:
                    errors.append(f"Row {row_num}: Student {student_id} not found")
                    error_count += 1
                    continue
                
                # Parse data
                score = float(row['score'])
                was_present = row['was_present'].strip().upper() in ['TRUE', '1', 'YES']
                absent_reason = row.get('absent_reason', '').strip()
                remarks = row.get('remarks', '').strip()
                
                # Validate score
                if score < 0 or score > exam.max_score:
                    errors.append(f"Row {row_num}: Invalid score {score} (max: {exam.max_score})")
                    error_count += 1
                    continue
                
                # Check if result already exists
                existing = ExamResult.objects.filter(exam=exam, student=student).first()
                
                if existing:
                    if update_existing:
                        # Update existing result
                        existing.score = score
                        existing.was_present = was_present
                        existing.absent_reason = absent_reason
                        existing.remarks = remarks
                        existing.save()
                        print(f"   🔄 Updated: {student_id} - {exam_id} ({score}/{exam.max_score})")
                        success_count += 1
                    else:
                        # Skip existing
                        print(f"   ⚠️  Skipped: {student_id} - {exam_id} (already exists)")
                        skip_count += 1
                else:
                    # Create new result
                    ExamResult.objects.create(
                        exam=exam,
                        student=student,
                        score=score,
                        was_present=was_present,
                        absent_reason=absent_reason,
                        remarks=remarks
                    )
                    print(f"   ✅ Created: {student_id} - {exam_id} ({score}/{exam.max_score})")
                    success_count += 1
                
            except KeyError as e:
                errors.append(f"Row {row_num}: Missing column {e}")
                error_count += 1
            except ValueError as e:
                errors.append(f"Row {row_num}: Invalid value - {e}")
                error_count += 1
            except Exception as e:
                errors.append(f"Row {row_num}: Unexpected error - {e}")
                error_count += 1
    
    # Print summary
    print("\n" + "=" * 80)
    print("📊 IMPORT SUMMARY")
    print("=" * 80)
    print(f"✅ Successfully imported: {success_count}")
    print(f"⚠️  Skipped (already exist): {skip_count}")
    print(f"❌ Errors: {error_count}")
    
    if errors:
        print("\n❌ ERRORS:")
        for error in errors[:10]:  # Show first 10 errors
            print(f"   • {error}")
        if len(errors) > 10:
            print(f"   ... and {len(errors) - 10} more errors")


def import_scores_from_csv(csv_file, update_existing=False):
    """
    Import scores (alternative Score model) from CSV file
    
    CSV Format:
    student_id,subject_id,exam_type_id,academic_year_id,score,max_score,remarks
    STU-0001,1,1,1,85,100,Good work
    """
    from school.models import Score, Subject, ExamType, AcademicYear
    
    print("=" * 80)
    print("📥 IMPORTING SCORES")
    print("=" * 80)
    print(f"File: {csv_file}")
    
    if not os.path.exists(csv_file):
        print(f"❌ File not found: {csv_file}")
        return
    
    success_count = 0
    skip_count = 0
    error_count = 0
    errors = []
    
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        
        print("\n📊 Processing records...\n")
        
        for row_num, row in enumerate(reader, start=2):
            try:
                # Get student
                student_id = row['student_id'].strip()
                student = Student.objects.get(student_id=student_id)
                
                # Get subject
                subject_id = int(row['subject_id'])
                subject = Subject.objects.get(id=subject_id)
                
                # Get exam type
                exam_type_id = int(row['exam_type_id'])
                exam_type = ExamType.objects.get(id=exam_type_id)
                
                # Get academic year
                academic_year_id = int(row['academic_year_id'])
                academic_year = AcademicYear.objects.get(id=academic_year_id)
                
                # Parse scores
                score = float(row['score'])
                max_score = float(row['max_score'])
                remarks = row.get('remarks', '').strip()
                
                # Check if score already exists
                existing = Score.objects.filter(
                    student=student,
                    subject=subject,
                    exam_type=exam_type,
                    academic_year=academic_year
                ).first()
                
                if existing:
                    if update_existing:
                        existing.score = score
                        existing.max_score = max_score
                        existing.remarks = remarks
                        existing.save()
                        print(f"   🔄 Updated: {student_id} - {subject.name} ({score}/{max_score})")
                        success_count += 1
                    else:
                        print(f"   ⚠️  Skipped: {student_id} - {subject.name} (already exists)")
                        skip_count += 1
                else:
                    Score.objects.create(
                        student=student,
                        subject=subject,
                        exam_type=exam_type,
                        academic_year=academic_year,
                        score=score,
                        max_score=max_score,
                        remarks=remarks
                    )
                    print(f"   ✅ Created: {student_id} - {subject.name} ({score}/{max_score})")
                    success_count += 1
                
            except Exception as e:
                errors.append(f"Row {row_num}: {str(e)}")
                error_count += 1
    
    # Print summary
    print("\n" + "=" * 80)
    print("📊 IMPORT SUMMARY")
    print("=" * 80)
    print(f"✅ Successfully imported: {success_count}")
    print(f"⚠️  Skipped (already exist): {skip_count}")
    print(f"❌ Errors: {error_count}")
    
    if errors:
        print("\n❌ ERRORS:")
        for error in errors[:10]:
            print(f"   • {error}")


def create_scores_template():
    """Create sample CSV template for scores"""
    sample_file = 'scores_template.csv'
    
    with open(sample_file, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            'student_id', 'subject_id', 'exam_type_id', 'academic_year_id', 
            'score', 'max_score', 'remarks'
        ])
        writer.writerow(['STU-0001', '1', '1', '1', '85', '100', 'Good work'])
        writer.writerow(['STU-0002', '1', '1', '1', '92', '100', 'Excellent'])
        writer.writerow(['STU-0003', '1', '1', '1', '45', '100', 'Needs improvement'])
    
    print(f"✅ Created scores template: {sample_file}")


def list_exams():
    """List all available exams"""
    print("\n📝 AVAILABLE EXAMS:")
    exams = Exam.objects.all()[:20]  # Show first 20
    for exam in exams:
        print(f"   {exam.exam_id} - {exam.name} ({exam.classroom})")
    
    total = Exam.objects.count()
    if total > 20:
        print(f"   ... and {total - 20} more exams")


def list_students():
    """List all students"""
    print("\n👨‍🎓 AVAILABLE STUDENTS:")
    students = Student.objects.filter(is_active=True)[:20]
    for student in students:
        print(f"   {student.student_id} - {student} ({student.classroom})")
    
    total = Student.objects.filter(is_active=True).count()
    if total > 20:
        print(f"   ... and {total - 20} more students")


if __name__ == '__main__':
    print("\n" + "=" * 80)
    print("📥 BULK IMPORT TOOL")
    print("=" * 80)
    
    print("\nOPTIONS:")
    print("1. Create sample CSV template (ExamResult)")
    print("2. Create sample CSV template (Score)")
    print("3. Import exam results from CSV")
    print("4. Import scores from CSV")
    print("5. List available exams")
    print("6. List available students")
    print("7. Exit")
    
    choice = input("\nEnter your choice (1-7): ")
    
    if choice == '1':
        create_sample_csv()
    
    elif choice == '2':
        create_scores_template()
    
    elif choice == '3':
        list_exams()
        list_students()
        
        csv_file = input("\n📄 CSV file path: ")
        update = input("🔄 Update existing results? (yes/no, default: no): ").lower()
        update_existing = update in ['yes', 'y']
        
        import_exam_results(csv_file, update_existing)
    
    elif choice == '4':
        csv_file = input("\n📄 CSV file path: ")
        update = input("🔄 Update existing scores? (yes/no, default: no): ").lower()
        update_existing = update in ['yes', 'y']
        
        import_scores_from_csv(csv_file, update_existing)
    
    elif choice == '5':
        list_exams()
    
    elif choice == '6':
        list_students()
    
    else:
        print("👋 Goodbye!")
