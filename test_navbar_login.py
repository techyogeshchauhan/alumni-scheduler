#!/usr/bin/env python3
"""
Test script to verify navbar and login functionality
"""

import sys
import os
import requests
from urllib.parse import urljoin

def test_navbar_routes():
    """Test that all navbar routes are accessible"""
    base_url = "http://localhost:5000"
    
    # Routes that should be accessible without login
    public_routes = [
        "/",
        "/events",
        "/login",
        "/admin/login",
        "/register"
    ]
    
    # Routes that require authentication
    protected_routes = [
        "/dashboard",
        "/directory", 
        "/jobs",
        "/calendar",
        "/search",
        "/notifications",
        "/profile"
    ]
    
    # Admin routes
    admin_routes = [
        "/admin",
        "/create_event"
    ]
    
    print("🧪 Testing Navbar Routes...")
    
    # Test public routes
    print("\n📂 Testing Public Routes:")
    for route in public_routes:
        try:
            url = urljoin(base_url, route)
            response = requests.get(url, timeout=5)
            status = "✅ OK" if response.status_code in [200, 302] else f"❌ {response.status_code}"
            print(f"  {route}: {status}")
        except requests.exceptions.RequestException as e:
            print(f"  {route}: ❌ Connection Error - {e}")
    
    # Test protected routes (should redirect to login)
    print("\n🔒 Testing Protected Routes (should redirect):")
    for route in protected_routes:
        try:
            url = urljoin(base_url, route)
            response = requests.get(url, timeout=5, allow_redirects=False)
            status = "✅ Redirects" if response.status_code in [302, 401] else f"❌ {response.status_code}"
            print(f"  {route}: {status}")
        except requests.exceptions.RequestException as e:
            print(f"  {route}: ❌ Connection Error - {e}")
    
    # Test admin routes (should redirect to admin login)
    print("\n🛡️  Testing Admin Routes (should redirect):")
    for route in admin_routes:
        try:
            url = urljoin(base_url, route)
            response = requests.get(url, timeout=5, allow_redirects=False)
            status = "✅ Redirects" if response.status_code in [302, 401] else f"❌ {response.status_code}"
            print(f"  {route}: {status}")
        except requests.exceptions.RequestException as e:
            print(f"  {route}: ❌ Connection Error - {e}")

def test_login_functionality():
    """Test login form submission"""
    base_url = "http://localhost:5000"
    
    print("\n🔐 Testing Login Functionality...")
    
    # Test alumni login page
    try:
        login_url = urljoin(base_url, "/login")
        response = requests.get(login_url, timeout=5)
        if response.status_code == 200:
            print("  Alumni Login Page: ✅ Accessible")
            # Check if form elements exist
            if 'name="email"' in response.text and 'name="password"' in response.text:
                print("  Alumni Login Form: ✅ Form elements present")
            else:
                print("  Alumni Login Form: ❌ Missing form elements")
        else:
            print(f"  Alumni Login Page: ❌ {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"  Alumni Login Page: ❌ Connection Error - {e}")
    
    # Test admin login page
    try:
        admin_login_url = urljoin(base_url, "/admin/login")
        response = requests.get(admin_login_url, timeout=5)
        if response.status_code == 200:
            print("  Admin Login Page: ✅ Accessible")
            # Check if form elements exist
            if 'name="email"' in response.text and 'name="password"' in response.text:
                print("  Admin Login Form: ✅ Form elements present")
            else:
                print("  Admin Login Form: ❌ Missing form elements")
        else:
            print(f"  Admin Login Page: ❌ {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"  Admin Login Page: ❌ Connection Error - {e}")

def test_navbar_elements():
    """Test that navbar elements are properly rendered"""
    base_url = "http://localhost:5000"
    
    print("\n🧭 Testing Navbar Elements...")
    
    try:
        response = requests.get(base_url, timeout=5)
        if response.status_code == 200:
            content = response.text
            
            # Check for navbar elements
            navbar_elements = [
                'Alumni Scheduler',  # Logo/title
                'Events',           # Events link
                'Login',            # Login link
                'Admin',            # Admin link
                'Get Started'       # Register button
            ]
            
            for element in navbar_elements:
                if element in content:
                    print(f"  {element}: ✅ Present")
                else:
                    print(f"  {element}: ❌ Missing")
                    
            # Check for responsive menu
            if 'mobile-menu' in content:
                print("  Mobile Menu: ✅ Present")
            else:
                print("  Mobile Menu: ❌ Missing")
                
        else:
            print(f"  Homepage: ❌ {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"  Homepage: ❌ Connection Error - {e}")

def main():
    """Run all tests"""
    print("🚀 Alumni Scheduler - Navbar & Login Test Suite")
    print("=" * 50)
    
    # Check if server is running
    try:
        response = requests.get("http://localhost:5000", timeout=5)
        print("✅ Server is running")
    except requests.exceptions.RequestException:
        print("❌ Server is not running. Please start the Flask app first.")
        print("   Run: python app.py")
        return
    
    test_navbar_routes()
    test_login_functionality()
    test_navbar_elements()
    
    print("\n" + "=" * 50)
    print("🏁 Test Suite Complete!")
    print("\nIf you see any ❌ errors above, please check:")
    print("1. Flask app is running on localhost:5000")
    print("2. All route handlers are properly defined")
    print("3. Templates are rendering correctly")
    print("4. Database connection is working")

if __name__ == "__main__":
    main()