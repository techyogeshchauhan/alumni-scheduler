#!/usr/bin/env python3
"""
Comprehensive test suite for Alumni Event Scheduler API
"""
import os
import sys
import json
import unittest
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from api import create_api_app
from config import TestingConfig
from models import UserModel, EventModel, RSVPModel

class TestAlumniEventSchedulerAPI(unittest.TestCase):
    """Test cases for the Alumni Event Scheduler API"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.app = create_api_app(TestingConfig)
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
        
        # Mock database
        self.mock_db = MagicMock()
        self.mock_users = MagicMock()
        self.mock_events = MagicMock()
        self.mock_rsvps = MagicMock()
        
        # Mock collections
        self.mock_db.users = self.mock_users
        self.mock_db.events = self.mock_events
        self.mock_db.rsvps = self.mock_rsvps
        
        # Mock user data
        self.test_user = {
            '_id': '507f1f77bcf86cd799439011',
            'name': 'Test User',
            'email': 'test@example.com',
            'password_hash': 'hashed_password',
            'role': 'alumni',
            'phone': '+1234567890',
            'preferences': {'email': True, 'sms': False, 'push': True},
            'created_at': datetime.utcnow(),
            'is_active': True
        }
        
        # Mock event data
        self.test_event = {
            '_id': '507f1f77bcf86cd799439012',
            'title': 'Test Event',
            'description': 'Test event description',
            'start_time': datetime.utcnow() + timedelta(days=7),
            'end_time': datetime.utcnow() + timedelta(days=7, hours=2),
            'venue': 'Test Venue',
            'capacity': 50,
            'timezone': 'UTC',
            'created_by': '507f1f77bcf86cd799439011',
            'created_at': datetime.utcnow()
        }
    
    def test_health_check(self):
        """Test health check endpoint"""
        response = self.client.get('/api/health')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('status', data)
        self.assertEqual(data['status'], 'healthy')
    
    def test_user_registration_success(self):
        """Test successful user registration"""
        with patch('api.user_model') as mock_user_model:
            mock_user_model.get_user_by_email.return_value = None
            mock_user_model.validate_user_data.return_value = []
            mock_user_model.create_user.return_value = self.test_user
            
            response = self.client.post('/api/auth/register', json={
                'name': 'Test User',
                'email': 'test@example.com',
                'password': 'TestPassword123!',
                'phone': '+1234567890',
                'role': 'alumni'
            })
            
            self.assertEqual(response.status_code, 201)
            data = json.loads(response.data)
            self.assertIn('access_token', data)
            self.assertIn('refresh_token', data)
            self.assertIn('user', data)
    
    def test_user_registration_duplicate_email(self):
        """Test user registration with duplicate email"""
        with patch('api.user_model') as mock_user_model:
            mock_user_model.get_user_by_email.return_value = self.test_user
            
            response = self.client.post('/api/auth/register', json={
                'name': 'Test User',
                'email': 'test@example.com',
                'password': 'TestPassword123!'
            })
            
            self.assertEqual(response.status_code, 409)
            data = json.loads(response.data)
            self.assertIn('message', data)
    
    def test_user_registration_weak_password(self):
        """Test user registration with weak password"""
        response = self.client.post('/api/auth/register', json={
            'name': 'Test User',
            'email': 'test@example.com',
            'password': 'weak'
        })
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('errors', data)
    
    def test_user_login_success(self):
        """Test successful user login"""
        with patch('api.user_model') as mock_user_model:
            mock_user_model.get_user_by_email.return_value = self.test_user
            mock_user_model.update_user.return_value = True
            
            with patch('api.check_password_hash', return_value=True):
                response = self.client.post('/api/auth/login', json={
                    'email': 'test@example.com',
                    'password': 'TestPassword123!'
                })
                
                self.assertEqual(response.status_code, 200)
                data = json.loads(response.data)
                self.assertIn('access_token', data)
                self.assertIn('refresh_token', data)
                self.assertIn('user', data)
    
    def test_user_login_invalid_credentials(self):
        """Test login with invalid credentials"""
        with patch('api.user_model') as mock_user_model:
            mock_user_model.get_user_by_email.return_value = None
            
            response = self.client.post('/api/auth/login', json={
                'email': 'test@example.com',
                'password': 'wrongpassword'
            })
            
            self.assertEqual(response.status_code, 401)
            data = json.loads(response.data)
            self.assertIn('message', data)
    
    def test_get_user_profile(self):
        """Test getting user profile"""
        with patch('api.user_model') as mock_user_model:
            mock_user_model.get_user_by_id.return_value = self.test_user
            
            with patch('api.get_current_user', return_value='507f1f77bcf86cd799439011'):
                response = self.client.get('/api/users/me')
                
                self.assertEqual(response.status_code, 200)
                data = json.loads(response.data)
                self.assertEqual(data['name'], 'Test User')
                self.assertEqual(data['email'], 'test@example.com')
    
    def test_update_user_profile(self):
        """Test updating user profile"""
        with patch('api.user_model') as mock_user_model:
            mock_user_model.get_user_by_id.return_value = self.test_user
            mock_user_model.update_user.return_value = True
            
            with patch('api.get_current_user', return_value='507f1f77bcf86cd799439011'):
                response = self.client.put('/api/users/me', json={
                    'name': 'Updated Name',
                    'phone': '+0987654321'
                })
                
                self.assertEqual(response.status_code, 200)
                data = json.loads(response.data)
                self.assertIn('message', data)
    
    def test_get_events_list(self):
        """Test getting events list"""
        with patch('api.event_model') as mock_event_model:
            mock_event_model.search_events.return_value = {
                'events': [self.test_event],
                'total': 1,
                'page': 1,
                'per_page': 10,
                'pages': 1
            }
            
            response = self.client.get('/api/events')
            
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertIn('events', data)
            self.assertEqual(len(data['events']), 1)
    
    def test_create_event_success(self):
        """Test successful event creation"""
        with patch('api.user_model') as mock_user_model:
            mock_user_model.get_user_by_id.return_value = self.test_user
            
            with patch('api.event_model') as mock_event_model:
                mock_event_model.validate_event_data.return_value = []
                mock_event_model.create_event.return_value = self.test_event
                
                with patch('api.require_admin', return_value=None):
                    with patch('api.get_current_user', return_value='507f1f77bcf86cd799439011'):
                        response = self.client.post('/api/events', json={
                            'title': 'Test Event',
                            'description': 'Test event description',
                            'start_time': (datetime.utcnow() + timedelta(days=7)).isoformat(),
                            'end_time': (datetime.utcnow() + timedelta(days=7, hours=2)).isoformat(),
                            'venue': 'Test Venue',
                            'capacity': 50,
                            'timezone': 'UTC'
                        })
                        
                        self.assertEqual(response.status_code, 201)
                        data = json.loads(response.data)
                        self.assertEqual(data['title'], 'Test Event')
    
    def test_create_event_validation_error(self):
        """Test event creation with validation error"""
        with patch('api.event_model') as mock_event_model:
            mock_event_model.validate_event_data.return_value = ['Invalid start time']
            
            with patch('api.require_admin', return_value=None):
                with patch('api.get_current_user', return_value='507f1f77bcf86cd799439011'):
                    response = self.client.post('/api/events', json={
                        'title': 'Test Event',
                        'description': 'Test event description',
                        'start_time': 'invalid-date',
                        'end_time': (datetime.utcnow() + timedelta(days=7, hours=2)).isoformat(),
                        'venue': 'Test Venue',
                        'capacity': 50
                    })
                    
                    self.assertEqual(response.status_code, 400)
                    data = json.loads(response.data)
                    self.assertIn('errors', data)
    
    def test_get_event_detail(self):
        """Test getting event detail"""
        with patch('api.event_model') as mock_event_model:
            mock_event_model.get_event_by_id.return_value = self.test_event
            
            response = self.client.get('/api/events/507f1f77bcf86cd799439012')
            
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertEqual(data['title'], 'Test Event')
    
    def test_get_event_not_found(self):
        """Test getting non-existent event"""
        with patch('api.event_model') as mock_event_model:
            mock_event_model.get_event_by_id.return_value = None
            
            response = self.client.get('/api/events/507f1f77bcf86cd799439012')
            
            self.assertEqual(response.status_code, 404)
            data = json.loads(response.data)
            self.assertIn('message', data)
    
    def test_create_rsvp_success(self):
        """Test successful RSVP creation"""
        with patch('api.event_model') as mock_event_model:
            mock_event_model.get_event_by_id.return_value = self.test_event
            
            with patch('api.rsvp_model') as mock_rsvp_model:
                mock_rsvp_model.get_rsvp_by_event_and_user.return_value = None
                mock_rsvp_model.create_rsvp.return_value = {
                    '_id': '507f1f77bcf86cd799439013',
                    'event_id': '507f1f77bcf86cd799439012',
                    'user_id': '507f1f77bcf86cd799439011',
                    'status': 'going',
                    'guests': 1,
                    'notes': '',
                    'created_at': datetime.utcnow()
                }
                
                with patch('api.get_current_user', return_value='507f1f77bcf86cd799439011'):
                    response = self.client.post('/api/events/507f1f77bcf86cd799439012/rsvp', json={
                        'status': 'going',
                        'guests': 1,
                        'notes': 'Looking forward to it!'
                    })
                    
                    self.assertEqual(response.status_code, 200)
                    data = json.loads(response.data)
                    self.assertIn('message', data)
                    self.assertEqual(data['status'], 'going')
    
    def test_create_rsvp_invalid_status(self):
        """Test RSVP creation with invalid status"""
        with patch('api.event_model') as mock_event_model:
            mock_event_model.get_event_by_id.return_value = self.test_event
            
            with patch('api.get_current_user', return_value='507f1f77bcf86cd799439011'):
                response = self.client.post('/api/events/507f1f77bcf86cd799439012/rsvp', json={
                    'status': 'invalid_status',
                    'guests': 1
                })
                
                self.assertEqual(response.status_code, 400)
                data = json.loads(response.data)
                self.assertIn('message', data)
    
    def test_get_rsvp_stats(self):
        """Test getting RSVP statistics"""
        with patch('api.rsvp_model') as mock_rsvp_model:
            mock_rsvp_model.get_rsvp_stats.return_value = {
                'going': 10,
                'maybe': 5,
                'not_going': 2,
                'waitlist': 0,
                'total_guests': 15
            }
            
            response = self.client.get('/api/events/507f1f77bcf86cd799439012/rsvp-stats')
            
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data)
            self.assertEqual(data['going'], 10)
            self.assertEqual(data['maybe'], 5)
            self.assertEqual(data['total_guests'], 15)
    
    def test_rate_limiting(self):
        """Test rate limiting on auth endpoints"""
        # This would require more complex setup with actual rate limiting
        # For now, we'll just test that the endpoint exists
        response = self.client.post('/api/auth/login', json={
            'email': 'test@example.com',
            'password': 'TestPassword123!'
        })
        
        # Should return 401 for invalid credentials, not rate limit error
        self.assertIn(response.status_code, [401, 429])
    
    def test_cors_headers(self):
        """Test CORS headers are present"""
        response = self.client.options('/api/events')
        self.assertIn('Access-Control-Allow-Origin', response.headers)
    
    def test_jwt_token_required(self):
        """Test that protected endpoints require JWT token"""
        response = self.client.get('/api/users/me')
        self.assertEqual(response.status_code, 401)
    
    def test_admin_required(self):
        """Test that admin endpoints require admin role"""
        with patch('api.get_current_user', return_value='507f1f77bcf86cd799439011'):
            with patch('api.user_model') as mock_user_model:
                mock_user_model.get_user_by_id.return_value = {
                    **self.test_user,
                    'role': 'alumni'  # Not admin
                }
                
                response = self.client.post('/api/events', json={
                    'title': 'Test Event',
                    'description': 'Test event description',
                    'start_time': (datetime.utcnow() + timedelta(days=7)).isoformat(),
                    'end_time': (datetime.utcnow() + timedelta(days=7, hours=2)).isoformat(),
                    'venue': 'Test Venue',
                    'capacity': 50
                })
                
                self.assertEqual(response.status_code, 403)
                data = json.loads(response.data)
                self.assertIn('message', data)

class TestNotificationSystem(unittest.TestCase):
    """Test cases for the notification system"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.app = create_api_app(TestingConfig)
        self.app.config['TESTING'] = True
    
    def test_notification_template_rendering(self):
        """Test notification template rendering"""
        from notifications import NotificationTemplate
        
        template_handler = NotificationTemplate()
        variables = {
            'user_name': 'John Doe',
            'event_title': 'Test Event',
            'start_time': '2024-01-01 10:00 AM',
            'venue': 'Test Venue'
        }
        
        subject = template_handler.render_template('event_created', 'subject', variables)
        self.assertIn('Test Event', subject)
        self.assertIn('New Alumni Event', subject)
    
    def test_email_notification_service(self):
        """Test email notification service"""
        from notifications import EmailNotificationService
        from config import TestingConfig
        
        service = EmailNotificationService(TestingConfig)
        
        # Test template email sending (mocked)
        with patch.object(service, 'send_email', return_value=True):
            result = service.send_template_email('test@example.com', 'event_created', {
                'user_name': 'Test User',
                'event_title': 'Test Event',
                'start_time': '2024-01-01 10:00 AM',
                'venue': 'Test Venue'
            })
            self.assertTrue(result)

class TestModels(unittest.TestCase):
    """Test cases for data models"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.mock_collection = MagicMock()
        self.user_model = UserModel(self.mock_collection)
    
    def test_user_validation(self):
        """Test user data validation"""
        valid_user = {
            'name': 'Test User',
            'email': 'test@example.com',
            'password_hash': 'hashed_password',
            'role': 'alumni'
        }
        
        errors = self.user_model.validate_user_data(valid_user)
        self.assertEqual(len(errors), 0)
    
    def test_user_validation_invalid_email(self):
        """Test user validation with invalid email"""
        invalid_user = {
            'name': 'Test User',
            'email': 'invalid-email',
            'password_hash': 'hashed_password',
            'role': 'alumni'
        }
        
        errors = self.user_model.validate_user_data(invalid_user)
        self.assertGreater(len(errors), 0)
        self.assertIn('Invalid email format', errors[0])
    
    def test_user_validation_invalid_role(self):
        """Test user validation with invalid role"""
        invalid_user = {
            'name': 'Test User',
            'email': 'test@example.com',
            'password_hash': 'hashed_password',
            'role': 'invalid_role'
        }
        
        errors = self.user_model.validate_user_data(invalid_user)
        self.assertGreater(len(errors), 0)
        self.assertIn('Role must be', errors[0])

def run_tests():
    """Run all tests"""
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add test cases
    test_suite.addTest(unittest.makeSuite(TestAlumniEventSchedulerAPI))
    test_suite.addTest(unittest.makeSuite(TestNotificationSystem))
    test_suite.addTest(unittest.makeSuite(TestModels))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Return success status
    return result.wasSuccessful()

if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
