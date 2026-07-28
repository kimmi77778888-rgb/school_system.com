"""
Test the academic year list view to ensure it works
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crm.settings')
django.setup()

from django.test import RequestFactory, Client
from django.contrib.auth.models import User
from school.views import academic_year_list, academic_year_generate
from school.models import UserProfile, AcademicYear

print("Testing Academic Year Views...")
print("=" * 60)

# Check if users have profiles
print("\n1. Checking user profiles...")
users_without_profile = []
for user in User.objects.all():
    try:
        profile = user.profile
        print(f"   ✓ {user.username} has profile (role: {profile.role})")
    except UserProfile.DoesNotExist:
        users_without_profile.append(user)
        print(f"   ✗ {user.username} MISSING PROFILE!")

if users_without_profile:
    print(f"\n   ⚠ Found {len(users_without_profile)} users without profiles")
    print("   Creating missing profiles...")
    for user in users_without_profile:
        role = 'admin' if (user.is_staff or user.is_superuser) else 'student'
        UserProfile.objects.create(user=user, role=role)
        print(f"   ✓ Created profile for {user.username} (role: {role})")
else:
    print("   ✅ All users have profiles!")

# Check academic years
print("\n2. Checking academic years...")
years = AcademicYear.objects.all()
print(f"   Found {years.count()} academic year(s)")
for year in years:
    status = "✓ Active" if year.is_active else "  Inactive"
    print(f"   {status}: {year.year}")

if years.count() == 0:
    print("   ℹ No academic years found. You can create them using the generate form.")

# Test with Django test client
print("\n3. Testing view access...")
client = Client()

# Try to get an admin user
admin_user = User.objects.filter(is_superuser=True).first()
if not admin_user:
    admin_user = User.objects.filter(is_staff=True).first()
if not admin_user:
    admin_user = User.objects.filter(profile__role='admin').first()

if admin_user:
    print(f"   Using user: {admin_user.username}")
    client.force_login(admin_user)
    
    # Test academic year list
    try:
        response = client.get('/school/academic-years/')
        if response.status_code == 200:
            print(f"   ✅ Academic year list: OK (status {response.status_code})")
        else:
            print(f"   ⚠ Academic year list: Unexpected status {response.status_code}")
    except Exception as e:
        print(f"   ✗ Academic year list: ERROR - {e}")
    
    # Test academic year generate (GET)
    try:
        response = client.get('/school/academic-years/generate/')
        # Should redirect to list (302) or show list (200)
        if response.status_code in [200, 302]:
            print(f"   ✅ Academic year generate: OK (status {response.status_code})")
        else:
            print(f"   ⚠ Academic year generate: Unexpected status {response.status_code}")
    except Exception as e:
        print(f"   ✗ Academic year generate: ERROR - {e}")
else:
    print("   ⚠ No admin user found to test with")

print("\n" + "=" * 60)
print("✅ Test complete!")
print("\nTo test in browser:")
print("1. Make sure the Django server is running")
print("2. Visit: http://your-server/school/academic-years/")
print("3. The page should load without errors")
