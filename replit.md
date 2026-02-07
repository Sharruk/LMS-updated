# Tamil Nadu State Board – Question Papers & Answer Keys Portal

## Overview
A comprehensive web portal for school students (Class 9-12) to access and download previous year question papers and answer keys. The system follows a strict hierarchy: Class -> Subject -> Exam Type.

## Recent Changes
- 2026-02-07: Refactored from College Portal to School Portal. Updated data structures to support Class-based navigation.
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
- `data.json` - JSON data store for class hierarchy and file metadata
- `templates/` - Jinja2 HTML templates
- `static/` - CSS and JavaScript files

### Database Models
- **Subject**: Academic subjects with code, name, class_level, category
- **File**: Uploaded files with metadata and subject associations
- **User**: Admin users for content management

### Admin Access
- Login route: `/admin` (configurable via ADMIN_SECRET_PATH env var)
- Default credentials: admin / admin123

## User Preferences
- No specific preferences recorded yet.
