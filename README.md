# Alumni Event Scheduler

A comprehensive, production-ready web application for managing alumni events, RSVPs, and community engagement. Built with Flask, MongoDB, and modern web technologies.

## 🚀 Features

### 🎯 Core Features
- **Advanced User Management**: JWT-based authentication, role-based access control, profile management
- **Comprehensive Event Management**: Rich event data with timezone support, RSVP deadlines, waitlist functionality
- **Enhanced RSVP System**: Guest tracking, dietary restrictions, RSVP history, waitlist management
- **Admin Dashboard**: Real-time analytics, user management, event oversight, data export
- **File Upload System**: Secure file handling for event attachments and profile pictures
- **Advanced Search & Filtering**: Full-text search, category filtering, date range filtering
- **Multi-Channel Notifications**: Email, SMS, and Push notifications with customizable templates

### 🔐 Security & Authentication
- **JWT Authentication**: Secure token-based authentication with refresh tokens
- **Password Security**: Configurable password complexity requirements
- **Rate Limiting**: Protection against brute force attacks
- **CORS Configuration**: Secure cross-origin resource sharing
- **Input Validation**: Comprehensive server-side validation and sanitization
- **XSS Protection**: Content sanitization and security headers

### 📱 Notification System
- **Email Notifications**: SendGrid integration with HTML templates
- **SMS Notifications**: Twilio integration for text messages
- **Push Notifications**: Firebase Cloud Messaging support
- **Scheduled Reminders**: Automated reminders (48h, 24h, 1h before events)
- **Template System**: Customizable notification templates with variables
- **Background Processing**: Celery-based asynchronous notification delivery

### 👥 User Roles & Permissions
- **Alumni**: View events, RSVP, manage profile, receive notifications
- **Administrators**: Full system access, user management, analytics, bulk operations

### 📊 Analytics & Reporting
- **Real-time Dashboard**: Live statistics and metrics
- **Event Analytics**: Attendance rates, popular events, user engagement
- **Export Functionality**: CSV export for RSVPs and user data
- **Data Visualization**: Charts and graphs for insights

### 🎨 Modern UI/UX
- **Responsive Design**: Mobile-first approach with Tailwind CSS
- **Interactive Components**: Smooth animations and hover effects
- **Accessibility**: WCAG AA compliant design patterns
- **Progressive Web App**: Offline capabilities and mobile optimization

## 🛠️ Installation & Setup

### Prerequisites
- **Python 3.10+** (recommended)
- **MongoDB 6.0+** (local or Atlas)
- **Redis 7.0+** (for background jobs)
- **Docker & Docker Compose** (for containerized deployment)

### Quick Start with Docker (Recommended)

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd alumni-scheduler
   ```

2. **Set up environment variables**
   ```bash
   cp env.example .env
   # Edit .env with your configuration
   ```

3. **Start all services**
   ```bash
   docker-compose up -d
   ```

4. **Access the application**
   - Web App: http://localhost:5000
   - API Documentation: http://localhost:5000/api/docs
   - Celery Flower (Monitoring): http://localhost:5555

### Manual Installation

#### Backend Setup

1. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   cp env.example .env
   # Edit .env with your configuration
   ```

4. **Start MongoDB and Redis**
   ```bash
   # MongoDB
   mongod --dbpath /path/to/your/db
   
   # Redis
   redis-server
   ```

5. **Run the application**
   ```bash
   # Start Flask app
   python app.py
   
   # Start Celery worker (in another terminal)
   celery -A celery_app worker --loglevel=info
   
   # Start Celery beat (in another terminal)
   celery -A celery_app beat --loglevel=info
   ```

#### Frontend Setup (Optional)

The application includes a complete HTML/CSS frontend. For React development:

1. **Install Node.js dependencies**
   ```bash
   cd frontend
   npm install
   ```

2. **Start the development server**
   ```bash
   npm start
   ```

### Environment Configuration

Key environment variables to configure:

```bash
# Database
MONGO_URI=mongodb://localhost:27017
MONGO_DB_NAME=alumni_db

# Redis
REDIS_URL=redis://localhost:6379/0

# Security
SECRET_KEY=your-secret-key-change-in-production
JWT_SECRET_KEY=your-jwt-secret-key-change-in-production

# Email (Choose one)
MAIL_SERVER=smtp.gmail.com
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password

# Or SendGrid
SENDGRID_API_KEY=your-sendgrid-api-key

# SMS (Optional)
TWILIO_SID=your-twilio-sid
TWILIO_AUTH_TOKEN=your-twilio-auth-token
TWILIO_PHONE_NUMBER=+1234567890

# Push Notifications (Optional)
FCM_SERVER_KEY=your-fcm-server-key
```

## Configuration

### Environment Variables

Create a `.env` file in the root directory with the following variables:

```env
# Flask Configuration
SECRET_KEY=your-secret-key-here
FLASK_ENV=development
FLASK_DEBUG=True

# MongoDB Configuration
MONGO_URI=mongodb://localhost:27017
MONGO_DB_NAME=alumni_db

# Email Configuration
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password

# File Upload Configuration
UPLOAD_FOLDER=static/uploads
MAX_CONTENT_LENGTH=16777216
```

### Email Setup

For email notifications to work:

1. **Gmail Setup**:
   - Enable 2-factor authentication
   - Generate an app password
   - Use the app password in `MAIL_PASSWORD`

2. **Other SMTP Servers**:
   - Update `MAIL_SERVER`, `MAIL_PORT`, and `MAIL_USE_TLS` accordingly

## Usage

### For Alumni Users

1. **Registration**: Create an account with your email and graduation year
2. **Profile Management**: Update your profile information and preferences
3. **Event Discovery**: Browse and search for events
4. **RSVP**: RSVP to events with guest counts and special requirements
5. **Notifications**: Receive email notifications for events and RSVPs

### For Administrators

1. **Dashboard**: View comprehensive statistics and analytics
2. **Event Management**: Create, edit, and manage events
3. **User Management**: View and manage user accounts
4. **Analytics**: Track event attendance and user engagement
5. **Notifications**: Send notifications to users

## 📚 API Documentation

### RESTful API Endpoints

The application provides a comprehensive REST API with JWT authentication.

#### Authentication Endpoints
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `POST /api/auth/refresh` - Refresh JWT token

#### User Management
- `GET /api/users/me` - Get current user profile
- `PUT /api/users/me` - Update user profile

#### Event Management
- `GET /api/events` - List events with search/filtering
- `GET /api/events/<id>` - Get event details
- `POST /api/events` - Create new event (Admin)
- `PUT /api/events/<id>` - Update event (Admin)
- `DELETE /api/events/<id>` - Delete event (Admin)

#### RSVP Management
- `POST /api/events/<id>/rsvp` - Submit/update RSVP
- `GET /api/events/<id>/rsvp` - Get RSVP list (Admin)
- `GET /api/events/<id>/rsvp-stats` - Get RSVP statistics

#### Health Check
- `GET /api/health` - API health status

### API Authentication

All protected endpoints require a JWT token in the Authorization header:

```bash
Authorization: Bearer <your-jwt-token>
```

### Example API Usage

#### Register a new user
```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "password": "SecurePass123!",
    "phone": "+1234567890"
  }'
```

#### Login
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "SecurePass123!"
  }'
```

#### Create an event (Admin)
```bash
curl -X POST http://localhost:5000/api/events \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <your-jwt-token>" \
  -d '{
    "title": "Alumni Reunion 2024",
    "description": "Annual alumni reunion event",
    "start_time": "2024-06-15T18:00:00Z",
    "end_time": "2024-06-15T22:00:00Z",
    "venue": "Grand Hotel Ballroom",
    "capacity": 100,
    "timezone": "UTC",
    "tags": ["reunion", "networking"]
  }'
```

#### RSVP to an event
```bash
curl -X POST http://localhost:5000/api/events/<event-id>/rsvp \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <your-jwt-token>" \
  -d '{
    "status": "going",
    "guests": 2,
    "notes": "Looking forward to it!"
  }'
```

## Database Schema

### Users Collection
```json
{
  "_id": "ObjectId",
  "email": "string",
  "password": "string (hashed)",
  "name": "string",
  "grad_year": "number",
  "phone": "string",
  "is_admin": "boolean",
  "is_active": "boolean",
  "profile_picture": "string",
  "preferences": {
    "email_notifications": "boolean",
    "sms_notifications": "boolean",
    "event_reminders": "boolean"
  },
  "created_at": "datetime",
  "last_login": "datetime"
}
```

### Events Collection
```json
{
  "_id": "ObjectId",
  "title": "string",
  "description": "string",
  "date": "datetime",
  "location": "string",
  "capacity": "number",
  "category": "string",
  "venue": {
    "name": "string",
    "address": "string",
    "phone": "string"
  },
  "tags": ["string"],
  "attachments": [{
    "filename": "string",
    "file_path": "string",
    "upload_date": "datetime"
  }],
  "created_by": "ObjectId",
  "created_at": "datetime",
  "is_published": "boolean",
  "rsvp_count": "number"
}
```

### RSVPs Collection
```json
{
  "_id": "ObjectId",
  "event_id": "ObjectId",
  "user_id": "ObjectId",
  "status": "string (Yes/No/Maybe)",
  "guest_count": "number",
  "dietary_restrictions": "string",
  "comments": "string",
  "rsvp_date": "datetime"
}
```

## Development

### Project Structure
```
alumni-scheduler/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── .env.example          # Environment variables template
├── static/               # Static files
│   ├── css/
│   │   └── styles.css    # Custom CSS
│   └── uploads/          # File uploads
└── templates/            # Jinja2 templates
    ├── base.html         # Base template
    ├── index.html        # Homepage
    ├── login.html        # Login page
    ├── register.html     # Registration page
    ├── profile.html      # User profile
    ├── edit_profile.html # Edit profile
    ├── events.html       # Events listing
    ├── event_detail.html # Event details
    ├── create_event.html # Create event
    ├── edit_event.html   # Edit event
    ├── admin_dashboard.html # Admin dashboard
    ├── admin_users.html  # User management
    └── admin_events.html # Event management
```

### Adding New Features

1. **New Routes**: Add routes in `app.py`
2. **New Templates**: Create templates in `templates/`
3. **New Static Files**: Add CSS/JS in `static/`
4. **Database Changes**: Update the schema documentation

### Testing

```bash
# Run the application in debug mode
python app.py

# Test with sample data
# The first registered user becomes an admin automatically
```

## Deployment

### Production Deployment

1. **Set up a production server**
2. **Install dependencies**
3. **Configure environment variables**
4. **Set up MongoDB**
5. **Configure a reverse proxy (nginx)**
6. **Set up SSL certificates**
7. **Configure email settings**

### Docker Deployment

```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "app.py"]
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions:
- Create an issue in the repository
- Contact the development team
- Check the documentation

## Changelog

### Version 1.0.0
- Initial release
- User authentication and management
- Event creation and management
- RSVP system
- Admin dashboard
- File upload support
- Email notifications
- Responsive design
