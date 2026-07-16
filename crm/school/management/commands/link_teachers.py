from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from school.models import Teacher, UserProfile


class Command(BaseCommand):
    help = 'Create user accounts for existing teachers who don\'t have one'

    def add_arguments(self, parser):
        parser.add_argument(
            '--password',
            type=str,
            default='teacher123',
            help='Default password for teacher accounts (default: teacher123)'
        )

    def handle(self, *args, **options):
        default_password = options['password']
        teachers = Teacher.objects.all()
        created_count = 0
        existing_count = 0

        self.stdout.write(self.style.SUCCESS('=== Linking Teachers to User Accounts ===\n'))

        for teacher in teachers:
            # Check if teacher already has a user account
            existing_profile = UserProfile.objects.filter(teacher=teacher).first()

            if existing_profile:
                self.stdout.write(
                    self.style.WARNING(
                        f'✓ {teacher.first_name} {teacher.last_name} already has account: {existing_profile.user.username}'
                    )
                )
                existing_count += 1
                continue

            # Generate username
            first = teacher.first_name_en or teacher.first_name
            last = teacher.last_name_en or teacher.last_name
            username = f"{first}{last}".replace(' ', '').lower()

            # Make username unique
            base_username = username
            counter = 1
            while User.objects.filter(username=username).exists():
                username = f"{base_username}{counter}"
                counter += 1

            # Create user
            user = User.objects.create_user(
                username=username,
                password=default_password,
                first_name=teacher.first_name,
                last_name=teacher.last_name,
                email=teacher.email or ''
            )

            # Link user profile to teacher
            UserProfile.objects.update_or_create(
                user=user,
                defaults={'role': 'teacher', 'teacher': teacher, 'phone': teacher.phone}
            )

            self.stdout.write(
                self.style.SUCCESS(f'✓ Created account for {teacher.first_name} {teacher.last_name}')
            )
            self.stdout.write(f'  Username: {username}')
            self.stdout.write(f'  Password: {default_password}\n')
            created_count += 1

        # Summary
        self.stdout.write('\n' + '='*50)
        self.stdout.write(self.style.SUCCESS(f'\n✓ Created: {created_count} new accounts'))
        self.stdout.write(self.style.WARNING(f'✓ Existing: {existing_count} accounts'))
        
        if created_count > 0:
            self.stdout.write('\n' + self.style.WARNING(
                'Teachers should change their password after first login!'
            ))
