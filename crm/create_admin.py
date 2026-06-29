"""
One-time script to create a superuser on Render.
This file will be deleted after use.
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crm.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

username = 'admin'
password = 'Admin@12345'
email = 'admin@school.com'

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print(f'Superuser "{username}" created successfully!')
else:
    print(f'User "{username}" already exists.')
