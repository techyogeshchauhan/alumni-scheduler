#!/usr/bin/env python3
"""
Setup script for Alumni Event Scheduler
This script helps set up the application for development and production.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors."""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible."""
    print("🐍 Checking Python version...")
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        return False
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    return True

def create_virtual_environment():
    """Create a virtual environment."""
    if os.path.exists("venv"):
        print("📁 Virtual environment already exists")
        return True
    
    return run_command("python -m venv venv", "Creating virtual environment")

def install_dependencies():
    """Install Python dependencies."""
    if os.name == 'nt':  # Windows
        pip_cmd = "venv\\Scripts\\pip"
    else:  # Unix/Linux/MacOS
        pip_cmd = "venv/bin/pip"
    
    return run_command(f"{pip_cmd} install -r requirements.txt", "Installing dependencies")

def create_directories():
    """Create necessary directories."""
    print("📁 Creating directories...")
    directories = [
        "static/uploads",
        "logs",
        "static/uploads/events",
        "static/uploads/profiles"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✅ Created directory: {directory}")
    
    return True

def create_env_file():
    """Create .env file from template."""
    if os.path.exists(".env"):
        print("📄 .env file already exists")
        return True
    
    env_content = """# Flask Configuration
SECRET_KEY=your-secret-key-change-this-in-production
FLASK_ENV=development
FLASK_DEBUG=True

# MongoDB Configuration
MONGO_URI=mongodb://localhost:27017
MONGO_DB_NAME=alumni_db

# Email Configuration (Optional - for notifications)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password

# File Upload Configuration
UPLOAD_FOLDER=static/uploads
MAX_CONTENT_LENGTH=16777216

# Application Configuration
APP_NAME=Alumni Scheduler
APP_VERSION=1.0.0
ADMIN_EMAIL=admin@alumni-scheduler.com
"""
    
    try:
        with open(".env", "w") as f:
            f.write(env_content)
        print("✅ Created .env file from template")
        return True
    except Exception as e:
        print(f"❌ Failed to create .env file: {e}")
        return False

def check_mongodb():
    """Check if MongoDB is available."""
    print("🍃 Checking MongoDB connection...")
    try:
        from pymongo import MongoClient
        client = MongoClient("mongodb://localhost:27017", serverSelectionTimeoutMS=5000)
        client.server_info()
        print("✅ MongoDB connection successful")
        return True
    except Exception as e:
        print(f"⚠️  MongoDB connection failed: {e}")
        print("📝 Please ensure MongoDB is running on localhost:27017")
        print("   Or update MONGO_URI in .env file for remote MongoDB")
        return False

def create_sample_data():
    """Create sample data for testing."""
    print("📊 Creating sample data...")
    try:
        from pymongo import MongoClient
        from datetime import datetime, timedelta
        import hashlib
        
        client = MongoClient("mongodb://localhost:27017")
        db = client["alumni_db"]
        
        # Create sample admin user
        admin_user = {
            "email": "admin@alumni-scheduler.com",
            "password": hashlib.pbkdf2_hmac('sha256', b'admin123', b'salt', 100000).hex(),
            "name": "Admin User",
            "grad_year": 2020,
            "phone": "+1234567890",
            "is_admin": True,
            "is_active": True,
            "profile_picture": "",
            "preferences": {
                "email_notifications": True,
                "sms_notifications": False,
                "event_reminders": True
            },
            "created_at": datetime.now(),
            "last_login": None
        }
        
        # Insert admin user if not exists
        if not db.users.find_one({"email": "admin@alumni-scheduler.com"}):
            db.users.insert_one(admin_user)
            print("✅ Created sample admin user (email: admin@alumni-scheduler.com, password: admin123)")
        
        # Create sample events
        sample_events = [
            {
                "title": "Alumni Networking Mixer",
                "description": "Join us for an evening of networking and reconnecting with fellow alumni. Light refreshments will be served.",
                "date": datetime.now() + timedelta(days=7),
                "location": "University Alumni Center",
                "capacity": 50,
                "category": "Networking",
                "venue": {
                    "name": "Alumni Center",
                    "address": "123 University Ave, City, State 12345",
                    "phone": "+1234567890"
                },
                "tags": ["networking", "social", "professional"],
                "attachments": [],
                "created_by": db.users.find_one({"email": "admin@alumni-scheduler.com"})["_id"],
                "created_at": datetime.now(),
                "is_published": True,
                "rsvp_count": 0
            },
            {
                "title": "Homecoming Football Game",
                "description": "Cheer on our team at the annual homecoming football game. Tailgate party starts at 2 PM.",
                "date": datetime.now() + timedelta(days=14),
                "location": "University Stadium",
                "capacity": 1000,
                "category": "Sports",
                "venue": {
                    "name": "University Stadium",
                    "address": "456 Sports Blvd, City, State 12345",
                    "phone": "+1234567891"
                },
                "tags": ["sports", "homecoming", "tailgate"],
                "attachments": [],
                "created_by": db.users.find_one({"email": "admin@alumni-scheduler.com"})["_id"],
                "created_at": datetime.now(),
                "is_published": True,
                "rsvp_count": 0
            }
        ]
        
        for event in sample_events:
            if not db.events.find_one({"title": event["title"]}):
                db.events.insert_one(event)
        
        print("✅ Created sample events")
        print("🎉 Setup completed successfully!")
        print("\n📋 Next steps:")
        print("1. Start the application: python app.py")
        print("2. Open your browser: http://localhost:5000")
        print("3. Login with admin credentials: admin@alumni-scheduler.com / admin123")
        print("4. Create your first event or register new users")
        
        return True
        
    except Exception as e:
        print(f"⚠️  Could not create sample data: {e}")
        return False

def main():
    """Main setup function."""
    print("🚀 Alumni Event Scheduler Setup")
    print("=" * 40)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Create virtual environment
    if not create_virtual_environment():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        sys.exit(1)
    
    # Create directories
    if not create_directories():
        sys.exit(1)
    
    # Create .env file
    if not create_env_file():
        sys.exit(1)
    
    # Check MongoDB
    check_mongodb()
    
    # Create sample data
    create_sample_data()
    
    print("\n🎉 Setup completed!")
    print("\nTo start the application:")
    if os.name == 'nt':  # Windows
        print("venv\\Scripts\\python app.py")
    else:  # Unix/Linux/MacOS
        print("venv/bin/python app.py")
        print("or")
        print("source venv/bin/activate && python app.py")

if __name__ == "__main__":
    main()
