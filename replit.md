# Tamil Nadu State Board – Question Papers & Answer Keys Portal

## Overview

A comprehensive web portal designed for Tamil Nadu State Board students (Class 9-12) to access and download previous year question papers and answer keys. The system follows a strict hierarchy: Class → Subject → Exam Type → Year.

## System Architecture

### Backend Architecture
- **Framework**: Flask 3.0+
- **Data Storage**: JSON-based storage (`data.json`)
- **Database**: SQLite (SQLAlchemy) for user management and structured metadata
- **File Storage**: Local filesystem in `uploads/` directory

### Hierarchical Navigation
1. **Class**: 9th, 10th, 11th, 12th
2. **Subject**: Tamil, English, Maths, Science, Social Science, etc.
3. **Exam Type**: Unit Test 1-3, Quarterly, Half-Yearly, Revision, Practical, Annual
4. **Year**: Academic year of the exam

## Key Components
- **Admin Portal**: Secret route for uploading and managing materials.
- **Public Portal**: Download-only access for students.
- **Search**: Global search for quick access to papers.
