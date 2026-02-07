# TN Board Portal

## Overview
A Flask web application for Tamil Nadu Board exam portal. It allows browsing classes (9-12), subjects, exam types, and downloading question papers. Includes admin functionality for uploading and managing files.

## Recent Changes
- 2026-02-07: Initial migration to Replit environment completed
- Installed all Python dependencies (Flask, SQLAlchemy, gunicorn, etc.)
- PostgreSQL database created and connected
- Deployment configured with gunicorn on autoscale

## Project Architecture
- **Framework**: Flask (Python 3.11)
- **Database**: PostgreSQL via SQLAlchemy ORM
- **Server**: Gunicorn (WSGI)
- **Templates**: Jinja2 (in `templates/` directory)

### Key Files
- `main.py` - Entry point
- `app.py` - Flask app configuration, routes, and logic
- `models.py` - SQLAlchemy models (Subject, File, User)
- `templates/` - HTML templates
- `uploads/` - Uploaded files directory

### Models
- **Subject**: Board exam subjects with class levels
- **File**: Uploaded question papers/documents
- **User**: Admin users for content management

### Routes
- `/` - Homepage with class listing
- `/class-<id>` - Class view with subjects
- `/class-<id>/<subject>` - Subject view with exam categories
- `/upload` - Admin file upload
- `/search` - Search functionality
- `/admin` - Admin login (configurable path via ADMIN_SECRET_PATH env var)

## User Preferences
- None recorded yet
