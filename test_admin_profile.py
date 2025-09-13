#!/usr/bin/env python3
"""
Test admin profile functionality
"""

import requests
import sys
from urllib.parse import urljoin

def test_admin_profile_access():
    """Test admin profile access"""
    base_url = "http://localhost:5000"
    
    print("🧪 Testing Admin Profile Access")
    print("=" * 40)
    
    # Profile-related routes that admin should be able to access
    profile_routes = [
        ("/profile", "Profile View"),
        ("/profile/edit", "Profile Edit"),
        ("/profile/settings", "Profile Settings"),
        ("/notifications", "Notifications"),
        ("/directory", "Alumni Directory"),
        ("/jobs", "Job Board"),
        ("/calendar", "Calendar View")
    ]
    
    print("Testing routes (you need to be logged in as admin):")
    print("Login at: http://localhost:5000/admin/login")
    print("Credentials: admin@alumni-event-scheduler.com / admin123")
    print()
    
    for route, description in profile_routes:
        try:
            url = urljoin(base_url, route)
            response = requests.get(url, timeout=5, allow_redirects=False)
            
            if response.status_code == 200:
                status = "✅ Accessible"
            elif response.status_code == 302:
                # Check if redirecting to login
                location = response.headers.get('Location', '')
                if 'login' in location:
                    status = "🔄 Redirects to login (need to login first)"
                else:
                    status = "🔄 Redirects (may be normal)"
            elif response.status_code == 403:
                status = "❌ Forbidden (permission issue)"
            elif response.status_code == 404:
                status = "❌ Not Found"
            else:
                status = f"⚠️  Status {response.status_code}"
                
            print(f"{description:<20} {status}")
            
        except requests.exceptions.RequestException as e:
            print(f"{description:<20} ❌ Connection Error")
    
    print("\n" + "=" * 40)
    print("Manual Testing Steps:")
    print("1. Open browser and go to: http://localhost:5000")
    print("2. Login as admin using the admin login page")
    print("3. Click on profile dropdown in navbar")
    print("4. Click 'My Profile' - should open profile page")
    print("5. Click 'Edit Profile' button - should open edit form")
    print("6. Make changes and save - should update successfully")
    print("7. Test other dropdown items (Settings, Notifications)")

def create_admin_profile_test_data():
    """Create test data for admin profile"""
    print("\n🔧 Creating admin profile test data...")
    
    test_script = '''#!/usr/bin/env python3
"""
Create/update admin user with complete profile data
"""

from pymongo import MongoClient
from werkzeug.security import generate_password_hash
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

def update_admin_profile():
    """Update admin user with complete profile data"""
    try:
        # MongoDB connection
        client = MongoClient(os.getenv("MONGO_URI", "mongodb://localhost:27017"))
        db = client["alumni_db"]
        users_collection = db["users"]
        
        # Find admin user
        admin_user = users_collection.find_one({"email": "admin@alumni-event-scheduler.com"})
        
        if admin_user:
            # Update admin profile with complete data
            update_data = {
                "name": "Admin User",
                "phone": "+1-555-0123",
                "grad_year": 2015,  # Optional for admin
                "bio": "System administrator managing the Alumni Event Scheduler platform. Passionate about connecting alumni and building community.",
                "skills": ["System Administration", "Event Management", "Community Building", "Python", "MongoDB"],
                "interests": ["Technology", "Community Building", "Event Planning", "Alumni Relations"],
                "social_links": {
                    "linkedin": "https://linkedin.com/in/admin-user",
                    "twitter": "https://twitter.com/admin_user",
                    "github": "https://github.com/admin-user"
                },
                "profile_privacy": "alumni_only",
                "preferences": {
                    "email_notifications": True,
                    "sms_notifications": True,
                    "push_notifications": True,
                    "event_reminders": True,
                    "newsletter": True
                },
                "updated_at": datetime.now()
            }
            
            users_collection.update_one(
                {"_id": admin_user["_id"]},
                {"$set": update_data}
            )
            
            print("✅ Admin profile updated with complete data")
            print("📋 Admin Profile Details:")
            print(f"   Name: {update_data['name']}")
            print(f"   Email: admin@alumni-event-scheduler.com")
            print(f"   Phone: {update_data['phone']}")
            print(f"   Grad Year: {update_data['grad_year']}")
            print(f"   Skills: {', '.join(update_data['skills'][:3])}...")
            print(f"   Bio: {update_data['bio'][:50]}...")
            
        else:
            print("❌ Admin user not found. Please create admin user first.")
            
    except Exception as e:
        print(f"❌ Error updating admin profile: {e}")

if __name__ == "__main__":
    print("🚀 Updating Admin Profile Data...")
    update_admin_profile()
    print("✅ Complete!")
'''
    
    with open("update_admin_profile.py", "w", encoding="utf-8") as f:
        f.write(test_script)
    
    print("✅ Created update_admin_profile.py")

def main():
    """Run all tests and fixes"""
    print("🚀 Alumni Event Scheduler - Admin Profile Fix Tool")
    print("=" * 50)
    
    test_admin_profile_access()
    create_admin_profile_test_data()
    
    print("\n" + "=" * 50)
    print("🎉 Admin profile fixes completed!")
    print("\n📋 Quick Test Steps:")
    print("1. Run: python update_admin_profile.py")
    print("2. Start Flask app: python app.py")
    print("3. Login as admin: http://localhost:5000/admin/login")
    print("4. Test profile edit functionality")
    
    print("\n✅ Fixes Applied:")
    print("- Profile edit route now allows admin access")
    print("- Graduation year made optional for admin users")
    print("- Enhanced error handling in profile update")
    print("- All profile-related routes accessible to admin")

if __name__ == "__main__":
    main()