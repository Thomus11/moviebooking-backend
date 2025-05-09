# 🎬 Movie Cinema Booking System API

A full-featured RESTful API for a movie cinema booking platform built with **Flask**, **SQLAlchemy**, **JWT Authentication**, **Cloudinary**, and **Resend.io**. This system enables users to explore movies, book showtimes, reserve seats, and receive email confirmations. Admins can manage content and view analytics.

---

📦 Dependencies & Imports

from flask import Flask, request, jsonify
Core Flask modules:
  Flask: Web framework
  request: Access incoming HTTP requests
  jsonify: Convert Python objects to JSON responses

from flask_sqlalchemy import SQLAlchemy
ORM for interacting with the database using Python classes instead of raw SQL.


from models import db, User, Movie, Showtime, Seat, Reservation
Importing data models (User, Movie, Showtime, etc.) defined in models.py.

from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
JWT (JSON Web Token) utilities:
JWTManager: Manages token-based authentication
create_access_token: Generates secure tokens after login
jwt_required: Protects endpoints from unauthorized access
get_jwt_identity: Retrieves user ID from the token



from resend.emails._emails import Emails
 Integration with Resend.io for sending reservation confirmation emails.


import cloudinary
   import cloudinary.uploader
   For uploading movie posters to Cloudinary , a cloud-based media storage solution.

from datetime import timedelta, datetime
   Used for handling time durations and timestamps.

from humanize import naturaltime
   useful for formatting timestamps like “2 hours ago”.


from dotenv import load_dotenv
import os
import re  # For manual email validation
load_dotenv: Loads configuration from .env file
os: Interact with operating system (e.g., environment variables)
re: Regular expressions for validating email formats


⚙️ Environment Setup
  load_dotenv()
  Load environment variables from .env file.

app = Flask(__name__)
Initialize the Flask application.

App Configuration
  app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cinema.db'
  Use SQLite as the default database. Stores data in cinema.db.

app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
app.config['RESEND_API_KEY'] = os.getenv('RESEND_API_KEY')
app.config['CLOUDINARY_CLOUD_NAME'] = os.getenv('CLOUDINARY_CLOUD_NAME')
app.config['CLOUDINARY_API_KEY'] = os.getenv('CLOUDINARY_API_KEY')
app.config['CLOUDINARY_API_SECRET'] = os.getenv('CLOUDINARY_API_SECRET')


Keys and credentials loaded from environment variables for security.

  app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
  Sets JWT token expiration to 1 hour.

🧱 Initialize Extensions
  db.init_app(app)


Initializes the SQLAlchemy ORM with the Flask app.
  jwt = JWTManager(app)
Initializes JWT manager for token handling





## 📦 Features

### 🔐 Authentication & Authorization
- JWT-based registration and login system.
- Role-based access (Admin / User).
- Admin promotion and content management.

### 🎥 Movie Management
- Add, update, delete, and list movies.
- Cloudinary integration for poster uploads.
- Search movies by title or genre.

### 🕒 Showtimes & Seat Reservation
- Admins can schedule showtimes per movie.
- Dynamic seat maps with booking and cancellation.
- Prevent double bookings.
- Email confirmation sent via Resend.io after reservation.

### 📊 Admin Dashboard & Reports
- Track total reservations.
- View capacity utilization per showtime.
- Estimate revenue ($10 per seat by default).

### 🔍 Search & Filter
- Search by movie genre/title.
- Filter showtimes by date.

### ⚠️ Robust Error Handling
- Centralized error responses (400, 404, 500).
- Input validation with clear messages.

---

## 🛠️ Technologies Used

| Technology           | Description                             |
|----------------------|-----------------------------------------|
| **Flask**            | Python web framework                    |
| **Flask-SQLAlchemy** | ORM for database modeling               |
| **JWT**              | Authentication and authorization        |
| **Cloudinary**       | Image storage for posters               |
| **Resend.io**        | Email service for confirmations         |
| **SQLite**           | Lightweight dev database                |
| **dotenv**           | Environment variable management         |
| **Regex**            | Email format validation                 |
| **Humanize (optional)** | Timestamp formatting               |

---

## 🧩 API Endpoints Overview

| Method | Endpoint                         | Description                          | Auth Required     |
|--------|----------------------------------|--------------------------------------|-------------------|
| POST   | `/register`                      | Register a new user                  | ❌                |
| POST   | `/login`                         | Login and get JWT token              | ❌                |
| POST   | `/users/promote/<id>`           | Promote a user to admin              | ✅ (Admin only)    |
| POST   | `/movies`                        | Create a new movie                   | ✅ (Admin only)    |
| GET    | `/movies`                        | List all movies                      | ✅                |
| GET    | `/movies/search`                | Search by title or genre             | ✅                |
| PUT    | `/movies/<id>`                  | Update a movie                       | ✅ (Admin only)    |
| DELETE | `/movies/<id>`                  | Delete a movie                       | ✅ (Admin only)    |
| POST   | `/upload-poster`               | Upload movie poster to Cloudinary   | ✅ (Admin only)    |
| POST   | `/showtimes`                    | Schedule new showtime                | ✅ (Admin only)    |
| GET    | `/showtimes/search`            | Search showtimes by date             | ✅                |
| POST   | `/seats`                         | Add seats to showtime                | ✅ (Admin only)    |
| POST   | `/reservations`                | Reserve one or more seats            | ✅                |
| DELETE | `/reservations/<id>`           | Cancel a reservation                 | ✅ (Owner only)    |
| GET    | `/admin/report`                | Admin analytics dashboard            | ✅ (Admin only)    |

1:POST /register
Request Body: {
  "username": "john_doe",
  "email": "john@example.com",
  "password": "password123"
}
Response; {
  "message": "User registered successfully",
  "user": {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "is_admin": false
  }
}

2:Post/login
Request Body: {
  "username": "john_doe",
  "password": "password123"
}
Response; {
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUz...",
  "user": {
    "id": 1,
    "username": "john_doe",
    "is_admin": false
  }
}

3: Promote User to Admin
POST /users/promote/<user_id>
Auth: Admin Only
Response
{
  "message": "User promoted to admin successfully"
}

4:🎥 Movie Endpoints
✅ Create Movie
POST /movies
Auth: Admin Only

Request
{
  "title": "Inception",
  "genre": "Sci-Fi",
  "description": "A thief who steals corporate secrets...",
  "poster_url": "https://res.cloudinary.com/.../inception.jpg"
}
Response
{
  "id": 5,
  "title": "Inception",
  "genre": "Sci-Fi",
  "description": "A thief who steals corporate secrets...",
  "poster_url": "https://res.cloudinary.com/.../inception.jpg"
}


5:🔍 Search Movies
GET /movies/search?title=inception

Response
[
  {
    "id": 5,
    "title": "Inception",
    "genre": "Sci-Fi",
    "poster_url": "https://res.cloudinary.com/.../inception.jpg"
  }
]

6:🕒 Showtimes
✅ Schedule Showtime
POST /showtimes
Auth: Admin Only

Request
{
  "movie_id": 5,
  "start_time": "2025-05-01T18:00:00"
}
Response
{
  "id": 3,
  "movie_title": "Inception",
  "start_time": "2025-05-01T18:00:00"
}
7:🪑 Seat Reservation
✅ Add Seats
POST /seats
Auth: Admin Only

Request
{
  "showtime_id": 3,
  "seats": ["A1", "A2", "A3"]
}

Response
{
  "message": "Seats added successfully",
  "seats": ["A1", "A2", "A3"]
}
8:✅ Make Reservation
POST /reservations
Auth: User

Request
{
  "showtime_id": 3,
  "seats": ["A1", "A2"]
}

Response
{
  "message": "Reservation confirmed",
  "reservation": {
    "id": 10,
    "showtime_id": 3,
    "user_id": 1,
    "seats": ["A1", "A2"],
    "total_price": 20
  }
}

9:❌ Cancel Reservation
DELETE /reservations/10
Auth: User (Owner only)

Response
{
  "message": "Reservation cancelled successfully"
}
10📊 Admin Report
GET /admin/report
Auth: Admin Only

Response
{
  "total_reservations": 50,
  "tickets_sold": 120,
  "revenue_estimate": 1200
}
11:📤 Upload Poster
POST /upload-poster
Auth: Admin Only

Request
{
  "image": "base64_or_multipart_file_data"
}

Response
{
  "url": "https://res.cloudinary.com/your_cloud/image/upload/filename.jpg"
}

12📧 Email Confirmation Example
Upon successful booking, users receive a Resend.io confirmation email:

Example Content
Hello John,

Your booking is confirmed:
🎬 Movie: Inception  
🕒 Showtime: 2025-05-01 18:00  
🪑 Seats: A1, A2

Enjoy your movie!


## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://Thomus11/movie-cinema-api.git
cd movie-cinema-api

### 2 set up the environment

''bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
# OR
       venv\Scripts\activate     # Windows

3. Install Dependencies
'''bash
pip install -r requirements.txt

4. Run the App
'''bash
python app.py
✔️ The server will start on port 5500:
👉 http://localhost:5500

Use tools like Postman , Thunder Client , or curl to test endpoints.

👨‍💻 Contributing
Contributions are welcome!

Fork the repo.
Create a feature branch (feature/new-feature-name).
Commit your changes.
Push to your fork.
Open a pull request.
📞 Contact
''''''For questions or support, reach out at mainathomas827@gmail.com
