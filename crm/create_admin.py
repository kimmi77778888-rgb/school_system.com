import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crm.settings')
django.setup()

from django.contrib.auth import get_user_model
from school.models import UserProfile

User = get_user_model()

username = 'admin'
password = 'Admin@12345'
email = 'admin@school.com'

if not User.objects.filter(username=username).exists():
    user = User.objects.create_superuser(username=username, email=email, password=password)
    print(f'Superuser "{username}" created successfully!')
else:
    user = User.objects.get(username=username)
    print(f'User "{username}" already exists.')

# Always ensure admin has a profile with role=admin
profile, created = UserProfile.objects.get_or_create(user=user, defaults={'role': 'admin'})
if not created and profile.role != 'admin':
    profile.role = 'admin'
    profile.save()
    print(f'Updated profile role to admin.')
print(f'Profile OK: role={profile.role}')
