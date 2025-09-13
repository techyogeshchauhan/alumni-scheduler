#!/usr/bin/env python3
"""
Startup and test script for Alumni Scheduler
"""

import subprocess
import time
import sys
import os
import threading
import requests
from urllib.parse import urljoin

def start_flask_app():
    """Start the Flask application in background"""
    try:
        print("🚀 Starting Flask application...")
        # Start Flask app in background
        process = subprocess.Popen([
            sys.executable, "app.py"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait a moment for the app to start
        time.sleep(3)
        
        # Check if app is running
        try:
            response = requests.get("http://localhost:5000", timeout=5)
            if response.status_code == 200:
                print("✅ Flask app started successfully!")
                return process
            else:
                print(f"❌ Flask app returned status {response.status_code}")
                return None
        except requests.exceptions.RequestException:
            print("❌ Flask app failed to start or is not responding")
            return None
            
    except Exception as e:
        print(f"❌ Error starting Flask app: {e}")
        return None

def run_tests():
    """Run the navbar and login tests"""
    print("\n🧪 Running tests...")
    try:
        result = subprocess.run([
            sys.executable, "test_navbar_login.py"
        ], capture_output=True, text=True, timeout=30)
        
        print(result.stdout)
        if result.stderr:
            print("Errors:", result.stderr)
            
        return result.returncode == 0
    except subprocess.TimeoutExpired:
        print("❌ Tests timed out")
        return False
    except Exception as e:
        print(f"❌ Error running tests: {e}")
        return False

def create_test_users():
    """Create test users for testing"""
    print("\n👥 Creating test users...")
    
    try:
        from pymongo import MongoClient
        from werkzeug.security import generate_password_hash
        from datetime import datetime
        import os
        from dotenv import load_dotenv
        
        load_dotenv()
        
        # Connect to MongoDB
        client = MongoClient(os.getenv("MONGO_URI", "mongodb://localhost:27017"))
        db = client["alumni_db"]
        users_collection = db["users"]
        
        # Test alumni user
        alumni_user = {
            "name": "Test Alumni",
            "email": "alumni@test.com",
            "password": generate_password_hash("password123"),
            "is_admin": False,
            "is_active": True,
            "phone": "+1234567890",
            "grad_year": 2020,
            "profile_picture": "",
            "preferences": {"email": True, "sms": False, "push": True},
            "created_at": datetime.utcnow(),
            "last_login": None,
            "failed_login_attempts": 0,
            "lockout_until": None,
            "bio": "Test alumni user for testing",
            "skills": ["Python", "JavaScript"],
            "interests": ["Technology", "Networking"],
            "social_links": {"linkedin": "", "twitter": "", "github": ""},
            "profile_privacy": "alumni_only"
        }
        
        # Test admin user
        admin_user = {
            "name": "Test Admin",
            "email": "admin@test.com", 
            "password": generate_password_hash("admin123"),
            "is_admin": True,
            "is_active": True,
            "phone": "+1234567890",
            "grad_year": 2018,
            "profile_picture": "",
            "preferences": {"email": True, "sms": False, "push": True},
            "created_at": datetime.utcnow(),
            "last_login": None,
            "failed_login_attempts": 0,
            "lockout_until": None,
            "bio": "Test admin user for testing",
            "skills": ["Management", "Python"],
            "interests": ["Administration", "Technology"],
            "social_links": {"linkedin": "", "twitter": "", "github": ""},
            "profile_privacy": "alumni_only"
        }
        
        # Insert users if they don't exist
        if not users_collection.find_one({"email": "alumni@test.com"}):
            users_collection.insert_one(alumni_user)
            print("✅ Created test alumni user: alumni@test.com / password123")
        else:
            print("ℹ️  Test alumni user already exists")
            
        if not users_collection.find_one({"email": "admin@test.com"}):
            users_collection.insert_one(admin_user)
            print("✅ Created test admin user: admin@test.com / admin123")
        else:
            print("ℹ️  Test admin user already exists")
            
        return True
        
    except Exception as e:
        print(f"❌ Error creating test users: {e}")
        return False

def show_usage_instructions():
    """Show usage instructions"""
    print("\n📋 Usage Instructions:")
    print("=" * 50)
    print("1. Open your browser and go to: http://localhost:5000")
    print("2. Test the navbar navigation")
    print("3. Try logging in with test accounts:")
    print("   👤 Alumni: alumni@test.com / password123")
    print("   🛡️  Admin: admin@test.com / admin123")
    print("4. Test different user roles and permissions")
    print("5. Check mobile responsiveness")
    print("\n🔍 What to test:")
    print("   - Navbar shows correct links for each user type")
    print("   - Login redirects to appropriate dashboard")
    print("   - Mobile menu works properly")
    print("   - Logout functionality works")
    print("   - Protected routes require authentication")

def main():
    """Main function"""
    print("🎯 Alumni Scheduler - Startup & Test Tool")
    print("=" * 50)
    
    # Check if required files exist
    required_files = ["app.py", "templates/base.html", "test_navbar_login.py"]
    missing_files = [f for f in required_files if not os.path.exists(f)]
    
    if missing_files:
        print("❌ Missing required files:")
        for f in missing_files:
            print(f"   - {f}")
        return
    
    # Create test users
    create_test_users()
    
    # Start Flask app
    flask_process = start_flask_app()
    
    if not flask_process:
        print("❌ Failed to start Flask app. Please check for errors.")
        return
    
    try:
        # Run tests
        tests_passed = run_tests()
        
        if tests_passed:
            print("✅ All tests passed!")
        else:
            print("⚠️  Some tests failed. Check output above.")
        
        # Show usage instructions
        show_usage_instructions()
        
        # Keep the app running
        print(f"\n🌐 Flask app is running at: http://localhost:5000")
        print("Press Ctrl+C to stop the server...")
        
        try:
            flask_process.wait()
        except KeyboardInterrupt:
            print("\n🛑 Stopping Flask app...")
            flask_process.terminate()
            flask_process.wait()
            print("✅ Flask app stopped.")
            
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        if flask_process:
            flask_process.terminate()

if __name__ == "__main__":
    main()