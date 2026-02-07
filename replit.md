# TN State Board Portal

## Overview
A Tamil Nadu State Board Question Papers & Answer Keys Portal built with Flask. Students can browse question papers organized by class (9, 10, 11, 12), subject, and exam type. Admins can upload and manage files.

## Recent Changes
- 2026-02-07: Completed project import to Replit environment. Set up PostgreSQL database, installed dependencies, configured workflow.

## Project Architecture
- **Framework**: Flask (Python 3.11)
- **Database**: PostgreSQL via SQLAlchemy ORM
- **Server**: Gunicorn on port 5000
- **Templates**: Jinja2 (in `templates/`)
- **Static Assets**: CSS and JS (in `static/`)

### Key Files
- `app.py` - Main application with routes, admin login, file upload/download
- `models.py` - Database models (Subject, File, Comment, User)
- `main.py` - Entry point for gunicorn
- `templates/` - HTML templates (base, index, class_view, subject_view, etc.)
- `static/` - CSS and JavaScript files
- `uploads/` - Uploaded files directory

### Features
- Browse question papers by Class > Subject > Exam Type
- Admin panel (session-based auth) for file management
- File upload with metadata (class, subject, exam type, year)
- Search functionality
- Like/dislike and comment system on files
- File visibility toggle for admins

## User Preferences
- None recorded yet
