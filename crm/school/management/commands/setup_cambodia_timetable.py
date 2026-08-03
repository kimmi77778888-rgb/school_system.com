"""
Management command to setup Cambodia standard timetable structure
Run: python manage.py setup_cambodia_timetable
"""
from django.core.management.base import BaseCommand
from school.models import TimeSlot
from datetime import time


class Command(BaseCommand):
    help = 'Setup Cambodia standard timetable time slots'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('Setting up Cambodia standard timetable...'))
        
        # Clear existing time slots
        deleted_count = TimeSlot.objects.all().count()
        TimeSlot.objects.all().delete()
        self.stdout.write(self.style.WARNING(f'Deleted {deleted_count} existing time slots'))
        
        # Cambodia standard periods
        # Format: (day, period, start_time, end_time)
        # Days: 1=Mon, 2=Tue, 3=Wed, 4=Thu, 5=Fri, 6=Sat
        cambodia_periods = [
            # Monday (ច័ន្ទ)
            (1, 1, time(7, 0), time(7, 50)),
            (1, 2, time(7, 50), time(8, 40)),
            (1, 3, time(8, 55), time(9, 45)),
            (1, 4, time(9, 45), time(10, 35)),
            (1, 5, time(10, 35), time(11, 25)),
            (1, 6, time(13, 30), time(14, 20)),
            (1, 7, time(14, 20), time(15, 10)),
            (1, 8, time(15, 25), time(16, 15)),
            (1, 9, time(16, 15), time(17, 5)),
            
            # Tuesday (អង្គារ)
            (2, 1, time(7, 0), time(7, 50)),
            (2, 2, time(7, 50), time(8, 40)),
            (2, 3, time(8, 55), time(9, 45)),
            (2, 4, time(9, 45), time(10, 35)),
            (2, 5, time(10, 35), time(11, 25)),
            (2, 6, time(13, 30), time(14, 20)),
            (2, 7, time(14, 20), time(15, 10)),
            (2, 8, time(15, 25), time(16, 15)),
            (2, 9, time(16, 15), time(17, 5)),
            
            # Wednesday (ពុធ)
            (3, 1, time(7, 0), time(7, 50)),
            (3, 2, time(7, 50), time(8, 40)),
            (3, 3, time(8, 55), time(9, 45)),
            (3, 4, time(9, 45), time(10, 35)),
            (3, 5, time(10, 35), time(11, 25)),
            (3, 6, time(13, 30), time(14, 20)),
            (3, 7, time(14, 20), time(15, 10)),
            (3, 8, time(15, 25), time(16, 15)),
            (3, 9, time(16, 15), time(17, 5)),
            
            # Thursday (ព្រហស្បតិ៍)
            (4, 1, time(7, 0), time(7, 50)),
            (4, 2, time(7, 50), time(8, 40)),
            (4, 3, time(8, 55), time(9, 45)),
            (4, 4, time(9, 45), time(10, 35)),
            (4, 5, time(10, 35), time(11, 25)),
            (4, 6, time(13, 30), time(14, 20)),
            (4, 7, time(14, 20), time(15, 10)),
            (4, 8, time(15, 25), time(16, 15)),
            (4, 9, time(16, 15), time(17, 5)),
            
            # Friday (សុក្រ)
            (5, 1, time(7, 0), time(7, 50)),
            (5, 2, time(7, 50), time(8, 40)),
            (5, 3, time(8, 55), time(9, 45)),
            (5, 4, time(9, 45), time(10, 35)),
            (5, 5, time(10, 35), time(11, 25)),
            (5, 6, time(13, 30), time(14, 20)),
            (5, 7, time(14, 20), time(15, 10)),
            (5, 8, time(15, 25), time(16, 15)),
            (5, 9, time(16, 15), time(17, 5)),
            
            # Saturday (សៅរ៍)
            (6, 1, time(7, 0), time(7, 50)),
            (6, 2, time(7, 50), time(8, 40)),
            (6, 3, time(8, 55), time(9, 45)),
            (6, 4, time(9, 45), time(10, 35)),
            (6, 5, time(10, 35), time(11, 25)),
            (6, 6, time(13, 30), time(14, 20)),
            (6, 7, time(14, 20), time(15, 10)),
            (6, 8, time(15, 25), time(16, 15)),
            (6, 9, time(16, 15), time(17, 5)),
        ]
        
        created_count = 0
        for day, period, start_time, end_time in cambodia_periods:
            TimeSlot.objects.create(
                day=day,
                period=period,
                start_time=start_time,
                end_time=end_time
            )
            created_count += 1
        
        self.stdout.write(self.style.SUCCESS(f'✓ Created {created_count} time slots'))
        self.stdout.write(self.style.SUCCESS(''))
        self.stdout.write(self.style.SUCCESS('Cambodia Timetable Structure:'))
        self.stdout.write(self.style.SUCCESS('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━'))
        self.stdout.write(self.style.SUCCESS('🌅 វេនព្រឹក (Morning):'))
        self.stdout.write(self.style.SUCCESS('   Period 1: 07:00 - 07:50'))
        self.stdout.write(self.style.SUCCESS('   Period 2: 07:50 - 08:40'))
        self.stdout.write(self.style.WARNING('   សម្រាក: 08:40 - 08:55'))
        self.stdout.write(self.style.SUCCESS('   Period 3: 08:55 - 09:45'))
        self.stdout.write(self.style.SUCCESS('   Period 4: 09:45 - 10:35'))
        self.stdout.write(self.style.SUCCESS('   Period 5: 10:35 - 11:25'))
        self.stdout.write(self.style.SUCCESS(''))
        self.stdout.write(self.style.SUCCESS('🌞 វេនល្ងាច (Afternoon):'))
        self.stdout.write(self.style.SUCCESS('   Period 6: 13:30 - 14:20'))
        self.stdout.write(self.style.SUCCESS('   Period 7: 14:20 - 15:10'))
        self.stdout.write(self.style.WARNING('   សម្រាក: 15:10 - 15:25'))
        self.stdout.write(self.style.SUCCESS('   Period 8: 15:25 - 16:15'))
        self.stdout.write(self.style.SUCCESS('   Period 9: 16:15 - 17:05'))
        self.stdout.write(self.style.SUCCESS(''))
        self.stdout.write(self.style.SUCCESS('📅 School Days: Monday - Saturday (6 days)'))
        self.stdout.write(self.style.SUCCESS('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━'))
        self.stdout.write(self.style.SUCCESS(''))
        self.stdout.write(self.style.SUCCESS('✓ Setup complete! You can now create timetables.'))
