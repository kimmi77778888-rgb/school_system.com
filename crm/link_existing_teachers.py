#!/usr/bin/env python
"""
Script to create user accounts for existing teachers who don't have one.
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crm.settings')
django.setup()

from django.contrib.auth.models import User
from school.models import Teacher, UserProfile

def link_teachers():
    teachers = Teacher.objects.all()
    
    for teacher in teachers:
        # Check if teacher already has a user account
        existing_profile = UserProfile.objects.filter(teacher=teacher).first()
        
        if existing_profile:
            print(f'✓ {teacher.first_name} {teacher.last_name} already has account: {existing_profile.user.username}')
            continue
        
        # Generate username
        username = f"{teacher.first_name_en or teacher.first_name}{teacher.last_name_en or teacher.last_name}".replace(' ', '').lower()
        
        # Make username unique
        base_username = username
        counter = 1
        while User.objects.filter(username=username).exists():
            username = f"{base_username}{counter}"
            counter += 1
        
        # Create user
        password = 'teacher123'  # Default password
        user = User.objects.create_user(
            username=username,
            password=password,
            first_name=teacher.first_name,
            last_name=teacher.last_name,
            email=teacher.email or ''
        )
        
        # Link user profile to teacher
        profile = UserProfile.objects.update_or_create(
            user=user,
            defaults={'role': 'teacher', 'teacher': teacher, 'phone': teacher.phone}
        )[0]
        
        print(f'✓ Created account for {teacher.first_name} {teacher.last_name}')
        print(f'  Username: {username}')
        print(f'  Password: {password}')
        print(f'  Profile: {profile}')
        print()

if __name__ == '__main__':
    print('=== Linking Existing Teachers to User Accounts ===\n')
    link_teachers()
    print('\n=== Done! ===')
    print('\nAll teachers can now log in with:')
    print('  Default password: teacher123')
    print('  (They should change it after first login)')
