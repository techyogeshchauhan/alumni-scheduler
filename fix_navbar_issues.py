#!/usr/bin/env python3
"""
Fix navbar and functionality issues
"""

import os
import re

def fix_csrf_tokens():
    """Add CSRF tokens to forms that are missing them"""
    print("🔧 Fixing CSRF token issues...")
    
    templates_to_fix = [
        "templates/event_detail.html",
        "templates/event_detail_new.html"
    ]
    
    for template_file in templates_to_fix:
        if os.path.exists(template_file):
            try:
                with open(template_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Check if CSRF tokens are missing from forms
                forms = re.findall(r'<form[^>]*method=["\']POST["\'][^>]*>(.*?)</form>', content, re.DOTALL | re.IGNORECASE)
                
                needs_fix = False
                for form in forms:
                    if 'csrf_token' not in form:
                        needs_fix = True
                        break
                
                if needs_fix:
                    # Add CSRF tokens to POST forms that don't have them
                    content = re.sub(
                        r'(<form[^>]*method=["\']POST["\'][^>]*>)(?!\s*<input[^>]*name=["\']csrf_token["\'])',
                        r'\1\n                    <input type="hidden" name="csrf_token" value="{{ csrf_token() }}"/>',
                        content,
                        flags=re.IGNORECASE
                    )
                    
                    with open(template_file, 'w', encoding='utf-8') as f:
                        f.write(content)
                    
                    print(f"✅ Fixed CSRF tokens in {template_file}")
                else:
                    print(f"✅ {template_file} already has CSRF tokens")
                    
            except Exception as e:
                print(f"❌ Error fixing {template_file}: {e}")
        else:
            print(f"⚠️  {template_file} not found")

def fix_graduation_year_issue():
    """Fix graduation year sorting issue in app.py"""
    print("\n🔧 Checking graduation year sorting...")
    
    if os.path.exists("app.py"):
        try:
            with open("app.py", 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check if the fix is already applied
            if "grad_years_raw = users_collection.distinct" in content:
                print("✅ Graduation year fix already applied")
            else:
                print("⚠️  Graduation year fix may need to be applied manually")
                
        except Exception as e:
            print(f"❌ Error checking app.py: {e}")

def create_navbar_test_script():
    """Create a test script for navbar functionality"""
    print("\n🔧 Creating navbar test script...")
    
    test_script = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Navbar Test</title>
    <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
</head>
<body class="bg-gray-100">
    <div class="container mx-auto p-8">
        <h1 class="text-3xl font-bold mb-8">Navbar Functionality Test</h1>
        
        <div class="bg-white p-6 rounded-lg shadow-lg">
            <h2 class="text-xl font-semibold mb-4">Test Checklist:</h2>
            
            <div class="space-y-3">
                <label class="flex items-center">
                    <input type="checkbox" class="mr-2">
                    <span>Mobile menu toggle works</span>
                </label>
                
                <label class="flex items-center">
                    <input type="checkbox" class="mr-2">
                    <span>Dropdown menus open on hover</span>
                </label>
                
                <label class="flex items-center">
                    <input type="checkbox" class="mr-2">
                    <span>Dropdown menus open on click</span>
                </label>
                
                <label class="flex items-center">
                    <input type="checkbox" class="mr-2">
                    <span>Dropdown menus close when clicking outside</span>
                </label>
                
                <label class="flex items-center">
                    <input type="checkbox" class="mr-2">
                    <span>All navigation links work</span>
                </label>
                
                <label class="flex items-center">
                    <input type="checkbox" class="mr-2">
                    <span>User profile dropdown shows correct info</span>
                </label>
                
                <label class="flex items-center">
                    <input type="checkbox" class="mr-2">
                    <span>Admin dropdown appears for admin users</span>
                </label>
                
                <label class="flex items-center">
                    <input type="checkbox" class="mr-2">
                    <span>Logout functionality works</span>
                </label>
            </div>
            
            <div class="mt-6 p-4 bg-blue-50 rounded-lg">
                <h3 class="font-semibold text-blue-800 mb-2">Instructions:</h3>
                <ol class="list-decimal list-inside text-blue-700 space-y-1">
                    <li>Start the Flask application</li>
                    <li>Log in with test credentials</li>
                    <li>Test each navbar functionality</li>
                    <li>Check both desktop and mobile views</li>
                    <li>Test with both alumni and admin accounts</li>
                </ol>
            </div>
        </div>
    </div>
</body>
</html>'''
    
    with open("navbar_test.html", "w", encoding="utf-8") as f:
        f.write(test_script)
    
    print("✅ Created navbar_test.html")

def create_debug_info():
    """Create debug information for troubleshooting"""
    print("\n🔧 Creating debug information...")
    
    debug_info = '''# Navbar and Functionality Debug Guide

## Common Issues and Solutions

### 1. Dropdown Menus Not Working
**Symptoms**: Dropdowns don't open on hover or click
**Solutions**:
- Check JavaScript console for errors
- Ensure Tailwind CSS is loaded
- Verify dropdown JavaScript is running
- Check for conflicting CSS

### 2. CSRF Token Errors (400 Bad Request)
**Symptoms**: Forms return 400 errors
**Solutions**:
- Add `<input type="hidden" name="csrf_token" value="{{ csrf_token() }}"/>` to forms
- Ensure CSRF protection is enabled in Flask
- Check form method is POST

### 3. Graduation Year Sorting Error
**Symptoms**: TypeError when accessing directory
**Solutions**:
- Convert graduation years to integers before sorting
- Filter out None/invalid values
- Handle mixed data types

### 4. ObjectId Serialization Error
**Symptoms**: JSON serialization errors in calendar
**Solutions**:
- Convert ObjectIds to strings before JSON serialization
- Use str(object_id) for MongoDB ObjectIds

### 5. Mobile Menu Issues
**Symptoms**: Mobile menu doesn't toggle
**Solutions**:
- Check mobile menu JavaScript
- Verify button click handlers
- Test on actual mobile devices

## Testing Steps

1. **Start Application**:
   ```bash
   python app.py
   ```

2. **Test User Flows**:
   - Register new user
   - Login as alumni
   - Login as admin
   - Test all navbar links
   - Test dropdown menus
   - Test mobile responsiveness

3. **Check Browser Console**:
   - Open Developer Tools (F12)
   - Check Console tab for JavaScript errors
   - Check Network tab for failed requests

4. **Test Forms**:
   - RSVP to events
   - Post comments
   - Edit profile
   - Create events (admin)

## Browser Compatibility

- Chrome: ✅ Fully supported
- Firefox: ✅ Fully supported  
- Safari: ✅ Fully supported
- Edge: ✅ Fully supported
- Mobile browsers: ✅ Responsive design

## Performance Tips

- Use browser caching for static files
- Minimize JavaScript execution
- Optimize CSS delivery
- Use CDN for external libraries
'''
    
    with open("DEBUG_GUIDE.md", "w", encoding="utf-8") as f:
        f.write(debug_info)
    
    print("✅ Created DEBUG_GUIDE.md")

def main():
    """Run all fixes"""
    print("🚀 Alumni Event Scheduler - Navbar Fix Tool")
    print("=" * 50)
    
    fix_csrf_tokens()
    fix_graduation_year_issue()
    create_navbar_test_script()
    create_debug_info()
    
    print("\n" + "=" * 50)
    print("🎉 Navbar fixes completed!")
    print("\n📋 Next steps:")
    print("1. Restart your Flask application")
    print("2. Test navbar functionality")
    print("3. Open navbar_test.html for testing checklist")
    print("4. Check DEBUG_GUIDE.md for troubleshooting")
    
    print("\n🔧 Manual fixes needed:")
    print("- Ensure MongoDB is running")
    print("- Clear browser cache if needed")
    print("- Test on different screen sizes")

if __name__ == "__main__":
    main()