"""
Clear broken local image paths from the production database.
Run this once on Render to fix 500 errors caused by missing local images.
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crm.settings')
django.setup()

# Only run on production (Render)
if not os.environ.get('DATABASE_URL'):
    print("Local environment — skipping fix_images.py")
    exit(0)

from school.models import Student, Teacher, UserProfile, SchoolSettings

# Clear student photos
count = Student.objects.exclude(photo='').exclude(photo=None).count()
Student.objects.exclude(photo='').exclude(photo=None).update(photo='')
print(f"Cleared {count} student photos")

# Clear teacher photos
count = Teacher.objects.exclude(photo='').exclude(photo=None).count()
Teacher.objects.exclude(photo='').exclude(photo=None).update(photo='')
print(f"Cleared {count} teacher photos")

# Clear user profile photos
count = UserProfile.objects.exclude(photo='').exclude(photo=None).count()
UserProfile.objects.exclude(photo='').exclude(photo=None).update(photo='')
print(f"Cleared {count} user profile photos")

# Clear school logo and favicon
settings = SchoolSettings.objects.filter(pk=1).first()
if settings:
    settings.logo = ''
    settings.favicon = ''
    settings.save()
    print("Cleared school logo and favicon")

print("Done! All broken image paths cleared.")
