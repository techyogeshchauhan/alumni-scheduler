#!/usr/bin/env python3
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
