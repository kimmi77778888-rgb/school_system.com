"""
Verify Student Promotion API Deployment
Tests that all new endpoints are working on production server
"""

import requests
import json
import sys

# Configuration
PRODUCTION_URL = "https://school-system-com.onrender.com"  # Update with your Render URL
API_BASE = f"{PRODUCTION_URL}/api"

class DeploymentVerifier:
    def __init__(self, production_url=None):
        self.base_url = production_url or API_BASE
        self.token = None
        self.errors = []
        self.successes = []
    
    def print_header(self, title):
        print("\n" + "="*60)
        print(f"  {title}")
        print("="*60)
    
    def test_login(self, username="admin", password="admin"):
        """Test login and get token"""
        self.print_header("🔐 TESTING: Authentication")
        
        try:
            response = requests.post(
                f"{self.base_url}/auth/login/",
                json={"username": username, "password": password},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                self.token = data.get('token')
                print(f"✅ Login successful!")
                print(f"   User: {data.get('username')} ({data.get('role')})")
                self.successes.append("Authentication")
                return True
            else:
                print(f"❌ Login failed: {response.status_code}")
                print(f"   Response: {response.text}")
                self.errors.append(f"Authentication failed: {response.status_code}")
                return False
        except requests.exceptions.RequestException as e:
            print(f"❌ Connection error: {e}")
            self.errors.append(f"Authentication error: {e}")
            return False
    
    def get_headers(self):
        return {
            "Authorization": f"Token {self.token}",
            "Content-Type": "application/json"
        }
    
    def test_endpoint(self, name, method, endpoint, data=None, params=None):
        """Test a single endpoint"""
        print(f"\n📍 Testing: {name}")
        print(f"   {method} {endpoint}")
        
        try:
            url = f"{self.base_url}{endpoint}"
            
            if method == "GET":
                response = requests.get(url, headers=self.get_headers(), params=params, timeout=10)
            elif method == "POST":
                response = requests.post(url, headers=self.get_headers(), json=data, timeout=10)
            else:
                print(f"❌ Unsupported method: {method}")
                return False
            
            if response.status_code in [200, 201]:
                print(f"✅ Success! Status: {response.status_code}")
                self.successes.append(name)
                return True
            elif response.status_code == 400:
                # Expected for some endpoints without data
                print(f"⚠️  Expected error: {response.status_code}")
                print(f"   Response: {response.json()}")
                self.successes.append(f"{name} (expected error)")
                return True
            else:
                print(f"❌ Failed: {response.status_code}")
                print(f"   Response: {response.text[:200]}")
                self.errors.append(f"{name}: Status {response.status_code}")
                return False
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Request error: {e}")
            self.errors.append(f"{name}: {e}")
            return False
    
    def run_verification(self):
        """Run all verification tests"""
        print("\n" + "🎓"*30)
        print("   STUDENT PROMOTION API DEPLOYMENT VERIFICATION")
        print("🎓"*30)
        
        print(f"\n🌐 Testing production URL: {self.base_url}")
        
        # Test authentication first
        if not self.test_login():
            print("\n❌ Cannot proceed without authentication")
            print("\nPlease check:")
            print("1. Is the server running?")
            print("2. Is the URL correct?")
            print("3. Are the credentials correct?")
            return False
        
        # Test promotion endpoints
        self.print_header("📋 TESTING: Promotion Endpoints")
        
        # 1. Check eligibility (will fail without classroom, but endpoint exists)
        self.test_endpoint(
            "Check Promotion Eligibility",
            "POST",
            "/students/check_promotion_eligibility/",
            data={"classroom_id": 1}
        )
        
        # 2. Available promotions (will fail without classroom, but endpoint exists)
        self.test_endpoint(
            "Available Promotions",
            "GET",
            "/students/available_promotions/",
            params={"classroom_id": 1}
        )
        
        # 3. Student history list
        self.test_endpoint(
            "Student History List",
            "GET",
            "/student-history/"
        )
        
        # 4. History by student (will return empty if no data)
        self.test_endpoint(
            "History by Student",
            "GET",
            "/student-history/by_student/",
            params={"student_id": 1}
        )
        
        # 5. History by academic year
        self.test_endpoint(
            "History by Academic Year",
            "GET",
            "/student-history/by_academic_year/",
            params={"academic_year_id": 1}
        )
        
        # 6. Promotion statistics
        self.test_endpoint(
            "Promotion Statistics",
            "GET",
            "/student-history/promotion_statistics/",
            params={"academic_year_id": 1}
        )
        
        # Print summary
        self.print_header("📊 VERIFICATION SUMMARY")
        
        print(f"\n✅ Successful: {len(self.successes)}")
        for success in self.successes:
            print(f"   • {success}")
        
        if self.errors:
            print(f"\n❌ Failed: {len(self.errors)}")
            for error in self.errors:
                print(f"   • {error}")
        
        print("\n" + "="*60)
        
        if len(self.errors) == 0:
            print("✅ ALL ENDPOINTS DEPLOYED SUCCESSFULLY!")
            print("\nThe Student Promotion API is live and ready to use.")
            return True
        else:
            print("⚠️  SOME ENDPOINTS HAD ISSUES")
            print("\nPlease check the Render logs for more details.")
            return False

def main():
    """Main function"""
    print("\n" + "🎓"*30)
    print("   PROMOTION API DEPLOYMENT VERIFIER")
    print("🎓"*30)
    
    # Get production URL
    production_url = input(f"\nEnter production URL (or press Enter for default):\n[{PRODUCTION_URL}]: ").strip()
    if not production_url:
        production_url = PRODUCTION_URL
    
    api_base = f"{production_url}/api"
    
    # Get credentials
    print("\nEnter admin credentials:")
    username = input("Username [admin]: ").strip() or "admin"
    password = input("Password [admin]: ").strip() or "admin"
    
    # Run verification
    verifier = DeploymentVerifier(api_base)
    
    print("\n🚀 Starting verification...")
    
    # Override credentials
    success = verifier.test_login(username, password)
    if success:
        verifier.run_verification()
    
    print("\n" + "="*60)
    print("📚 For API documentation, see: API_PROMOTION_GUIDE.md")
    print("="*60 + "\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n✅ Verification cancelled by user.")
        sys.exit(0)
