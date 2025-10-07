# Movie Ticket Booking System

A Django REST Framework based backend system for movie ticket booking with JWT authentication.

## Features

- User registration and login with JWT
- Movie and show management
- Seat booking with conflict prevention
- Booking cancellation
- User booking history
- Swagger API documentation

## Tech Stack

- Python 3.8+
- Django 4.2+
- Django REST Framework
- JWT Authentication
- SQLite (development)
- drf-yasg (Swagger documentation)

## Project Structure
movie-ticket-booking/
├── venv/ # Virtual environment
├── manage.py # Django management script
├── db.sqlite3 # Database (created after setup)
├── requirements.txt # Python dependencies
├── create_sample_data.py # Sample data script
├── README.md # This file
├── ticket_booking/ # Django project folder
│ ├── init.py
│ ├── settings.py
│ ├── urls.py
│ └── wsgi.py
└── booking/ # Django app folder
├── init.py
├── admin.py
├── apps.py
├── models.py
├── views.py
├── serializers.py
├── urls.py
└── migrations/
└── init.py


## 🚀 Complete Setup & Running Guide

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Step 1: Project Setup

```
# Navigate to your project directory
cd movie-ticket-booking

# Create virtual environment (if not already created)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Database Setup & Migrations
```
# Create database migrations
python manage.py makemigrations

# Apply migrations to database
python manage.py migrate
```

### Step 3: Create Superuser (Admin Access)
```
python manage.py createsuperuser
Follow the prompts:

Username: admin
Email address: admin@example.com
Password: ********
Password (again): ********
Superuser created successfully.
```

### Step 4: Create Sample Data
```
python create_sample_data.py
```

### Step 5: Run the Development Server
```
python manage.py runserver
```

### Step 6: Verify Server is Running
Open your web browser and visit these URLs:

Admin Panel: http://localhost:8000/admin/

Login with superuser credentials

You should see Movies, Shows, and Bookings

Swagger API Documentation: http://localhost:8000/swagger/

You should see all API endpoints documented

ReDoc Documentation: http://localhost:8000/redoc/

Alternative API documentation

### 📖 API Usage Guide
1. User Registration
Endpoint: POST http://localhost:8000/api/signup/

Request Body:

```
{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "securepassword123",
  "first_name": "John",
  "last_name": "Doe"
}
```
Response:

```
{
  "user": {
    "username": "john_doe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe"
  },
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

2. User Login
Endpoint: POST http://localhost:8000/api/login/

Request Body:

```
{
  "username": "john_doe",
  "password": "securepassword123"
}
```
Response:

```
{
  "user": {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com"
  },
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

3. Using JWT Token
Add the token to your request headers:

Authorization: Bearer <your_access_token>
Example using curl:

```
curl -H "Authorization: Bearer your_access_token_here" http://localhost:8000/api/movies/
```

4. Available Endpoints
Method	Endpoint	Description	Authentication
POST	/api/signup/	User registration	No
POST	/api/login/	User login	No
GET	/api/movies/	List all movies	No
GET	/api/movies/{id}/shows/	List shows for a movie	No
POST	/api/shows/{id}/book/	Book a seat	Yes
POST	/api/bookings/{id}/cancel/	Cancel a booking	Yes
GET	/api/my-bookings/	Get user's bookings	Yes

5. Complete API Flow Example
```
# 1. Register a new user
curl -X POST http://localhost:8000/api/signup/ \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "email": "test@example.com", "password": "testpass123", "first_name": "Test", "last_name": "User"}'

# 2. Login to get JWT token
curl -X POST http://localhost:8000/api/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "testpass123"}'

# 3. View all movies (no auth required)
curl http://localhost:8000/api/movies/

# 4. View shows for a movie (replace {id} with actual movie ID)
curl http://localhost:8000/api/movies/1/shows/

# 5. Book a seat (replace {id} with show ID and use your token)
curl -X POST http://localhost:8000/api/shows/1/book/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{"seat_number": 5}'

# 6. View your bookings
curl http://localhost:8000/api/my-bookings/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"

# 7. Cancel a booking (replace {id} with booking ID)
curl -X POST http://localhost:8000/api/bookings/1/cancel/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### 🛠️ Testing with Swagger UI
Open Swagger: Go to http://localhost:8000/swagger/

Get JWT Token:

Use /api/login/ endpoint to get your token

Copy the access token from response

Authorize:

Click "Authorize" button

Enter: Bearer your_token_here

Click "Authorize"

Test Endpoints:

All protected endpoints will now work

Try booking seats, viewing bookings, etc.

### For Testing (Command Prompt)
# Test 1: User Registration
```
curl -X POST http://localhost:8000/api/signup/ -H "Content-Type: application/json" -d "{\"username\": \"testuser\", \"email\": \"test@example.com\", \"password\": \"testpass123\", \"first_name\": \"Test\", \"last_name\": \"User\"}"
```
Response:
```
{"user":{"username":"testuser","email":"test@example.com","first_name":"Test","last_name":"User"},"refresh":"eyJh.....","access":"eyJh....."}
```
# Test 2: User Login
```
curl -X POST http://localhost:8000/api/login/ -H "Content-Type: application/json" -d "{\"username\": \"testuser\", \"password\": \"testpass123\"}"
```
Response:
```
{
    "refresh": "eyJhbGci...",
    "access": "eyJhbGci..."
}
```
# Test the Health Check Endpoint
```
curl http://localhost:8000/api/health/
```
Response:
```
{"status": "success", "message": "API is working!"}
```
