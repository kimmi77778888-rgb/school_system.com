#!/usr/bin/env python
"""
Simple Student Promotion Processor
ដំណើរការឡើងថ្នាក់សិស្ស

Usage:
    python process_promotion.py --from-classroom 1 --to-classroom 2
    python process_promotion.py --from-grade 2 --to-grade 3 --year 2026
"""

import os
import sys
import django
from datetime import datetime

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crm.settings')
django.setup()

from school.models import Student, Classroom, AcademicYear, StudentHistory
from django.db.models import Avg, Count


class PromotionProcessor:
    """Process student promotions with validation"""
    
    def __init__(self, passing_score=50, min_attendance=80):
        self.passing_score = passing_score
        self.min_attendance = min_attendance
        self.results = {
            'total': 0,
            'eligible': 0,
            'promoted': 0,
            'failed': [],
            'details': []
        }
    
    def check_eligibility(self, student, academic_year=None):
        """Check if student meets promotion criteria"""
        # Get scores
        if academic_year:
            scores = student.scores.filter(academic_year=academic_year)
        else:
            scores = student.scores.all()
        
        if not scores.exists():
            return False, "No scores available"
        
        # Calculate average
        total_subjects = scores.count()
        avg_percentage = sum(score.percentage() for score in scores) / total_subjects
        
        # Check score requirement
        if avg_percentage < self.passing_score:
            return False, f"Average {avg_percentage:.1f}% < {self.passing_score}%"
        
        # Check attendance
        if academic_year:
            year_attendance = student.attendances.filter(
                date__year__in=[int(y) for y in academic_year.year.split('-')]
            )
        else:
            year_attendance = student.attendances.all()
        
        total_days = year_attendance.count()
        present_days = year_attendance.filter(status='P').count()
        attendance_rate = (present_days / total_days * 100) if total_days > 0 else 0
        
        if attendance_rate < self.min_attendance:
            return False, f"Attendance {attendance_rate:.1f}% < {self.min_attendance}%"
        
        return True, f"Average: {avg_percentage:.1f}%, Attendance: {attendance_rate:.1f}%"
    
    def validate_progression(self, from_classroom, to_classroom):
        """Validate grade progression rules"""
        from_grade = from_classroom.grade
        to_grade = to_classroom.grade
        
        if not from_grade or not to_grade:
            return False, "Missing grade information"
        
        from_num = from_grade.grade_number
        to_num = to_grade.grade_number
        
        # Must be sequential
        if to_num != from_num + 1:
            return False, f"Cannot skip grades: Grade {from_num} → Grade {to_num}"
        
        # Check level transitions
        if from_num == 6 and to_num == 7:
            if to_grade.level != 'lower_secondary':
                return False, "Grade 6→7 must transition to Lower Secondary"
        
        elif from_num == 9 and to_num == 10:
            if to_grade.level != 'upper_secondary':
                return False, "Grade 9→10 must transition to Upper Secondary"
        
        elif from_num == 12:
            return False, "Grade 12 students cannot be promoted (graduation)"
        
        return True, "Valid progression"
    
    def create_history_record(self, student, old_classroom, new_classroom, academic_year):
        """Create student history record"""
        try:
            # Get academic data
            scores = student.scores.filter(academic_year=academic_year)
            total_subjects = scores.count()
            
            if total_subjects > 0:
                avg_score = sum(s.score for s in scores) / total_subjects
                passed = sum(1 for s in scores if s.is_passing(self.passing_score))
                failed = total_subjects - passed
            else:
                avg_score = 0
                passed = 0
                failed = 0
            
            # Get attendance data
            year_attendance = student.attendances.filter(
                date__year__in=[int(y) for y in academic_year.year.split('-')]
            )
            total_days = year_attendance.count()
            present_days = year_attendance.filter(status='P').count()
            absent_days = year_attendance.filter(status='A').count()
            
            # Create history
            history, created = StudentHistory.objects.update_or_create(
                student=student,
                academic_year=academic_year,
                defaults={
                    'classroom': old_classroom,
                    'grade_name': str(old_classroom.grade),
                    'grade_number': old_classroom.grade.grade_number,
                    'grade_level': old_classroom.grade.level,
                    'status': 'PROMOTED',
                    'average_score': avg_score,
                    'total_subjects': total_subjects,
                    'passed_subjects': passed,
                    'failed_subjects': failed,
                    'total_days': total_days,
                    'present_days': present_days,
                    'absent_days': absent_days,
                    'end_date': datetime.now().date(),
                    'promoted_to': str(new_classroom),
                    'promotion_note': f"Promoted to {new_classroom} on {datetime.now().strftime('%Y-%m-%d')}"
                }
            )
            return True
        except Exception as e:
            print(f"Error creating history: {e}")
            return False
    
    def promote_student(self, student, from_classroom, to_classroom, academic_year):
        """Promote a single student"""
        try:
            # Validate progression
            valid, msg = self.validate_progression(from_classroom, to_classroom)
            if not valid:
                return False, msg
            
            # Check eligibility
            eligible, reason = self.check_eligibility(student, academic_year)
            if not eligible:
                return False, f"Not eligible: {reason}"
            
            # Create history record
            if academic_year:
                self.create_history_record(student, from_classroom, to_classroom, academic_year)
            
            # Update student
            student.previous_classroom = str(from_classroom)
            student.promotion_date = datetime.now().date()
            student.classroom = to_classroom
            student.status = 'ACTIVE'
            
            # Add note
            note = f"Promoted from {from_classroom} to {to_classroom} on {datetime.now().strftime('%Y-%m-%d')}"
            if student.notes:
                student.notes += f"\n{note}"
            else:
                student.notes = note
            
            student.save()
            return True, "Successfully promoted"
            
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def process_classroom(self, from_classroom_id, to_classroom_id, dry_run=False):
        """Process all eligible students in a classroom"""
        try:
            from_classroom = Classroom.objects.get(pk=from_classroom_id)
            to_classroom = Classroom.objects.get(pk=to_classroom_id)
            academic_year = from_classroom.academic_year
            
            print(f"\n{'='*70}")
            print(f"PROMOTION PROCESS")
            print(f"{'='*70}")
            print(f"From: {from_classroom}")
            print(f"To:   {to_classroom}")
            print(f"Year: {academic_year}")
            print(f"Mode: {'DRY RUN (no changes)' if dry_run else 'LIVE (will make changes)'}")
            print(f"{'='*70}\n")
            
            # Validate progression first
            valid, msg = self.validate_progression(from_classroom, to_classroom)
            if not valid:
                print(f"❌ INVALID PROGRESSION: {msg}\n")
                return self.results
            
            # Get students
            students = Student.objects.filter(
                classroom=from_classroom,
                is_active=True
            ).order_by('student_id')
            
            self.results['total'] = students.count()
            
            print(f"Found {self.results['total']} active students\n")
            print(f"{'No':<4} {'ID':<12} {'Name':<25} {'Avg%':<8} {'Att%':<8} {'Status'}")
            print(f"{'-'*70}")
            
            for idx, student in enumerate(students, 1):
                eligible, reason = self.check_eligibility(student, academic_year)
                
                # Get student data for display
                scores = student.scores.filter(academic_year=academic_year) if academic_year else student.scores.all()
                if scores.exists():
                    avg = sum(s.percentage() for s in scores) / scores.count()
                    
                    year_att = student.attendances.filter(
                        date__year__in=[int(y) for y in academic_year.year.split('-')]
                    ) if academic_year else student.attendances.all()
                    
                    total_days = year_att.count()
                    present = year_att.filter(status='P').count()
                    att_rate = (present / total_days * 100) if total_days > 0 else 0
                else:
                    avg = 0
                    att_rate = 0
                
                status = "✅ ELIGIBLE" if eligible else f"❌ {reason}"
                
                print(f"{idx:<4} {student.student_id:<12} {student.full_name()[:24]:<25} "
                      f"{avg:>6.1f}% {att_rate:>6.1f}% {status}")
                
                if eligible:
                    self.results['eligible'] += 1
                    
                    if not dry_run:
                        success, msg = self.promote_student(student, from_classroom, to_classroom, academic_year)
                        if success:
                            self.results['promoted'] += 1
                            self.results['details'].append(f"✅ {student.student_id} - {student.full_name()}")
                        else:
                            self.results['failed'].append(f"❌ {student.student_id} - {msg}")
                else:
                    self.results['failed'].append(f"❌ {student.student_id} - {reason}")
            
            # Print summary
            print(f"\n{'='*70}")
            print(f"SUMMARY")
            print(f"{'='*70}")
            print(f"Total students:     {self.results['total']}")
            print(f"Eligible:           {self.results['eligible']}")
            if not dry_run:
                print(f"Successfully promoted: {self.results['promoted']}")
                print(f"Failed:             {len(self.results['failed'])}")
            print(f"{'='*70}\n")
            
            if not dry_run and self.results['failed']:
                print("\nFailed promotions:")
                for fail in self.results['failed']:
                    print(f"  {fail}")
            
            return self.results
            
        except Classroom.DoesNotExist:
            print(f"❌ Error: Classroom not found")
            return self.results
        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()
            return self.results


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Process student promotions')
    parser.add_argument('--from-classroom', type=int, required=True, help='Source classroom ID')
    parser.add_argument('--to-classroom', type=int, required=True, help='Target classroom ID')
    parser.add_argument('--passing-score', type=float, default=50, help='Minimum passing score (default: 50)')
    parser.add_argument('--min-attendance', type=float, default=80, help='Minimum attendance rate (default: 80)')
    parser.add_argument('--dry-run', action='store_true', help='Preview only, do not make changes')
    
    args = parser.parse_args()
    
    # Create processor
    processor = PromotionProcessor(
        passing_score=args.passing_score,
        min_attendance=args.min_attendance
    )
    
    # Process
    results = processor.process_classroom(
        from_classroom_id=args.from_classroom,
        to_classroom_id=args.to_classroom,
        dry_run=args.dry_run
    )
    
    # Exit code
    if results['promoted'] > 0 or args.dry_run:
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == '__main__':
    main()
