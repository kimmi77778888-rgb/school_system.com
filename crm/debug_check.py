import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crm.settings')
import django
django.setup()

from django.contrib.auth.models import User
from school.models import UserProfile

print("=== Checking all users and profiles ===")
users = User.objects.select_related('profile').order_by('username')
for u in users:
    print(f"\nUser: {u.username} (superuser={u.is_superuser})")
    try:
        p = u.profile
        print(f"  Profile: role={p.role}, photo='{p.photo}'")
        if p.photo and p.photo.name:
            try:
                url = p.photo.url
                print(f"  Photo URL: {url}")
            except Exception as e:
                print(f"  Photo URL ERROR: {type(e).__name__}: {e}")
    except Exception as e:
        print(f"  NO PROFILE: {type(e).__name__}: {e}")

print("\n=== Checking SchoolSettings ===")
from school.models import SchoolSettings
s = SchoolSettings.get()
print(f"  school_name={s.school_name}")
print(f"  logo='{s.logo}'")
if s.logo and s.logo.name:
    try:
        print(f"  logo URL: {s.logo.url}")
    except Exception as e:
        print(f"  logo URL ERROR: {type(e).__name__}: {e}")

print(f"  favicon='{s.favicon}'")
if s.favicon and s.favicon.name:
    try:
        print(f"  favicon URL: {s.favicon.url}")
    except Exception as e:
        print(f"  favicon URL ERROR: {type(e).__name__}: {e}")

print("\n=== Done ===")
