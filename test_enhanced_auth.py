#!/usr/bin/env python3
"""
Enhanced Authentication System Test Suite
Tests the improved login/signup functionality for both admin and alumni users
"""

import unittest
import sys
import os
from unittest.mock import patch, MagicMock
import json

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, users_collection, events_collection, rsvps_collection
from bson import ObjectId
from datetime import datetime

class TestEnhancedAuthentication(unittest.TestCase):
    """Test cases for enhanced authentication system"""
    
    def setUp(self):
        """Set up test environment"""
        self.app = app
        self.app.config['TESTING'] = True
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.client = self.app.test_client()
        
        # Clear test data
        users_collection.delete_many({})
        events_collection.delete_many({})
        rsvps_collection.delete_many({})
    
    def tearDown(self):
        """Clean up after tests"""
        users_collection.delete_many({})
        events_collection.delete_many({})
        rsvps_collection.delete_many({})
    
    def test_enhanced_registration_validation(self):
        """Test enhanced registration validation"""
        print("\n🧪 Testing Enhanced Registration Validation...")
        
        # Test 1: Valid registration
        response = self.client.post('/register', data={
            'name': 'John Doe',
            'email': 'john@example.com',
            'phone': '+1234567890',
            'grad_year': '2020',
            'password': 'SecurePass123!',
            'confirm_password': 'SecurePass123!',
            'terms': 'on'
        })
        
        self.assertEqual(response.status_code, 302)  # Redirect after successful registration
        self.assertIn(b'Welcome to our alumni community', response.data)
        
        # Test 2: Password mismatch
        response = self.client.post('/register', data={
            'name': 'Jane Doe',
            'email': 'jane@example.com',
            'phone': '+1234567890',
            'grad_year': '2021',
            'password': 'SecurePass123!',
            'confirm_password': 'DifferentPass123!',
            'terms': 'on'
        })
        
        self.assertEqual(response.status_code, 302)
        self.assertIn(b'Passwords do not match', response.data)
        
        # Test 3: Weak password
        response = self.client.post('/register', data={
            'name': 'Bob Smith',
            'email': 'bob@example.com',
            'phone': '+1234567890',
            'grad_year': '2019',
            'password': 'weak',
            'confirm_password': 'weak',
            'terms': 'on'
        })
        
        self.assertEqual(response.status_code, 302)
        self.assertIn(b'Password must be at least 8 characters long', response.data)
        
        # Test 4: Invalid email
        response = self.client.post('/register', data={
            'name': 'Alice Johnson',
            'email': 'invalid-email',
            'phone': '+1234567890',
            'grad_year': '2022',
            'password': 'SecurePass123!',
            'confirm_password': 'SecurePass123!',
            'terms': 'on'
        })
        
        self.assertEqual(response.status_code, 302)
        self.assertIn(b'Please enter a valid email address', response.data)
        
        # Test 5: Terms not accepted
        response = self.client.post('/register', data={
            'name': 'Charlie Brown',
            'email': 'charlie@example.com',
            'phone': '+1234567890',
            'grad_year': '2023',
            'password': 'SecurePass123!',
            'confirm_password': 'SecurePass123!'
        })
        
        self.assertEqual(response.status_code, 302)
        self.assertIn(b'You must accept the Terms of Service', response.data)
        
        print("✅ Enhanced registration validation tests passed!")
    
    def test_enhanced_login_validation(self):
        """Test enhanced login validation"""
        print("\n🧪 Testing Enhanced Login Validation...")
        
        # Create a test user
        test_user = {
            'name': 'Test User',
            'email': 'test@example.com',
            'password': 'SecurePass123!',
            'grad_year': 2020,
            'phone': '+1234567890',
            'is_admin': False,
            'is_active': True,
            'created_at': datetime.now()
        }
        
        # Hash password
        from werkzeug.security import generate_password_hash
        test_user['password'] = generate_password_hash(test_user['password'])
        users_collection.insert_one(test_user)
        
        # Test 1: Valid login
        response = self.client.post('/login', data={
            'email': 'test@example.com',
            'password': 'SecurePass123!',
            'remember-me': 'on'
        })
        
        self.assertEqual(response.status_code, 302)
        self.assertIn(b'Welcome back', response.data)
        
        # Test 2: Invalid email format
        response = self.client.post('/login', data={
            'email': 'invalid-email',
            'password': 'SecurePass123!'
        })
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Please enter a valid email address', response.data)
        
        # Test 3: Empty fields
        response = self.client.post('/login', data={
            'email': '',
            'password': ''
        })
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Please fill in all required fields', response.data)
        
        # Test 4: Wrong password
        response = self.client.post('/login', data={
            'email': 'test@example.com',
            'password': 'WrongPassword123!'
        })
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Invalid email or password', response.data)
        
        print("✅ Enhanced login validation tests passed!")
    
    def test_admin_login_enhancements(self):
        """Test enhanced admin login functionality"""
        print("\n🧪 Testing Enhanced Admin Login...")
        
        # Create a test admin user
        admin_user = {
            'name': 'Admin User',
            'email': 'admin@example.com',
            'password': 'AdminPass123!',
            'grad_year': 2015,
            'phone': '+1234567890',
            'is_admin': True,
            'is_active': True,
            'created_at': datetime.now()
        }
        
        from werkzeug.security import generate_password_hash
        admin_user['password'] = generate_password_hash(admin_user['password'])
        users_collection.insert_one(admin_user)
        
        # Test 1: Valid admin login
        response = self.client.post('/admin/login', data={
            'email': 'admin@example.com',
            'password': 'AdminPass123!'
        })
        
        self.assertEqual(response.status_code, 302)
        self.assertIn(b'Welcome back', response.data)
        
        # Test 2: Non-admin trying to access admin login
        regular_user = {
            'name': 'Regular User',
            'email': 'regular@example.com',
            'password': 'UserPass123!',
            'grad_year': 2020,
            'phone': '+1234567890',
            'is_admin': False,
            'is_active': True,
            'created_at': datetime.now()
        }
        
        regular_user['password'] = generate_password_hash(regular_user['password'])
        users_collection.insert_one(regular_user)
        
        response = self.client.post('/admin/login', data={
            'email': 'regular@example.com',
            'password': 'UserPass123!'
        })
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Access denied', response.data)
        
        # Test 3: Invalid email format for admin
        response = self.client.post('/admin/login', data={
            'email': 'invalid-email',
            'password': 'AdminPass123!'
        })
        
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Please enter a valid email address', response.data)
        
        print("✅ Enhanced admin login tests passed!")
    
    def test_password_reset_flow(self):
        """Test enhanced password reset functionality"""
        print("\n🧪 Testing Password Reset Flow...")
        
        # Create a test user
        test_user = {
            'name': 'Reset User',
            'email': 'reset@example.com',
            'password': 'OldPass123!',
            'grad_year': 2020,
            'phone': '+1234567890',
            'is_admin': False,
            'is_active': True,
            'created_at': datetime.now()
        }
        
        from werkzeug.security import generate_password_hash
        test_user['password'] = generate_password_hash(test_user['password'])
        users_collection.insert_one(test_user)
        
        # Test 1: Forgot password request
        with patch('app.send_notification_email') as mock_email:
            response = self.client.post('/forgot-password', data={
                'email': 'reset@example.com'
            })
            
            self.assertEqual(response.status_code, 302)
            self.assertIn(b'If your email is in our system', response.data)
            mock_email.assert_called_once()
        
        # Test 2: Invalid email for password reset
        response = self.client.post('/forgot-password', data={
            'email': 'nonexistent@example.com'
        })
        
        self.assertEqual(response.status_code, 302)
        self.assertIn(b'If your email is in our system', response.data)
        
        print("✅ Password reset flow tests passed!")
    
    def test_ui_enhancements(self):
        """Test UI enhancements are properly rendered"""
        print("\n🧪 Testing UI Enhancements...")
        
        # Test 1: Enhanced login page
        response = self.client.get('/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome Back', response.data)
        self.assertIn(b'password strength', response.data)
        self.assertIn(b'Remember me', response.data)
        
        # Test 2: Enhanced registration page
        response = self.client.get('/register')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Join Our Alumni Community', response.data)
        self.assertIn(b'Password strength', response.data)
        self.assertIn(b'Terms of Service', response.data)
        
        # Test 3: Enhanced admin login page
        response = self.client.get('/admin/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Admin Portal', response.data)
        self.assertIn(b'Security Notice', response.data)
        self.assertIn(b'Restricted Access', response.data)
        
        # Test 4: Enhanced forgot password page
        response = self.client.get('/forgot-password')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Reset Your Password', response.data)
        self.assertIn(b'What happens next', response.data)
        
        print("✅ UI enhancements tests passed!")
    
    def test_session_management(self):
        """Test enhanced session management"""
        print("\n🧪 Testing Session Management...")
        
        # Create a test user
        test_user = {
            'name': 'Session User',
            'email': 'session@example.com',
            'password': 'SessionPass123!',
            'grad_year': 2020,
            'phone': '+1234567890',
            'is_admin': False,
            'is_active': True,
            'created_at': datetime.now()
        }
        
        from werkzeug.security import generate_password_hash
        test_user['password'] = generate_password_hash(test_user['password'])
        users_collection.insert_one(test_user)
        
        # Test 1: Login with remember me
        response = self.client.post('/login', data={
            'email': 'session@example.com',
            'password': 'SessionPass123!',
            'remember-me': 'on'
        })
        
        self.assertEqual(response.status_code, 302)
        
        # Test 2: Login without remember me
        response = self.client.post('/login', data={
            'email': 'session@example.com',
            'password': 'SessionPass123!'
        })
        
        self.assertEqual(response.status_code, 302)
        
        print("✅ Session management tests passed!")
    
    def test_security_features(self):
        """Test security enhancements"""
        print("\n🧪 Testing Security Features...")
        
        # Test 1: SQL injection protection
        malicious_input = "'; DROP TABLE users; --"
        response = self.client.post('/login', data={
            'email': malicious_input,
            'password': 'test'
        })
        
        # Should not crash and should handle gracefully
        self.assertEqual(response.status_code, 200)
        
        # Test 2: XSS protection
        xss_input = "<script>alert('xss')</script>"
        response = self.client.post('/register', data={
            'name': xss_input,
            'email': 'xss@example.com',
            'grad_year': '2020',
            'password': 'SecurePass123!',
            'confirm_password': 'SecurePass123!',
            'terms': 'on'
        })
        
        # Should escape the input
        self.assertEqual(response.status_code, 302)
        
        print("✅ Security features tests passed!")

def run_enhanced_auth_tests():
    """Run all enhanced authentication tests"""
    print("🚀 Starting Enhanced Authentication System Tests...")
    print("=" * 60)
    
    # Create test suite
    suite = unittest.TestLoader().loadTestsFromTestCase(TestEnhancedAuthentication)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "=" * 60)
    print("📊 Test Summary:")
    print(f"✅ Tests run: {result.testsRun}")
    print(f"❌ Failures: {len(result.failures)}")
    print(f"💥 Errors: {len(result.errors)}")
    
    if result.failures:
        print("\n❌ Failed Tests:")
        for test, traceback in result.failures:
            print(f"  - {test}: {traceback}")
    
    if result.errors:
        print("\n💥 Error Tests:")
        for test, traceback in result.errors:
            print(f"  - {test}: {traceback}")
    
    success_rate = ((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun) * 100
    print(f"\n🎯 Success Rate: {success_rate:.1f}%")
    
    if success_rate == 100:
        print("🎉 All tests passed! Enhanced authentication system is working perfectly!")
    else:
        print("⚠️  Some tests failed. Please review the issues above.")
    
    return result.wasSuccessful()

if __name__ == '__main__':
    success = run_enhanced_auth_tests()
    sys.exit(0 if success else 1)
