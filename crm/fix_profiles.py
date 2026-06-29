"""
Ensure every User has a UserProfile.
Safe to run multiple times — only creates missing profiles.
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crm.settings')
django.setup()

from django.contrib.auth.models import User
from school.models import UserProfile

print("Checking UserProfiles...")
fixed = 0
for user in User.objects.all():
    try:
        _ = user.profile
    except Exception:
        role = 'admin' if user.is_superuser else 'student'
        UserProfile.objects.create(user=user, role=role)
        print(f"  Created profile for '{user.username}' (role={role})")
        fixed += 1

if fixed == 0:
    print("  All users have profiles. Nothing to fix.")
else:
    print(f"  Fixed {fixed} missing profiles.")
