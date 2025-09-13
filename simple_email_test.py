#!/usr/bin/env python3
"""
Simple test for email functionality without Flask app context
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

def test_smtp_connection():
    """Test SMTP connection for email functionality"""
    print("🧪 Testing Email SMTP Connection...")
    
    # Email configuration (using Gmail as example)
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    
    # Check if email credentials are set
    email_username = os.getenv('MAIL_USERNAME', '')
    email_password = os.getenv('MAIL_PASSWORD', '')
    
    if not email_username or not email_password:
        print("❌ Email credentials not found in environment variables")
        print("   Please set MAIL_USERNAME and MAIL_PASSWORD in your .env file")
        return False
    
    print(f"📧 Testing connection to {smtp_server}:{smtp_port}")
    print(f"📧 Username: {email_username}")
    
    try:
        # Create SMTP connection
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()  # Enable TLS encryption
        server.login(email_username, email_password)
        
        print("✅ SMTP connection successful!")
        
        # Test sending a simple email
        msg = MIMEMultipart()
        msg['From'] = email_username
        msg['To'] = email_username  # Send to self for testing
        msg['Subject'] = "Test Email - Alumni Event Scheduler"
        
        body = """
        <h2>🎉 Email Test Successful!</h2>
        <p>This is a test email from the Alumni Event Scheduler system.</p>
        <p>If you receive this email, the email notification system is working correctly!</p>
        <p><strong>Features tested:</strong></p>
        <ul>
            <li>✅ SMTP connection</li>
            <li>✅ Email authentication</li>
            <li>✅ HTML email sending</li>
        </ul>
        <p>Best regards,<br>Alumni Event Scheduler System</p>
        """
        
        msg.attach(MIMEText(body, 'html'))
        
        # Send email
        text = msg.as_string()
        server.sendmail(email_username, email_username, text)
        
        print("✅ Test email sent successfully!")
        print(f"📧 Check your inbox at {email_username}")
        
        server.quit()
        return True
        
    except smtplib.SMTPAuthenticationError:
        print("❌ SMTP Authentication failed")
        print("   Please check your email credentials")
        return False
    except smtplib.SMTPException as e:
        print(f"❌ SMTP Error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def check_email_config():
    """Check email configuration"""
    print("\n📋 Email Configuration Check:")
    
    config_vars = [
        'MAIL_SERVER',
        'MAIL_PORT', 
        'MAIL_USERNAME',
        'MAIL_PASSWORD',
        'MAIL_USE_TLS'
    ]
    
    for var in config_vars:
        value = os.getenv(var, 'Not set')
        if var == 'MAIL_PASSWORD' and value != 'Not set':
            value = '*' * len(value)  # Hide password
        print(f"   {var}: {value}")

if __name__ == "__main__":
    print("🚀 Alumni Event Scheduler - Email Test")
    print("=" * 50)
    
    check_email_config()
    
    print("\n" + "=" * 50)
    success = test_smtp_connection()
    
    if success:
        print("\n🎉 Email system is ready!")
        print("   ✅ Event creation emails will be sent to selected alumni")
        print("   ✅ RSVP response emails will be sent to admins")
    else:
        print("\n⚠️  Email system needs configuration")
        print("   Please check your .env file and email settings")
