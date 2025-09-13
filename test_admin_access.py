#!/usr/bin/env python3
"""
Test admin access to various routes
"""

import requests
import sys

def test_admin_access():
    """Test admin access to routes"""
    base_url = "http://localhost:5000"
    
    # Routes that should be accessible to admin
    admin_routes = [
        "/profile",
        "/notifications", 
        "/profile/settings",
        "/directory",
        "/jobs",
        "/calendar",
        "/admin",
        "/admin/users",
        "/admin/events",
        "/admin/analytics"
    ]
    
    print("🧪 Testing Admin Route Access")
    print("=" * 40)
    print("Note: You need to be logged in as admin to test these routes")
    print("Login at: http://localhost:5000/admin/login")
    print("Test credentials: admin@alumni-event-scheduler.com / admin123")
    print()
    
    for route in admin_routes:
        try:
            url = f"{base_url}{route}"
            response = requests.get(url, timeout=5, allow_redirects=False)
            
            if response.status_code == 200:
                status = "✅ OK"
            elif response.status_code == 302:
                status = "🔄 Redirect (may need login)"
            elif response.status_code == 403:
                status = "❌ Forbidden"
            elif response.status_code == 404:
                status = "❌ Not Found"
            else:
                status = f"⚠️  {response.status_code}"
                
            print(f"{route:<20} {status}")
            
        except requests.exceptions.RequestException as e:
            print(f"{route:<20} ❌ Connection Error")
    
    print()
    print("Manual Testing Steps:")
    print("1. Start Flask app: python app.py")
    print("2. Login as admin: http://localhost:5000/admin/login")
    print("3. Test navbar dropdowns and links")
    print("4. Verify admin can access directory and jobs")

if __name__ == "__main__":
    test_admin_access()
