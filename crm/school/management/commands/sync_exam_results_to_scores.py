"""
Management command to sync ExamResults to Scores for promotion calculations
This connects the Exam system with Student Promotion
"""
from django.core.management.base import BaseCommand
from school.models import ExamResult, Score, Student
from django.db import transaction

class Command(BaseCommand):
    help = 'Sync Exam Results to Scores table for promotion calculations'

    def add_arguments(self, parser):
        parser.add_argument(
            '--academic-year',
            type=str,
            help='Academic year to sync (e.g., "2026-2027"). If not provided, syncs all.',
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be synced without actually syncing',
        )

    def handle(self, *args, **options):
        academic_year = options.get('academic_year')
        dry_run = options.get('dry_run', False)
        
        self.stdout.write(self.style.SUCCESS('\n🔄 Syncing Exam Results to Scores...\n'))
        
        if dry_run:
            self.stdout.write(self.style.WARNING('📝 DRY RUN MODE - No changes will be made\n'))
        
        # Get exam results to sync
        exam_results = ExamResult.objects.select_related(
            'exam', 'student', 'exam__subject', 'exam__exam_type', 'exam__academic_year'
        ).filter(was_present=True)  # Only sync results where student was present
        
        if academic_year:
            from school.models import AcademicYear
            try:
                year_obj = AcademicYear.objects.get(year=academic_year)
                exam_results = exam_results.filter(exam__academic_year=year_obj)
                self.stdout.write(f'📅 Filtering by academic year: {academic_year}\n')
            except AcademicYear.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'❌ Academic year "{academic_year}" not found!'))
                return
        
        total = exam_results.count()
        self.stdout.write(f'📊 Found {total} exam results to process\n')
        
        if total == 0:
            self.stdout.write(self.style.WARNING('⚠️  No exam results found!'))
            return
        
        created_count = 0
        updated_count = 0
        skipped_count = 0
        error_count = 0
        
        self.stdout.write('\n' + '─' * 70 + '\n')
        
        for result in exam_results:
            try:
                exam = result.exam
                student = result.student
                
                # Check if score already exists
                score, created = Score.objects.get_or_create(
                    student=student,
                    subject=exam.subject,
                    exam_type=exam.exam_type,
                    exam=exam,
                    academic_year=exam.academic_year,
                    defaults={
                        'score': result.score,
                        'max_score': exam.max_score,
                        'remarks': result.remarks or ''
                    }
                )
                
                if created:
                    if not dry_run:
                        created_count += 1
                        self.stdout.write(
                            self.style.SUCCESS(
                                f'  ✅ Created: {student} | {exam.subject} | {exam.exam_type} | {result.score}/{exam.max_score}'
                            )
                        )
                    else:
                        self.stdout.write(
                            f'  [DRY RUN] Would create: {student} | {exam.subject} | {exam.exam_type} | {result.score}/{exam.max_score}'
                        )
                else:
                    # Update if score changed
                    if score.score != result.score or score.max_score != exam.max_score:
                        if not dry_run:
                            score.score = result.score
                            score.max_score = exam.max_score
                            score.remarks = result.remarks or ''
                            score.save()
                            updated_count += 1
                            self.stdout.write(
                                self.style.WARNING(
                                    f'  🔄 Updated: {student} | {exam.subject} | {exam.exam_type} | {result.score}/{exam.max_score}'
                                )
                            )
                        else:
                            self.stdout.write(
                                f'  [DRY RUN] Would update: {student} | {exam.subject} | {exam.exam_type} | {result.score}/{exam.max_score}'
                            )
                    else:
                        skipped_count += 1
                        if skipped_count <= 5:  # Show first 5 skipped
                            self.stdout.write(
                                f'  ⏭️  Skipped (unchanged): {student} | {exam.subject}'
                            )
            
            except Exception as e:
                error_count += 1
                self.stdout.write(
                    self.style.ERROR(f'  ❌ Error: {result.student} - {str(e)}')
                )
        
        if skipped_count > 5:
            self.stdout.write(f'  ... and {skipped_count - 5} more skipped')
        
        # Summary
        self.stdout.write('\n' + '─' * 70)
        self.stdout.write(self.style.SUCCESS(f'\n📊 Summary:'))
        self.stdout.write(f'  • Processed: {total} exam results')
        self.stdout.write(f'  • Created: {created_count} new scores')
        self.stdout.write(f'  • Updated: {updated_count} existing scores')
        self.stdout.write(f'  • Skipped: {skipped_count} (no changes)')
        if error_count > 0:
            self.stdout.write(self.style.ERROR(f'  • Errors: {error_count}'))
        
        if not dry_run:
            self.stdout.write(self.style.SUCCESS(f'\n✅ Sync completed!'))
            self.stdout.write('\n💡 Scores are now ready for student promotion calculations')
        else:
            self.stdout.write(self.style.WARNING('\n📝 DRY RUN completed - no changes made'))
            self.stdout.write('   Run without --dry-run to actually sync')
