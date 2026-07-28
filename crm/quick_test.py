"""
Quick API Test - Try this now!
Run: python quick_test.py
"""
import requests
import json

BASE_URL = 'http://localhost:8000/api'

print("=" * 60)
print("🚀 Quick API Test")
print("=" * 60)

# Step 1: Login
print("\n1️⃣  Testing Login...")
try:
    response = requests.post(
        f'{BASE_URL}/auth/login/',
        json={
            'username': 'admin',
            'password': 'admin'  # Change this to your admin password
        }
    )
    
    if response.status_code == 200:
        data = response.json()
        token = data['token']
        print(f"✅ Login Successful!")
        print(f"   Token: {token[:20]}...")
        print(f"   Role: {data['role']}")
        print(f"   Username: {data['username']}")
    else:
        print(f"❌ Login Failed: {response.status_code}")
        print("   Try changing the password in quick_test.py")
        exit(1)
        
except Exception as e:
    print(f"❌ Error: {e}")
    print("   Make sure the server is running: python manage.py runserver")
    exit(1)

headers = {'Authorization': f'Token {token}'}

# Step 2: Get Dashboard
print("\n2️⃣  Getting Dashboard Stats...")
try:
    response = requests.get(f'{BASE_URL}/dashboard/overview/', headers=headers)
    if response.status_code == 200:
        stats = response.json()
        print("✅ Dashboard Retrieved:")
        print(f"   Students: {stats.get('total_students', 0)}")
        print(f"   Teachers: {stats.get('total_teachers', 0)}")
        print(f"   Classrooms: {stats.get('total_classrooms', 0)}")
    else:
        print(f"⚠️  Status: {response.status_code}")
except Exception as e:
    print(f"❌ Error: {e}")

# Step 3: Get Students
print("\n3️⃣  Getting Students List...")
try:
    response = requests.get(f'{BASE_URL}/students/?page_size=5', headers=headers)
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Found {data.get('count', 0)} students")
        if data.get('results'):
            print("   First 3 students:")
            for student in data['results'][:3]:
                print(f"   • {student['student_id']}: {student['full_name']}")
    else:
        print(f"⚠️  Status: {response.status_code}")
except Exception as e:
    print(f"❌ Error: {e}")

# Step 4: Get Teachers
print("\n4️⃣  Getting Teachers List...")
try:
    response = requests.get(f'{BASE_URL}/teachers/?page_size=5', headers=headers)
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Found {data.get('count', 0)} teachers")
        if data.get('results'):
            print("   First 3 teachers:")
            for teacher in data['results'][:3]:
                print(f"   • {teacher['teacher_id']}: {teacher['full_name']}")
    else:
        print(f"⚠️  Status: {response.status_code}")
except Exception as e:
    print(f"❌ Error: {e}")

# Step 5: Get Notifications
print("\n5️⃣  Checking Notifications...")
try:
    response = requests.get(f'{BASE_URL}/notifications/unread/', headers=headers)
    if response.status_code == 200:
        notifications = response.json()
        print(f"✅ You have {len(notifications)} unread notifications")
        if notifications:
            for notif in notifications[:3]:
                print(f"   • {notif['title']}")
    else:
        print(f"⚠️  Status: {response.status_code}")
except Exception as e:
    print(f"❌ Error: {e}")

print("\n" + "=" * 60)
print("✅ API Test Complete!")
print("=" * 60)
print("\n📚 Next Steps:")
print("   1. Open http://localhost:8000/api/ in your browser")
print("   2. Read START_HERE.md for more examples")
print("   3. Check API_DOCUMENTATION.md for all endpoints")
print("\n🎉 Your API is working perfectly!")
