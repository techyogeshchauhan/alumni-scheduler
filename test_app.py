#!/usr/bin/env python3
"""
Test script for Alumni Event Scheduler
This script tests the basic functionality of the application.
"""

import os
import sys
import requests
import time
import subprocess
import threading
from pathlib import Path

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test if all required modules can be imported."""
    print("🔄 Testing imports...")
    try:
        import flask
        import pymongo
        import flask_login
        import flask_mail
        import werkzeug
        from bson.objectid import ObjectId
        from datetime import datetime
        print("✅ All imports successful")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_database_connection():
    """Test MongoDB connection."""
    print("🔄 Testing database connection...")
    try:
        from pymongo import MongoClient
        client = MongoClient("mongodb://localhost:27017", serverSelectionTimeoutMS=5000)
        client.server_info()
        print("✅ Database connection successful")
        return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

def test_app_creation():
    """Test if the Flask app can be created."""
    print("🔄 Testing Flask app creation...")
    try:
        from app import app
        print("✅ Flask app created successfully")
        return True
    except Exception as e:
        print(f"❌ Flask app creation failed: {e}")
        return False

def test_routes():
    """Test if routes are accessible."""
    print("🔄 Testing routes...")
    try:
        from app import app
        with app.test_client() as client:
            # Test homepage
            response = client.get('/')
            if response.status_code == 200:
                print("✅ Homepage route working")
            else:
                print(f"❌ Homepage route failed: {response.status_code}")
                return False
            
            # Test events page
            response = client.get('/events')
            if response.status_code == 200:
                print("✅ Events route working")
            else:
                print(f"❌ Events route failed: {response.status_code}")
                return False
            
            # Test login page
            response = client.get('/login')
            if response.status_code == 200:
                print("✅ Login route working")
            else:
                print(f"❌ Login route failed: {response.status_code}")
                return False
            
            # Test register page
            response = client.get('/register')
            if response.status_code == 200:
                print("✅ Register route working")
            else:
                print(f"❌ Register route failed: {response.status_code}")
                return False
            
        return True
    except Exception as e:
        print(f"❌ Route testing failed: {e}")
        return False

def test_user_registration():
    """Test user registration functionality."""
    print("🔄 Testing user registration...")
    try:
        from app import app
        with app.test_client() as client:
            # Test registration form
            response = client.post('/register', data={
                'name': 'Test User',
                'email': 'test@example.com',
                'password': 'testpassword123',
                'grad_year': '2020',
                'phone': '+1234567890'
            })
            
            if response.status_code == 302:  # Redirect after successful registration
                print("✅ User registration working")
                return True
            else:
                print(f"❌ User registration failed: {response.status_code}")
                return False
    except Exception as e:
        print(f"❌ User registration testing failed: {e}")
        return False

def test_file_upload():
    """Test file upload functionality."""
    print("🔄 Testing file upload...")
    try:
        # Check if upload directory exists
        upload_dir = Path("static/uploads")
        if upload_dir.exists():
            print("✅ Upload directory exists")
            return True
        else:
            print("❌ Upload directory does not exist")
            return False
    except Exception as e:
        print(f"❌ File upload testing failed: {e}")
        return False

def run_server_test():
    """Test if the server can start."""
    print("🔄 Testing server startup...")
    try:
        from app import app
        # Start server in a separate thread
        def run_server():
            app.run(debug=False, port=5001, use_reloader=False)
        
        server_thread = threading.Thread(target=run_server)
        server_thread.daemon = True
        server_thread.start()
        
        # Wait for server to start
        time.sleep(3)
        
        # Test if server is responding
        try:
            response = requests.get('http://localhost:5001', timeout=5)
            if response.status_code == 200:
                print("✅ Server started successfully")
                return True
            else:
                print(f"❌ Server responded with status: {response.status_code}")
                return False
        except requests.exceptions.RequestException:
            print("❌ Server not responding")
            return False
            
    except Exception as e:
        print(f"❌ Server startup failed: {e}")
        return False

def main():
    """Main test function."""
    print("🧪 Alumni Event Scheduler Test Suite")
    print("=" * 40)
    
    tests = [
        ("Import Test", test_imports),
        ("Database Connection", test_database_connection),
        ("Flask App Creation", test_app_creation),
        ("Route Testing", test_routes),
        ("User Registration", test_user_registration),
        ("File Upload", test_file_upload),
        ("Server Startup", run_server_test)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 Running {test_name}...")
        if test_func():
            passed += 1
        else:
            print(f"❌ {test_name} failed")
    
    print(f"\n📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The application is ready to use.")
        print("\nTo start the application:")
        print("python app.py")
        print("\nThen open your browser to: http://localhost:5000")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        print("\nCommon issues:")
        print("- MongoDB not running: Start MongoDB service")
        print("- Missing dependencies: Run 'pip install -r requirements.txt'")
        print("- Port conflicts: Make sure port 5000 is available")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
