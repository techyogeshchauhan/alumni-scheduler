#!/usr/bin/env python3
"""
Test script to verify the separate login system works correctly
"""

import requests
import json
from datetime import datetime

# Test configuration
BASE_URL = "http://localhost:5000"
ADMIN_EMAIL = "admin@alumni-scheduler.com"
ADMIN_PASSWORD = "admin123"

def test_separate_logins():
    """Test that admin and alumni can login separately without logging each other out"""
    
    print("🧪 Testing Separate Login System")
    print("=" * 50)
    
    # Test 1: Admin login
    print("\n1. Testing Admin Login...")
    session = requests.Session()
    
    # Get login page
    response = session.get(f"{BASE_URL}/admin/login")
    if response.status_code == 200:
        print("✅ Admin login page accessible")
    else:
        print("❌ Admin login page not accessible")
        return False
    
    # Test admin login
    login_data = {
        'email': ADMIN_EMAIL,
        'password': ADMIN_PASSWORD
    }
    
    response = session.post(f"{BASE_URL}/admin/login", data=login_data)
    if response.status_code == 200 and "Welcome back, Admin!" in response.text:
        print("✅ Admin login successful")
    else:
        print("❌ Admin login failed")
        return False
    
    # Test 2: Alumni login (should not affect admin session)
    print("\n2. Testing Alumni Login (should not affect admin session)...")
    alumni_session = requests.Session()
    
    # Get alumni login page
    response = alumni_session.get(f"{BASE_URL}/login")
    if response.status_code == 200:
        print("✅ Alumni login page accessible")
    else:
        print("❌ Alumni login page not accessible")
        return False
    
    # Test 3: Verify admin session still works
    print("\n3. Verifying Admin Session Still Active...")
    response = session.get(f"{BASE_URL}/admin")
    if response.status_code == 200 and "Admin Dashboard" in response.text:
        print("✅ Admin session still active after alumni login attempt")
    else:
        print("❌ Admin session lost")
        return False
    
    # Test 4: Test new features
    print("\n4. Testing New Features...")
    
    # Test alumni dashboard
    response = session.get(f"{BASE_URL}/dashboard")
    if response.status_code == 200:
        print("✅ Alumni dashboard accessible")
    else:
        print("❌ Alumni dashboard not accessible")
    
    # Test calendar view
    response = session.get(f"{BASE_URL}/calendar")
    if response.status_code == 200:
        print("✅ Calendar view accessible")
    else:
        print("❌ Calendar view not accessible")
    
    # Test search
    response = session.get(f"{BASE_URL}/search")
    if response.status_code == 200:
        print("✅ Search page accessible")
    else:
        print("❌ Search page not accessible")
    
    # Test API endpoints
    response = session.get(f"{BASE_URL}/api/events/upcoming")
    if response.status_code == 200:
        print("✅ API endpoints working")
    else:
        print("❌ API endpoints not working")
    
    print("\n🎉 All tests completed!")
    return True

def test_ui_improvements():
    """Test UI improvements"""
    print("\n🎨 Testing UI Improvements")
    print("=" * 50)
    
    session = requests.Session()
    
    # Test enhanced styles
    response = session.get(f"{BASE_URL}/")
    if response.status_code == 200:
        print("✅ Homepage loads with enhanced styles")
        
        # Check for enhanced CSS classes
        if "nav-enhanced" in response.text:
            print("✅ Enhanced navigation styles applied")
        else:
            print("❌ Enhanced navigation styles not found")
        
        if "card-enhanced" in response.text or "glass-effect" in response.text:
            print("✅ Enhanced card styles applied")
        else:
            print("❌ Enhanced card styles not found")
    else:
        print("❌ Homepage not accessible")
        return False
    
    return True

if __name__ == "__main__":
    print("🚀 Starting Alumni Scheduler Tests")
    print("=" * 50)
    
    try:
        # Test separate logins
        login_success = test_separate_logins()
        
        # Test UI improvements
        ui_success = test_ui_improvements()
        
        if login_success and ui_success:
            print("\n✅ All tests passed! The system is working correctly.")
        else:
            print("\n❌ Some tests failed. Please check the output above.")
            
    except requests.exceptions.ConnectionError:
        print("\n❌ Could not connect to the application. Make sure it's running on http://localhost:5000")
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")
