# College Materials & PYQs Portal

## Overview
A comprehensive web portal for college students to access and download previous year question papers, answer keys, and study materials. Supports UG, PG, and MBA course types with hierarchical navigation: Course Type -> Department -> Semester -> Category.

## Recent Changes
- 2026-02-07: Initial Replit setup - fixed data.json compatibility, database initialization, and deployment configuration.

## System Architecture

### Backend
- **Framework**: Flask 3.x (Python 3.11)
- **Database**: PostgreSQL (Neon-backed via Replit) for user management and structured metadata (subjects, files, users)
- **Data Storage**: JSON-based storage (`data.json`) for course hierarchy and file listings
- **File Storage**: Local filesystem in `uploads/` directory
- **ORM**: SQLAlchemy via Flask-SQLAlchemy

### Frontend
- Server-rendered HTML via Jinja2 templates
- Bootstrap CSS for styling
- Static files in `static/css/` and `static/js/`

### Key Files
- `main.py` - Entry point, runs Flask on 0.0.0.0:5000
- `app.py` - Flask application with all routes and business logic
- `models.py` - SQLAlchemy models (Subject, File, User)
- `init_db.py` - Database initialization and seeding script
- `data.json` - JSON data store for course hierarchy and file metadata
- `templates/` - Jinja2 HTML templates
- `static/` - CSS and JavaScript files

### Database Models
- **Subject**: Academic subjects with code, name, course_type, department, semester, category
- **File**: Uploaded files with metadata and subject associations
- **User**: Admin users for content management

### Admin Access
- Login route: `/admin` (configurable via ADMIN_SECRET_PATH env var)
- Default credentials: admin / admin123

## User Preferences
- No specific preferences recorded yet.
