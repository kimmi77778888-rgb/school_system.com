"""
Management command to create all grades (1-12) if they don't exist
"""
from django.core.management.base import BaseCommand
from school.models import Grade

class Command(BaseCommand):
    help = 'Create all grades from 1 to 12 if they don\'t exist'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('\n🎓 Creating grades 1-12...\n'))
        
        # Grade definitions following Cambodia education system
        grades_data = [
            # Primary (បឋមសិក្សា) - Grades 1-6
            {'number': 1, 'name': 'ទី១', 'level': 'primary'},
            {'number': 2, 'name': 'ទី២', 'level': 'primary'},
            {'number': 3, 'name': 'ទី៣', 'level': 'primary'},
            {'number': 4, 'name': 'ទី៤', 'level': 'primary'},
            {'number': 5, 'name': 'ទី៥', 'level': 'primary'},
            {'number': 6, 'name': 'ទី៦', 'level': 'primary'},
            
            # Lower Secondary (បឋមភូមិ) - Grades 7-9
            {'number': 7, 'name': 'ទី៧', 'level': 'lower_secondary'},
            {'number': 8, 'name': 'ទី៨', 'level': 'lower_secondary'},
            {'number': 9, 'name': 'ទី៩', 'level': 'lower_secondary'},
            
            # Upper Secondary (មធ្យមភូមិ) - Grades 10-12
            {'number': 10, 'name': 'ទី១០', 'level': 'upper_secondary'},
            {'number': 11, 'name': 'ទី១១', 'level': 'upper_secondary'},
            {'number': 12, 'name': 'ទី១២', 'level': 'upper_secondary'},
        ]
        
        created_count = 0
        skipped_count = 0
        
        for grade_data in grades_data:
            grade, created = Grade.objects.get_or_create(
                grade_number=grade_data['number'],
                defaults={
                    'name': grade_data['name'],
                    'level': grade_data['level']
                }
            )
            
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'  ✅ Created: Grade {grade_data["number"]} ({grade_data["name"]}) - {grade_data["level"]}')
                )
                created_count += 1
            else:
                self.stdout.write(
                    self.style.WARNING(f'  ⏭️  Skipped: Grade {grade_data["number"]} ({grade_data["name"]}) - already exists')
                )
                skipped_count += 1
        
        self.stdout.write('\n' + '─' * 70)
        self.stdout.write(self.style.SUCCESS(f'\n✅ Summary:'))
        self.stdout.write(f'  • Created: {created_count} grades')
        self.stdout.write(f'  • Skipped: {skipped_count} grades (already exist)')
        self.stdout.write(f'  • Total: {Grade.objects.count()} grades in system\n')
        
        if created_count > 0:
            self.stdout.write(self.style.SUCCESS('\n🎉 Done! Grades 1-12 are now ready!'))
            self.stdout.write('\n💡 Next step: Create classrooms for these grades')
            self.stdout.write('   Run: python manage.py create_missing_classrooms --year "2026-2027"\n')
        else:
            self.stdout.write(self.style.SUCCESS('\n✅ All grades already exist!'))
