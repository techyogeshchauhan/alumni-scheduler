#!/usr/bin/env python3
"""
Test script for email notifications functionality
"""

import os
import sys
from datetime import datetime
from bson import ObjectId

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, send_notification_email, users_collection, events_collection
from config import Config

def test_email_notifications():
    """Test email notification functionality"""
    print("🧪 Testing Email Notifications...")
    
    with app.app_context():
        # Test 1: Check if email function works
        print("\n1. Testing basic email function...")
        try:
            result = send_notification_email(
                ["test@example.com"],
                "Test Email",
                "<h1>This is a test email</h1><p>If you receive this, email functionality is working!</p>"
            )
            print(f"   ✅ Email function result: {result}")
        except Exception as e:
            print(f"   ❌ Email function failed: {e}")
        
        # Test 2: Check admin users
        print("\n2. Checking admin users...")
        try:
            admin_users = list(users_collection.find({"is_admin": True, "is_active": True}, {"name": 1, "email": 1}))
            print(f"   📊 Found {len(admin_users)} admin users")
            for admin in admin_users:
                print(f"      - {admin.get('name', 'Unknown')} ({admin.get('email', 'No email')})")
        except Exception as e:
            print(f"   ❌ Failed to get admin users: {e}")
        
        # Test 3: Check alumni users
        print("\n3. Checking alumni users...")
        try:
            alumni_users = list(users_collection.find({"is_admin": False, "is_active": True}, {"name": 1, "email": 1}))
            print(f"   📊 Found {len(alumni_users)} alumni users")
            for alumni in alumni_users[:3]:  # Show first 3
                print(f"      - {alumni.get('name', 'Unknown')} ({alumni.get('email', 'No email')})")
            if len(alumni_users) > 3:
                print(f"      ... and {len(alumni_users) - 3} more")
        except Exception as e:
            print(f"   ❌ Failed to get alumni users: {e}")
        
        # Test 4: Check events with assigned alumni
        print("\n4. Checking events with assigned alumni...")
        try:
            events_with_alumni = list(events_collection.find(
                {"assigned_alumni": {"$exists": True, "$ne": []}},
                {"title": 1, "assigned_alumni": 1, "created_at": 1}
            ).sort("created_at", -1).limit(3))
            print(f"   📊 Found {len(events_with_alumni)} events with assigned alumni")
            for event in events_with_alumni:
                alumni_count = len(event.get('assigned_alumni', []))
                print(f"      - {event.get('title', 'Unknown')} ({alumni_count} assigned alumni)")
        except Exception as e:
            print(f"   ❌ Failed to get events: {e}")
        
        # Test 5: Email configuration
        print("\n5. Checking email configuration...")
        try:
            config = Config()
            print(f"   📧 Mail server: {config.MAIL_SERVER}")
            print(f"   📧 Mail port: {config.MAIL_PORT}")
            print(f"   📧 Mail username: {config.MAIL_USERNAME}")
            print(f"   📧 Mail use TLS: {config.MAIL_USE_TLS}")
        except Exception as e:
            print(f"   ❌ Failed to get email config: {e}")
    
    print("\n🎉 Email notification testing completed!")

if __name__ == "__main__":
    test_email_notifications()
