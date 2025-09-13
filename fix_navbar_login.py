#!/usr/bin/env python3
"""
Fix script for navbar and login issues
"""

import os
import re

def fix_navbar_issues():
    """Fix common navbar issues"""
    print("🔧 Fixing Navbar Issues...")
    
    # Check if base.html exists and has proper structure
    base_template = "templates/base.html"
    if os.path.exists(base_template):
        print("✅ Base template exists")
        
        with open(base_template, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Check for common issues
        issues_found = []
        
        if 'get_current_user()' not in content:
            issues_found.append("Missing get_current_user() context")
            
        if 'nav-link' not in content:
            issues_found.append("Missing nav-link CSS classes")
            
        if 'mobile-menu' not in content:
            issues_found.append("Missing mobile menu")
            
        if issues_found:
            print("❌ Issues found in navbar:")
            for issue in issues_found:
                print(f"   - {issue}")
        else:
            print("✅ Navbar structure looks good")
    else:
        print("❌ Base template not found")

def fix_login_routes():
    """Check and fix login route issues"""
    print("\n🔧 Checking Login Routes...")
    
    app_file = "app.py"
    if os.path.exists(app_file):
        with open(app_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Check for required routes
        required_routes = [
            r'@app\.route\(["\']\/login["\']',
            r'@app\.route\(["\']\/admin\/login["\']',
            r'@app\.route\(["\']\/logout["\']',
            r'def login\(\):',
            r'def admin_login\(\):',
            r'def logout\(\):'
        ]
        
        missing_routes = []
        for route_pattern in required_routes:
            if not re.search(route_pattern, content):
                missing_routes.append(route_pattern)
        
        if missing_routes:
            print("❌ Missing routes:")
            for route in missing_routes:
                print(f"   - {route}")
        else:
            print("✅ All login routes present")
            
        # Check for session handling functions
        session_functions = [
            'get_user_session',
            'set_user_session', 
            'clear_user_session',
            'is_user_logged_in',
            'get_current_user'
        ]
        
        missing_functions = []
        for func in session_functions:
            if f'def {func}(' not in content:
                missing_functions.append(func)
                
        if missing_functions:
            print("❌ Missing session functions:")
            for func in missing_functions:
                print(f"   - {func}")
        else:
            print("✅ All session functions present")
    else:
        print("❌ app.py not found")

def fix_css_issues():
    """Check CSS file for navbar styles"""
    print("\n🔧 Checking CSS Styles...")
    
    css_file = "static/css/styles.css"
    if os.path.exists(css_file):
        with open(css_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Check for required CSS classes
        required_classes = [
            '.nav-link',
            '.mobile-nav-link',
            '.dropdown-item',
            '.btn-primary',
            '.card-enhanced'
        ]
        
        missing_classes = []
        for css_class in required_classes:
            if css_class not in content:
                missing_classes.append(css_class)
                
        if missing_classes:
            print("❌ Missing CSS classes:")
            for css_class in missing_classes:
                print(f"   - {css_class}")
        else:
            print("✅ All required CSS classes present")
    else:
        print("❌ CSS file not found")

def check_template_files():
    """Check if all required template files exist"""
    print("\n🔧 Checking Template Files...")
    
    required_templates = [
        "templates/base.html",
        "templates/login.html", 
        "templates/admin_login.html",
        "templates/alumni_dashboard.html",
        "templates/admin_dashboard.html"
    ]
    
    missing_templates = []
    for template in required_templates:
        if not os.path.exists(template):
            missing_templates.append(template)
        else:
            print(f"✅ {template}")
            
    if missing_templates:
        print("❌ Missing templates:")
        for template in missing_templates:
            print(f"   - {template}")

def generate_fix_recommendations():
    """Generate recommendations for fixing issues"""
    print("\n💡 Fix Recommendations:")
    print("=" * 40)
    
    recommendations = [
        "1. Ensure Flask app is running: python app.py",
        "2. Check database connection is working",
        "3. Verify all route decorators are correct",
        "4. Test login with valid credentials",
        "5. Check browser console for JavaScript errors",
        "6. Verify CSS files are loading properly",
        "7. Test responsive navbar on mobile devices",
        "8. Check session handling is working correctly"
    ]
    
    for rec in recommendations:
        print(f"   {rec}")

def main():
    """Run all fixes and checks"""
    print("🚀 Alumni Scheduler - Navbar & Login Fix Tool")
    print("=" * 50)
    
    fix_navbar_issues()
    fix_login_routes()
    fix_css_issues()
    check_template_files()
    generate_fix_recommendations()
    
    print("\n" + "=" * 50)
    print("🏁 Fix Check Complete!")
    print("\nNext steps:")
    print("1. Run the test script: python test_navbar_login.py")
    print("2. Start your Flask app: python app.py")
    print("3. Test the navbar and login functionality manually")

if __name__ == "__main__":
    main()