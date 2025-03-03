# Football Stadium Booking API

## Overview
Football Stadium Booking API is a Fast API that allows users to book football fields, view available fields, and manage bookings. The system supports three roles: Admin, Field Owners, and Users, each with different permissions.

## Features
### Admin
- Full control over the system

### Field Owners
- Add, edit, and delete football stadiums
- View and manage bookings for their stadiums

### Users
- View the list of football stadiums
- Filter stadiums by available time slots
- Sort stadiums by proximity to their location
- View stadium details
- Book a stadium

## Technologies Used
- **Django Rest Framework (DRF)** - For building the REST API
- **PostgreSQL** - Database for storing stadium and booking information
- **JWT Authentication** - Secure authentication for users
- **GeoDjango** - For handling geographic data (optional)

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/football-booking-api.git
   cd football-booking-api
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   ```bash
   cp .env.example .env
   ```
   Update `.env` file with necessary configurations.

5. Apply database migrations:
   ```bash
   python manage.py migrate
   ```

6. Create a superuser (admin):
   ```bash
   python manage.py createsuperuser
   ```

7. Start the server:
   ```bash
   python manage.py runserver
   ```

## API Endpoints
| Method | Endpoint | Description |
|--------|----------|--------------|
| POST | `/api/auth/register/` | Register a new user |
| POST | `/api/auth/login/` | Log in and get JWT token |
| GET | `/api/stadiums/` | List all stadiums (with filtering options) |
| GET | `/api/stadiums/<id>/` | Get stadium details |
| POST | `/api/stadiums/` | Create a stadium (owner only) |
| PUT | `/api/stadiums/<id>/` | Update stadium details (owner only) |
| DELETE | `/api/stadiums/<id>/` | Delete a stadium (owner only) |
| GET | `/api/bookings/` | List all bookings (owner only) |
| POST | `/api/bookings/` | Book a stadium (user only) |
| DELETE | `/api/bookings/<id>/` | Cancel a booking (owner only) |

## Filtering and Sorting
- Users can filter stadiums based on availability.
- Stadiums can be sorted based on proximity to the user’s location.

## Authentication & Authorization
- Uses **JWT authentication** for secure access.
- Role-based permissions are enforced in the API.

## Contribution
1. Fork the repository
2. Create a new branch: `git checkout -b feature-branch`
3. Make changes and commit: `git commit -m 'Add new feature'`
4. Push to GitHub: `git push origin feature-branch`
5. Open a Pull Request

