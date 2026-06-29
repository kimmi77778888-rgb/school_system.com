"""
Clear broken local image paths from the production database.
On Render, local media files don't exist — only Cloudinary images do.
This script clears any image paths that look like local uploads.
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crm.settings')
django.setup()

# Only run on production (Render has DATABASE_URL)
if not os.environ.get('DATABASE_URL'):
    print("Local environment — skipping fix_images.py")
    exit(0)

from school.models import Student, Teacher, UserProfile, SchoolSettings

def is_local_path(field):
    """Return True if the image field has a path but it's not a Cloudinary URL."""
    if not field or not field.name:
        return False
    name = field.name
    # Cloudinary URLs contain 'cloudinary' or start with 'http'
    # Local paths are just relative file paths like 'images/...'
    if name.startswith('http') or 'cloudinary' in name.lower():
        return False
    # Check if file actually exists on disk
    try:
        if hasattr(field, 'path') and os.path.exists(field.path):
            return False  # File exists locally, keep it
    except Exception:
        pass
    return True  # Local path but file doesn't exist — clear it

# Clear broken student photos
count = 0
for s in Student.objects.exclude(photo='').exclude(photo=None):
    if is_local_path(s.photo):
        Student.objects.filter(pk=s.pk).update(photo='')
        count += 1
print(f"Cleared {count} broken student photos")

# Clear broken teacher photos
count = 0
for t in Teacher.objects.exclude(photo='').exclude(photo=None):
    if is_local_path(t.photo):
        Teacher.objects.filter(pk=t.pk).update(photo='')
        count += 1
print(f"Cleared {count} broken teacher photos")

# Clear broken user profile photos
count = 0
for p in UserProfile.objects.exclude(photo='').exclude(photo=None):
    if is_local_path(p.photo):
        UserProfile.objects.filter(pk=p.pk).update(photo='')
        count += 1
print(f"Cleared {count} broken user profile photos")

# Clear broken school logo/favicon
settings = SchoolSettings.objects.filter(pk=1).first()
if settings:
    changed = False
    if is_local_path(settings.logo):
        settings.logo = ''
        changed = True
        print("Cleared broken school logo")
    if is_local_path(settings.favicon):
        settings.favicon = ''
        changed = True
        print("Cleared broken school favicon")
    if changed:
        settings.save()

print("Done! fix_images complete.")
