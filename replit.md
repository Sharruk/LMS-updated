# TN State Board Portal

## Overview
A Tamil Nadu State Board Question Papers & Answer Keys Portal built with Flask. Students can browse question papers by class (9-12), subject, and exam type. Admins can upload/manage files and moderate comments.

## Recent Changes
- 2026-02-07: Completed project import to Replit environment. Installed dependencies, set up PostgreSQL database, configured workflow.

## Architecture
- **Backend**: Flask (Python 3.11) with SQLAlchemy ORM
- **Database**: PostgreSQL (Replit built-in)
- **Frontend**: Server-rendered templates (Jinja2) with Bootstrap
- **Server**: Gunicorn on port 5000

## Key Files
- `app.py` - Main Flask application with all routes
- `models.py` - SQLAlchemy models (Subject, File, Comment, User)
- `main.py` - Entry point for gunicorn
- `templates/` - Jinja2 HTML templates
- `static/` - CSS and JS assets
- `uploads/` - Uploaded files directory

## Features
- Browse classes 9-12 with subjects
- View exam categories (Unit Tests, Midterms, Quarterly, Half Yearly, Annual)
- File upload/download system
- Admin dashboard with file management
- Comment system on files
- Like/dislike voting
- Search functionality
