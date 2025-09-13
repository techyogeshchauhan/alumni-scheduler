#!/usr/bin/env python3
"""
Final setup check for Alumni Event Scheduler
"""

import os
import re
import sys
from pathlib import Path

def check_template_titles():
    """Check that all templates have the correct title"""
    print("🔍 Checking template titles...")
    
    templates_dir = Path("templates")
    if not templates_dir.exists():
        print("❌ Templates directory not found")
        return False
    
    correct_branding = "Alumni Event Scheduler"
    issues = []
    
    for template_file in templates_dir.glob("*.html"):
        try:
            with open(template_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Check for title blocks
            title_matches = re.findall(r'{% block title %}(.+?){% endblock %}', content)
            
            for title in title_matches:
                if "Alumni Scheduler" in title and "Alumni Event Scheduler" not in title:
                    issues.append(f"{template_file.name}: Old branding found - '{title}'")
                elif correct_branding in title or "{{ " in title:
                    # Correct branding or dynamic title
                    continue
                elif template_file.name == "base.html":
                    # Base template has default title
                    continue
                else:
                    # Check if it needs branding
                    if not any(x in title.lower() for x in ["alumni", "scheduler", "event"]):
                        issues.append(f"{template_file.name}: Missing branding - '{title}'")
                        
        except Exception as e:
            issues.append(f"{template_file.name}: Error reading file - {e}")
    
    if issues:
        print("❌ Template title issues found:")
        for issue in issues:
            print(f"   - {issue}")
        return False
    else:
        print("✅ All template titles are correct")
        return True

def check_app_configuration():
    """Check app.py configuration"""
    print("\n🔍 Checking app.py configuration...")
    
    if not os.path.exists("app.py"):
        print("❌ app.py not found")
        return False
    
    try:
        with open("app.py", 'r', encoding='utf-8') as f:
            content = f.read()
        
        issues = []
        
        # Check for old branding in admin email
        if "admin@alumni-scheduler.com" in content:
            issues.append("Old admin email found")
        
        # Check for forgot password routes
        if "@app.route('/forgot-password'" not in content:
            issues.append("Forgot password route missing")
        
        if "@app.route('/reset-password/<token>'" not in content:
            issues.append("Reset password route missing")
        
        # Check for password reset token collection
        if "password_reset_tokens_collection" not in content:
            issues.append("Password reset tokens collection missing")
        
        if issues:
            print("❌ App configuration issues found:")
            for issue in issues:
                print(f"   - {issue}")
            return False
        else:
            print("✅ App configuration looks good")
            return True
            
    except Exception as e:
        print(f"❌ Error reading app.py: {e}")
        return False

def check_required_templates():
    """Check that all required templates exist"""
    print("\n🔍 Checking required templates...")
    
    required_templates = [
        "base.html",
        "index.html", 
        "login.html",
        "admin_login.html",
        "register.html",
        "forgot_password.html",
        "reset_password.html",
        "profile.html",
        "edit_profile.html",
        "profile_settings.html",
        "delete_profile.html",
        "directory.html",
        "alumni_dashboard.html",
        "admin_dashboard.html",
        "events.html",
        "event_detail.html",
        "create_event.html",
        "edit_event.html",
        "jobs.html",
        "job_detail.html",
        "post_job.html",
        "calendar.html",
        "search.html",
        "notifications.html"
    ]
    
    missing_templates = []
    
    for template in required_templates:
        template_path = Path(f"templates/{template}")
        if not template_path.exists():
            missing_templates.append(template)
    
    if missing_templates:
        print("❌ Missing templates:")
        for template in missing_templates:
            print(f"   - {template}")
        return False
    else:
        print("✅ All required templates exist")
        return True

def check_static_files():
    """Check static files"""
    print("\n🔍 Checking static files...")
    
    required_static = [
        "static/css/styles.css"
    ]
    
    missing_files = []
    
    for file_path in required_static:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
    
    if missing_files:
        print("❌ Missing static files:")
        for file_path in missing_files:
            print(f"   - {file_path}")
        return False
    else:
        print("✅ Static files exist")
        return True

def generate_test_data():
    """Generate test data script"""
    print("\n🔧 Generating test data script...")
    
    test_script = """#!/usr/bin/env python3
'''
Test data generator for Alumni Event Scheduler
'''

from pymongo import MongoClient
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

load_dotenv()

# MongoDB connection
client = MongoClient(os.getenv("MONGO_URI", "mongodb://localhost:27017"))
db = client["alumni_db"]

def create_test_users():
    '''Create test users'''
    users_collection = db["users"]
    
    # Test alumni user
    alumni_user = {
        "name": "John Doe",
        "email": "john@example.com",
        "password": generate_password_hash("password123"),
        "is_admin": False,
        "is_active": True,
        "phone": "+1234567890",
        "grad_year": 2020,
        "profile_picture": "",
        "bio": "Software engineer passionate about technology and community building.",
        "skills": ["Python", "JavaScript", "React", "Node.js"],
        "interests": ["Technology", "Hiking", "Photography"],
        "social_links": {
            "linkedin": "https://linkedin.com/in/johndoe",
            "twitter": "https://twitter.com/johndoe",
            "github": "https://github.com/johndoe"
        },
        "profile_privacy": "alumni_only",
        "preferences": {"email_notifications": True, "sms_notifications": False},
        "created_at": datetime.now(),
        "last_login": None,
        "failed_login_attempts": 0,
        "lockout_until": None
    }
    
    # Test admin user
    admin_user = {
        "name": "Admin User",
        "email": "admin@alumni-event-scheduler.com",
        "password": generate_password_hash("admin123"),
        "is_admin": True,
        "is_active": True,
        "phone": "+1234567890",
        "grad_year": 2018,
        "profile_picture": "",
        "bio": "System administrator managing the alumni community.",
        "skills": ["Administration", "Management", "Python"],
        "interests": ["Community Building", "Technology"],
        "social_links": {"linkedin": "", "twitter": "", "github": ""},
        "profile_privacy": "alumni_only",
        "preferences": {"email_notifications": True, "sms_notifications": True},
        "created_at": datetime.now(),
        "last_login": None,
        "failed_login_attempts": 0,
        "lockout_until": None
    }
    
    # Insert users if they don't exist
    if not users_collection.find_one({"email": "john@example.com"}):
        users_collection.insert_one(alumni_user)
        print("✅ Created test alumni user: john@example.com / password123")
    
    if not users_collection.find_one({"email": "admin@alumni-event-scheduler.com"}):
        users_collection.insert_one(admin_user)
        print("✅ Created test admin user: admin@alumni-event-scheduler.com / admin123")

def create_test_events():
    '''Create test events'''
    events_collection = db["events"]
    
    # Sample events
    events = [
        {
            "title": "Alumni Networking Night",
            "description": "Join us for an evening of networking and reconnecting with fellow alumni.",
            "date": datetime.now() + timedelta(days=7),
            "location": "Downtown Conference Center",
            "capacity": 100,
            "category": "Networking",
            "venue": {
                "name": "Conference Center",
                "address": "123 Main St, City",
                "phone": "+1234567890"
            },
            "tags": ["networking", "social", "alumni"],
            "attachments": [],
            "assigned_alumni": [],
            "created_at": datetime.now(),
            "is_published": True,
            "rsvp_count": 0
        },
        {
            "title": "Tech Talk: Future of AI",
            "description": "Explore the latest developments in artificial intelligence with industry experts.",
            "date": datetime.now() + timedelta(days=14),
            "location": "University Auditorium",
            "capacity": 200,
            "category": "Educational",
            "venue": {
                "name": "University Auditorium",
                "address": "456 Campus Dr, City",
                "phone": "+1234567891"
            },
            "tags": ["technology", "AI", "education"],
            "attachments": [],
            "assigned_alumni": [],
            "created_at": datetime.now(),
            "is_published": True,
            "rsvp_count": 0
        }
    ]
    
    for event in events:
        if not events_collection.find_one({"title": event["title"]}):
            events_collection.insert_one(event)
            print(f"✅ Created test event: {event['title']}")

if __name__ == "__main__":
    print("🚀 Creating test data for Alumni Event Scheduler...")
    create_test_users()
    create_test_events()
    print("✅ Test data creation complete!")
"""
    
    with open("create_test_data.py", "w", encoding="utf-8") as f:
        f.write(test_script)
    
    print("✅ Test data script created: create_test_data.py")

def main():
    """Run all checks"""
    print("🚀 Alumni Event Scheduler - Final Setup Check")
    print("=" * 50)
    
    all_good = True
    
    # Run all checks
    all_good &= check_required_templates()
    all_good &= check_template_titles()
    all_good &= check_app_configuration()
    all_good &= check_static_files()
    
    # Generate test data script
    generate_test_data()
    
    print("\n" + "=" * 50)
    
    if all_good:
        print("🎉 All checks passed! Alumni Event Scheduler is ready!")
        print("\n📋 Next steps:")
        print("1. Start MongoDB: mongod")
        print("2. Create test data: python create_test_data.py")
        print("3. Start the application: python app.py")
        print("4. Visit: http://localhost:5000")
        print("\n👥 Test accounts:")
        print("   Alumni: john@example.com / password123")
        print("   Admin: admin@alumni-event-scheduler.com / admin123")
    else:
        print("❌ Some issues found. Please fix them before running the application.")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())