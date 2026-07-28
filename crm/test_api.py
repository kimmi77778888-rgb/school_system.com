"""
Simple script to test the REST API endpoints
"""
import requests
import json
from pprint import pprint

BASE_URL = 'http://localhost:8000/api'

def test_api():
    """Test basic API endpoints"""
    
    print("=" * 60)
    print("Testing School Management System REST API")
    print("=" * 60)
    
    # Step 1: Login
    print("\n1. Testing login...")
    login_data = {
        'username': input("Enter username: "),
        'password': input("Enter password: ")
    }
    
    try:
        response = requests.post(f'{BASE_URL}/auth/login/', json=login_data)
        response.raise_for_status()
        auth_data = response.json()
        token = auth_data['token']
        print(f"✓ Login successful!")
        print(f"  Token: {token}")
        print(f"  Role: {auth_data['role']}")
    except requests.exceptions.RequestException as e:
        print(f"✗ Login failed: {e}")
        return
    
    # Headers for authenticated requests
    headers = {'Authorization': f'Token {token}'}
    
    # Step 2: Test Dashboard Overview
    print("\n2. Testing dashboard overview...")
    try:
        response = requests.get(f'{BASE_URL}/dashboard/overview/', headers=headers)
        response.raise_for_status()
        overview = response.json()
        print("✓ Dashboard data retrieved:")
        pprint(overview)
    except requests.exceptions.RequestException as e:
        print(f"✗ Failed: {e}")
    
    # Step 3: Test Students List
    print("\n3. Testing students list...")
    try:
        response = requests.get(f'{BASE_URL}/students/', headers=headers, params={'page_size': 5})
        response.raise_for_status()
        students = response.json()
        print(f"✓ Found {students.get('count', 0)} students")
        if students.get('results'):
            print("\nFirst 3 students:")
            for student in students['results'][:3]:
                print(f"  - {student['student_id']}: {student['full_name']} ({student.get('classroom_name', 'No class')})")
    except requests.exceptions.RequestException as e:
        print(f"✗ Failed: {e}")
    
    # Step 4: Test Teachers List
    print("\n4. Testing teachers list...")
    try:
        response = requests.get(f'{BASE_URL}/teachers/', headers=headers, params={'page_size': 5})
        response.raise_for_status()
        teachers = response.json()
        print(f"✓ Found {teachers.get('count', 0)} teachers")
        if teachers.get('results'):
            print("\nFirst 3 teachers:")
            for teacher in teachers['results'][:3]:
                print(f"  - {teacher['teacher_id']}: {teacher['full_name']} ({teacher.get('subject_specialty', 'N/A')})")
    except requests.exceptions.RequestException as e:
        print(f"✗ Failed: {e}")
    
    # Step 5: Test Active Academic Year
    print("\n5. Testing active academic year...")
    try:
        response = requests.get(f'{BASE_URL}/academic-years/active/', headers=headers)
        response.raise_for_status()
        academic_year = response.json()
        print(f"✓ Active academic year: {academic_year.get('year')}")
    except requests.exceptions.RequestException as e:
        print(f"✗ Failed: {e}")
    
    # Step 6: Test Today's Attendance
    print("\n6. Testing today's attendance statistics...")
    try:
        response = requests.get(f'{BASE_URL}/dashboard/attendance_today/', headers=headers)
        response.raise_for_status()
        attendance = response.json()
        print("✓ Attendance statistics:")
        print("\n  Students:")
        for key, value in attendance.get('students', {}).items():
            print(f"    {key}: {value}")
        print("\n  Teachers:")
        for key, value in attendance.get('teachers', {}).items():
            print(f"    {key}: {value}")
    except requests.exceptions.RequestException as e:
        print(f"✗ Failed: {e}")
    
    # Step 7: Test Unread Notifications
    print("\n7. Testing unread notifications...")
    try:
        response = requests.get(f'{BASE_URL}/notifications/unread/', headers=headers)
        response.raise_for_status()
        notifications = response.json()
        print(f"✓ You have {len(notifications)} unread notifications")
        if notifications:
            print("\nRecent notifications:")
            for notif in notifications[:3]:
                print(f"  - {notif['title']}")
    except requests.exceptions.RequestException as e:
        print(f"✗ Failed: {e}")
    
    # Step 8: Test Upcoming Events
    print("\n8. Testing upcoming events...")
    try:
        response = requests.get(f'{BASE_URL}/school-events/upcoming/', headers=headers)
        response.raise_for_status()
        events = response.json()
        print(f"✓ Found {len(events)} upcoming events")
        if events:
            print("\nUpcoming events:")
            for event in events[:3]:
                print(f"  - {event['title']} ({event['start_date']})")
    except requests.exceptions.RequestException as e:
        print(f"✗ Failed: {e}")
    
    # Step 9: Test Current User Profile
    print("\n9. Testing current user profile...")
    try:
        response = requests.get(f'{BASE_URL}/user-profiles/my_profile/', headers=headers)
        response.raise_for_status()
        profile = response.json()
        print("✓ Your profile:")
        print(f"  Role: {profile.get('role_display')}")
        print(f"  Phone: {profile.get('phone', 'N/A')}")
    except requests.exceptions.RequestException as e:
        print(f"✗ Failed: {e}")
    
    print("\n" + "=" * 60)
    print("API Testing Complete!")
    print("=" * 60)
    print("\nFor full API documentation, see API_DOCUMENTATION.md")
    print("Or visit http://localhost:8000/api/ in your browser")


if __name__ == '__main__':
    test_api()
