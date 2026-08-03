#!/usr/bin/env python
"""
Management command to create missing classrooms for grades that don't have any.
This is needed for student promotion to work properly.
"""
from django.core.management.base import BaseCommand
from school.models import Grade, AcademicYear, Classroom


class Command(BaseCommand):
    help = 'Create missing classrooms for grades that have no classrooms yet'

    def add_arguments(self, parser):
        parser.add_argument(
            '--year',
            type=str,
            help='Academic year name (e.g., "2026"). If not provided, uses the most recent year.',
        )

    def handle(self, *args, **options):
        # Get or determine academic year
        year_name = options.get('year')
        if year_name:
            try:
                academic_year = AcademicYear.objects.get(year=year_name)
            except AcademicYear.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'Academic year "{year_name}" not found!'))
                return
        else:
            # Get most recent academic year
            academic_year = AcademicYear.objects.order_by('-year').first()
            if not academic_year:
                self.stdout.write(self.style.ERROR('No academic years found! Please create one first.'))
                return

        self.stdout.write(f'\n{"="*60}')
        self.stdout.write(f'Creating missing classrooms for Academic Year: {academic_year}')
        self.stdout.write(f'{"="*60}\n')

        # Get all grades
        grades = Grade.objects.all().order_by('grade_number')
        
        created_count = 0
        skipped_count = 0
        
        for grade in grades:
            # Check if this grade already has classrooms for this academic year
            existing_classrooms = Classroom.objects.filter(
                grade=grade,
                academic_year=academic_year
            )
            
            if existing_classrooms.exists():
                self.stdout.write(
                    f'  ⊘ Skipped Grade {grade.name} (#{grade.grade_number}) - '
                    f'Already has {existing_classrooms.count()} classroom(s)'
                )
                skipped_count += 1
            else:
                # Create a classroom for this grade
                classroom = Classroom.objects.create(
                    grade=grade,
                    academic_year=academic_year,
                    room_number=f'{grade.name}'  # Simple naming, can be changed later
                )
                self.stdout.write(
                    self.style.SUCCESS(
                        f'  ✓ Created classroom: {classroom} '
                        f'(Grade #{grade.grade_number})'
                    )
                )
                created_count += 1
        
        # Summary
        self.stdout.write(f'\n{"="*60}')
        self.stdout.write(self.style.SUCCESS(f'✓ Created {created_count} new classrooms'))
        self.stdout.write(f'⊘ Skipped {skipped_count} grades (already have classrooms)')
        self.stdout.write(f'{"="*60}\n')
        
        # Show next promotion paths
        self.stdout.write('\n=== Promotion Paths Available ===')
        for grade in grades:
            if grade.grade_number:
                current_classrooms = Classroom.objects.filter(
                    grade=grade,
                    academic_year=academic_year
                )
                next_classrooms = Classroom.objects.filter(
                    grade__grade_number=grade.grade_number + 1,
                    academic_year=academic_year
                )
                
                if current_classrooms.exists():
                    next_info = f'{next_classrooms.count()} next classroom(s)' if next_classrooms.exists() else '⚠️  NO NEXT CLASSROOM'
                    self.stdout.write(
                        f'Grade {grade.name} (#{grade.grade_number}): '
                        f'{current_classrooms.count()} current → {next_info}'
                    )
        
        self.stdout.write('\n')
