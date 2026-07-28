"""
Management command to ensure all users have profiles
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from school.models import UserProfile


class Command(BaseCommand):
    help = 'Ensure all users have UserProfile records'

    def handle(self, *args, **options):
        self.stdout.write('Checking users and their profiles...\n')
        self.stdout.write('=' * 60)
        
        users_without_profile = []
        users_with_profile = []
        
        for user in User.objects.all():
            try:
                profile = user.profile
                users_with_profile.append((user.username, profile.role))
                self.stdout.write(
                    self.style.SUCCESS(f'✓ {user.username:20s} | Role: {profile.role}')
                )
            except UserProfile.DoesNotExist:
                users_without_profile.append(user)
                self.stdout.write(
                    self.style.ERROR(f'✗ {user.username:20s} | NO PROFILE!')
                )
        
        self.stdout.write('\n' + '=' * 60)
        self.stdout.write(f'Total users: {User.objects.count()}')
        self.stdout.write(f'Users with profile: {len(users_with_profile)}')
        self.stdout.write(f'Users without profile: {len(users_without_profile)}')
        
        if users_without_profile:
            self.stdout.write('\n' + '=' * 60)
            self.stdout.write('CREATING MISSING PROFILES...')
            self.stdout.write('=' * 60)
            
            for user in users_without_profile:
                # Create profile with admin role if user is staff/superuser, otherwise student
                role = 'admin' if (user.is_staff or user.is_superuser) else 'student'
                profile, created = UserProfile.objects.get_or_create(
                    user=user,
                    defaults={'role': role}
                )
                if created:
                    self.stdout.write(
                        self.style.SUCCESS(f'✓ Created profile for {user.username} with role: {role}')
                    )
            
            self.stdout.write(
                self.style.SUCCESS('\n✅ All missing profiles have been created!')
            )
        else:
            self.stdout.write(
                self.style.SUCCESS('\n✅ All users have profiles!')
            )
