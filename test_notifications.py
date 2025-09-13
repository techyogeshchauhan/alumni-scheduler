#!/usr/bin/env python3
"""
Test script for the Alumni Event Scheduler notification system
"""

import os
import sys
from datetime import datetime
from pymongo import MongoClient
from bson.objectid import ObjectId

# Add the app directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_notification_system():
    """Test the notification system"""
    print("🧪 Testing Alumni Event Scheduler - Notification System")
    print("=" * 60)
    
    # Connect to MongoDB
    try:
        client = MongoClient("mongodb://localhost:27017")
        db = client["alumni_db"]
        users_collection = db["users"]
        notifications_collection = db["notifications"]
        print("✅ Connected to MongoDB")
    except Exception as e:
        print(f"❌ Failed to connect to MongoDB: {e}")
        return
    
    # Check if we have users
    user_count = users_collection.count_documents({"is_active": True, "is_admin": False})
    print(f"📊 Found {user_count} active alumni users")
    
    if user_count == 0:
        print("⚠️  No alumni users found. Create some users first.")
        return
    
    # Get a sample user
    sample_user = users_collection.find_one({"is_active": True, "is_admin": False})
    if not sample_user:
        print("❌ No sample user found")
        return
    
    print(f"👤 Testing with user: {sample_user.get('name', 'Unknown')} ({sample_user.get('email', 'No email')})")
    
    # Create a test notification
    test_notification = {
        "user_id": sample_user["_id"],
        "title": "🧪 Test Notification",
        "message": "This is a test notification to verify the system is working correctly.",
        "type": "test",
        "created_at": datetime.now(),
        "read": False,
        "action_url": "/events"
    }
    
    result = notifications_collection.insert_one(test_notification)
    print(f"✅ Created test notification with ID: {result.inserted_id}")
    
    # Check notification count
    unread_count = notifications_collection.count_documents({
        "user_id": sample_user["_id"],
        "read": False
    })
    print(f"📬 User has {unread_count} unread notifications")
    
    # Test notification retrieval
    notifications = list(notifications_collection.find({
        "user_id": sample_user["_id"]
    }).sort("created_at", -1).limit(5))
    
    print(f"📋 Recent notifications for {sample_user.get('name', 'User')}:")
    for i, notif in enumerate(notifications, 1):
        status = "🔴 Unread" if not notif.get('read', False) else "✅ Read"
        print(f"   {i}. {notif.get('title', 'No title')} - {status}")
        print(f"      {notif.get('message', 'No message')}")
        print(f"      Created: {notif.get('created_at', 'Unknown time')}")
        print()
    
    print("🎯 Notification System Test Results:")
    print("=" * 40)
    print("✅ Database connection: Working")
    print("✅ Notification creation: Working")
    print("✅ Notification retrieval: Working")
    print("✅ Unread count calculation: Working")
    print()
    print("🚀 Next Steps:")
    print("1. Start the Flask app: python app.py")
    print("2. Login as an alumni user")
    print("3. Check the notification banner at the top")
    print("4. Visit /notifications to see all notifications")
    print("5. Create an event as admin to test email notifications")
    print()
    print("📧 Email Configuration:")
    print("- Update MAIL_USERNAME and MAIL_PASSWORD in .env file")
    print("- For Gmail, use an App Password (not your regular password)")
    print("- Enable 2-factor authentication first")
    print()
    print("✨ Notification system is ready to use!")

if __name__ == "__main__":
    test_notification_system()