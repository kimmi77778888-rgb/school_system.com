"""
Test script for Student Promotion API endpoints
Run with: python test_promotion_api.py
"""

import requests
import json

# Configuration
BASE_URL = "http://localhost:8000/api"
USERNAME = "admin"  # Change to your admin username
PASSWORD = "admin"  # Change to your admin password

class PromotionAPITester:
    def __init__(self):
        self.token = None
        self.base_url = BASE_URL
    
    def login(self):
        """Login and get authentication token"""
        print("\n" + "="*60)
        print("🔐 LOGGING IN...")
        print("="*60)
        
        response = requests.post(
            f"{self.base_url}/auth/login/",
            json={"username": USERNAME, "password": PASSWORD}
        )
        
        if response.status_code == 200:
            data = response.json()
            self.token = data.get('token')
            print(f"✅ Login successful!")
            print(f"   User: {data.get('username')} ({data.get('role')})")
            print(f"   Token: {self.token[:20]}...")
            return True
        else:
            print(f"❌ Login failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    
    def get_headers(self):
        """Get request headers with auth token"""
        return {
            "Authorization": f"Token {self.token}",
            "Content-Type": "application/json"
        }
    
    def test_check_eligibility(self, classroom_id=1):
        """Test check promotion eligibility endpoint"""
        print("\n" + "="*60)
        print("📋 TESTING: Check Promotion Eligibility")
        print("="*60)
        
        data = {
            "classroom_id": classroom_id,
            "passing_percentage": 50.0
        }
        
        print(f"Request: POST {self.base_url}/students/check_promotion_eligibility/")
        print(f"Data: {json.dumps(data, indent=2)}")
        
        response = requests.post(
            f"{self.base_url}/students/check_promotion_eligibility/",
            headers=self.get_headers(),
            json=data
        )
        
        print(f"\nResponse Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Success!")
            print(f"   Classroom: {result.get('classroom')}")
            print(f"   Total Students: {result.get('total_students')}")
            print(f"   Eligible: {result.get('eligible_count')}")
            
            if result.get('students'):
                print(f"\n   Sample Student:")
                student = result['students'][0]
                print(f"   - {student.get('student_name')}")
                print(f"   - Average: {student.get('avg_percentage')}%")
                print(f"   - Attendance: {student.get('attendance_rate')}%")
                print(f"   - Status: {student.get('promotion_status')}")
        else:
            print(f"❌ Failed: {response.text}")
    
    def test_available_classrooms(self, classroom_id=1):
        """Test get available promotion classrooms endpoint"""
        print("\n" + "="*60)
        print("🏫 TESTING: Get Available Classrooms")
        print("="*60)
        
        print(f"Request: GET {self.base_url}/students/available_promotions/?classroom_id={classroom_id}")
        
        response = requests.get(
            f"{self.base_url}/students/available_promotions/",
            headers=self.get_headers(),
            params={"classroom_id": classroom_id}
        )
        
        print(f"\nResponse Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Success!")
            print(f"   Current Classroom: {result.get('current_classroom')}")
            print(f"   Current Grade: {result.get('current_grade_number')}")
            print(f"   Next Grade: {result.get('next_grade_number')}")
            print(f"   Available Classrooms: {result.get('total_available')}")
            
            if result.get('available_classrooms'):
                print(f"\n   Available Options:")
                for classroom in result['available_classrooms'][:3]:
                    print(f"   - {classroom.get('name')}")
                    print(f"     Capacity: {classroom.get('current_students')}/{classroom.get('capacity')}")
                    print(f"     Has Timetable: {classroom.get('has_timetable')}")
        else:
            print(f"❌ Failed: {response.text}")
    
    def test_student_history(self, student_id=1):
        """Test get student history endpoint"""
        print("\n" + "="*60)
        print("📚 TESTING: Get Student History")
        print("="*60)
        
        print(f"Request: GET {self.base_url}/students/{student_id}/history/")
        
        response = requests.get(
            f"{self.base_url}/students/{student_id}/history/",
            headers=self.get_headers()
        )
        
        print(f"\nResponse Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Success!")
            print(f"   History Records: {len(result)}")
            
            if result:
                print(f"\n   Most Recent Record:")
                record = result[0]
                print(f"   - Year: {record.get('academic_year_name')}")
                print(f"   - Grade: {record.get('grade_name')}")
                print(f"   - Average Score: {record.get('average_score')}")
                print(f"   - Attendance: {record.get('attendance_percentage')}%")
                print(f"   - Status: {record.get('status_display')}")
        else:
            print(f"❌ Failed: {response.text}")
    
    def test_history_statistics(self, academic_year_id=1):
        """Test promotion statistics endpoint"""
        print("\n" + "="*60)
        print("📊 TESTING: Promotion Statistics")
        print("="*60)
        
        print(f"Request: GET {self.base_url}/student-history/promotion_statistics/?academic_year_id={academic_year_id}")
        
        response = requests.get(
            f"{self.base_url}/student-history/promotion_statistics/",
            headers=self.get_headers(),
            params={"academic_year_id": academic_year_id}
        )
        
        print(f"\nResponse Status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Success!")
            print(f"   Total Students: {result.get('total_students')}")
            print(f"   Promoted: {result.get('promoted')}")
            print(f"   Graduated: {result.get('graduated')}")
            print(f"   Average Score: {result.get('average_score')}")
            print(f"   Average Attendance: {result.get('average_attendance')}%")
            
            if result.get('by_grade_level'):
                print(f"\n   By Grade Level:")
                for level, stats in result['by_grade_level'].items():
                    print(f"   - {level}: {stats.get('total')} students, {stats.get('promoted')} promoted")
        else:
            print(f"❌ Failed: {response.text}")
    
    def run_all_tests(self):
        """Run all API tests"""
        print("\n" + "🎓"*30)
        print("   STUDENT PROMOTION API TEST SUITE")
        print("🎓"*30)
        
        if not self.login():
            print("\n❌ Cannot proceed without authentication")
            return
        
        # Run tests
        self.test_check_eligibility()
        self.test_available_classrooms()
        self.test_student_history()
        self.test_history_statistics()
        
        print("\n" + "="*60)
        print("✅ ALL TESTS COMPLETED")
        print("="*60)
        print("\nNote: Some tests may show errors if data doesn't exist yet.")
        print("Create classrooms, students, and scores first to see full results.")

if __name__ == "__main__":
    tester = PromotionAPITester()
    tester.run_all_tests()
