"""
Check if all users have profiles and create missing ones
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crm.settings')
django.setup()

from django.contrib.auth.models import User
from school.models import UserProfile

print("Checking users and their profiles...\n")
print("=" * 60)

users_without_profile = []
users_with_profile = []

for user in User.objects.all():
    try:
        profile = user.profile
        users_with_profile.append((user.username, profile.role))
        print(f"✓ {user.username:20s} | Role: {profile.role}")
    except UserProfile.DoesNotExist:
        users_without_profile.append(user)
        print(f"✗ {user.username:20s} | NO PROFILE!")

print("\n" + "=" * 60)
print(f"Total users: {User.objects.count()}")
print(f"Users with profile: {len(users_with_profile)}")
print(f"Users without profile: {len(users_without_profile)}")

if users_without_profile:
    print("\n" + "=" * 60)
    print("CREATING MISSING PROFILES...")
    print("=" * 60)
    
    for user in users_without_profile:
        # Create profile with admin role if user is staff/superuser, otherwise student
        role = 'admin' if (user.is_staff or user.is_superuser) else 'student'
        profile = UserProfile.objects.create(
            user=user,
            role=role
        )
        print(f"✓ Created profile for {user.username} with role: {role}")
    
    print("\n✅ All missing profiles have been created!")
else:
    print("\n✅ All users have profiles!")
