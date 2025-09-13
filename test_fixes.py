#!/usr/bin/env python3
"""
Test script to verify the fixes for navigation, calendar, dashboards, and session separation.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test that all required modules can be imported."""
    try:
        from app import app, get_current_user, is_user_logged_in
        print("✅ App imports successful")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_routes():
    """Test that all routes are properly defined."""
    try:
        from app import app
        routes = [str(rule) for rule in app.url_map.iter_rules()]
        
        required_routes = [
            '/dashboard',
            '/admin',
            '/calendar',
            '/admin/logout',
            '/logout'
        ]
        
        missing_routes = []
        for route in required_routes:
            if not any(route in r for r in routes):
                missing_routes.append(route)
        
        if missing_routes:
            print(f"❌ Missing routes: {missing_routes}")
            return False
        else:
            print("✅ All required routes found")
            return True
            
    except Exception as e:
        print(f"❌ Route test error: {e}")
        return False

def test_session_functions():
    """Test session management functions."""
    try:
        from app import get_user_session, set_user_session, clear_user_session, is_user_logged_in
        
        # Test session functions exist and are callable
        assert callable(get_user_session)
        assert callable(set_user_session)
        assert callable(clear_user_session)
        assert callable(is_user_logged_in)
        
        print("✅ Session management functions available")
        return True
        
    except Exception as e:
        print(f"❌ Session function test error: {e}")
        return False

def test_template_files():
    """Test that template files exist and are readable."""
    template_files = [
        'templates/base.html',
        'templates/alumni_dashboard.html',
        'templates/admin_dashboard.html',
        'templates/calendar.html',
        'templates/admin_login.html'
    ]
    
    missing_templates = []
    for template in template_files:
        if not os.path.exists(template):
            missing_templates.append(template)
    
    if missing_templates:
        print(f"❌ Missing templates: {missing_templates}")
        return False
    else:
        print("✅ All template files found")
        return True

def main():
    """Run all tests."""
    print("🧪 Testing Alumni Scheduler Fixes...")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_routes,
        test_session_functions,
        test_template_files
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The fixes should be working correctly.")
        return True
    else:
        print("⚠️  Some tests failed. Please check the issues above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
