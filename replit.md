# College Materials & PYQs Portal

## Overview

A comprehensive Flask-based web portal designed for college students to upload, organize, and download study materials, previous year question papers (PYQs), and academic resources. The application features a hierarchical navigation system organized by course types (UG/PG/MBA), departments, semesters, and categories.

## System Architecture

### Backend Architecture
- **Framework**: Flask 3.0+ (Python web framework)
- **Data Storage**: JSON-based file storage system with `data.json` as the primary data store
- **File Storage**: Local filesystem with organized directory structure in `uploads/` folder
- **Session Management**: Flask's built-in session handling with configurable secret key
- **Web Server**: Gunicorn WSGI server for production deployment

### Frontend Architecture
- **CSS Framework**: Bootstrap 5.3 for responsive design
- **Icons**: Font Awesome 6.4 for consistent iconography
- **JavaScript**: Vanilla JavaScript for client-side functionality
- **Template Engine**: Jinja2 (Flask's default templating engine)
- **UI Components**: Card-based layout with table and card view toggles

### Key Architectural Decisions
1. **JSON over Database**: Chosen for simplicity and rapid prototyping, avoiding database setup complexity
2. **File-based Storage**: Direct filesystem storage for uploaded files with secure filename handling
3. **Hierarchical Navigation**: Multi-level navigation structure (Course Type → Department → Semester → Category → Files)
4. **Responsive Design**: Mobile-first approach using Bootstrap's grid system

## Key Components

### Core Application Structure
- **Main Application** (`app.py`): Primary Flask application with all route handlers
- **Entry Point** (`main.py`): Application startup script for development
- **Data Models** (`models.py`): SQLAlchemy models (prepared for potential database migration)
- **Configuration**: Environment-based configuration with development defaults

### Navigation Hierarchy
1. **Course Types**: UG (8 semesters), PG (4 semesters), MBA (4 semesters), 5-year programs (10 semesters)
2. **Departments**: CSE, MECH, EEE, ECE, IT, CHEM, CIVIL, various PG specializations
3. **Categories**: CAT, ESE, SAT, Practical files for academic assessments
4. **File Management**: Upload, view, download, and delete functionality

### Calculator Suite
- **GPA Calculator**: Single semester grade point calculation
- **CGPA Calculator**: Multi-semester cumulative grade calculation  
- **Percentage Calculator**: GPA/CGPA to percentage conversion
- **Internal Marks Calculator**: CAT, SAT, assignment, and viva mark processing

## Data Flow

### File Upload Process
1. User selects course type, department, semester, category, and subject
2. File validation and secure filename generation using Werkzeug
3. File stored in organized directory structure: `uploads/[course]/[dept]/[semester]/[category]/`
4. Metadata stored in `data.json` with file paths and details

### Navigation Flow
1. Home → Course Types (UG/PG/MBA)
2. Course Type → Departments (CSE, MECH, etc.)
3. Department → Semesters (1-8 for UG, 1-4 for PG/MBA)
4. Semester → Categories (CAT, ESE, SAT, Practical)
5. Category → File listing with download/view options

### Calculator Data Flow
1. Form input validation on client-side
2. Grade/credit calculations using predefined mappings
3. Real-time result display with detailed breakdown tables
4. Local storage for preserving user input across sessions

## External Dependencies

### Python Dependencies
- **Flask**: Web framework and routing
- **Werkzeug**: File upload security and utilities
- **Gunicorn**: Production WSGI server
- **Optional**: SQLAlchemy, psycopg2-binary (prepared for database migration)

### Frontend Dependencies
- **Bootstrap 5.3**: CSS framework loaded via CDN
- **Font Awesome 6.4**: Icon library via CDN
- **No build process**: Direct HTML/CSS/JS approach for simplicity

### Development Environment
- **Replit Configuration**: Multi-language support (Python 3.11, Node.js 20, web modules)
- **Nix Packages**: System-level dependencies for image processing and multimedia support

## Deployment Strategy

### Current Deployment
- **Platform**: Replit with autoscale deployment target
- **Server**: Gunicorn binding to 0.0.0.0:5000
- **Port Mapping**: Internal 5000 → External 80
- **Process Management**: Replit workflows with automatic restart and reload capabilities

### Production Considerations
- **Database Migration**: Prepared SQLAlchemy models for PostgreSQL migration
- **File Storage**: Current local storage can be migrated to cloud storage (AWS S3, etc.)
- **Environment Variables**: Session secret and database URL configuration
- **Scaling**: Stateless design allows horizontal scaling with shared storage

### Security Measures
- **File Upload**: Werkzeug secure filename handling
- **Input Validation**: Form validation for all user inputs
- **Session Security**: Configurable secret key for session management
- **No File Size Limits**: Currently unrestricted (configurable for production)

## Changelog

- June 19, 2025. Initial setup
- June 19, 2025. Fixed file upload validation and department key normalization
- June 19, 2025. Added drag-and-drop interface with URL parameter auto-filling
- June 19, 2025. Resolved "Department not found" issue by normalizing data keys
- June 19, 2025. Fixed case-insensitive file matching in category routes
- June 19, 2025. Created consolidated requirements file combining all dependencies
- June 20, 2025. Project cleanup for GitHub deployment - removed unnecessary files, cleared uploaded files, created .gitignore, finalized requirements.txt
- June 20, 2025. Enhanced portal functionality - fixed delete functionality with proper file and database cleanup, improved upload form with auto-fill from URL parameters, added loading states and toast notifications for better user experience
- June 20, 2025. Implemented comprehensive smart search functionality - added dedicated search page with live filtering, advanced filters (course type, department, semester, category), responsive design with table/card views, and integrated search access throughout the portal
- June 20, 2025. Built JSON-based global search system - created modular search component for question papers and syllabus pages, implemented live filtering with highlighting, added delete functionality from search results, fully responsive design without database dependency
- June 20, 2025. Enhanced search UX - made search component collapsible by default, added to all upload pages, integrated search links in navigation and upload areas, search expands only when user clicks the search box
- June 20, 2025. Added social features - implemented like/dislike buttons with vote tracking, collapsible comment system with name and timestamp, optional file descriptions during upload, share button with clipboard copy functionality, all data stored in JSON without database dependency
- June 25, 2025. Implemented file detail view system - removed direct download buttons from file lists, created clickable file cards that open dedicated detail pages with file preview (PDF/images), description display, social features (likes/comments), and download/share actions, mobile-friendly design
- June 25, 2025. Enhanced file upload and preview system - added optional description field for uploads, improved file preview with PDF iframe, image display, DOCX preview via Microsoft Office Online, and text file preview with truncation
- June 25, 2025. Added comprehensive community discussion system - created dedicated community page with discussion creation, reply functionality, mobile-friendly design, all data stored in community.json without database dependency
- June 25, 2025. Enhanced file preview system with professional viewers - integrated PDF.js for interactive PDF viewing with zoom/navigation controls, improved Office Online Viewer for DOCX/PPT files with fallbacks, enhanced text file preview with syntax highlighting and word wrap toggle, secure file serving via send_from_directory
- June 25, 2025. Implemented Student Clubs management system - created clubs.json storage, admin-only club addition with image uploads, responsive card-based display, Instagram integration, secure file handling in uploads/clubs directory
- June 25, 2025. Completed Student Clubs feature integration - added clubs navigation link, updated homepage with Student Clubs section, implemented all CRUD operations with admin controls, secure file upload handling, mobile-responsive design consistent with portal styling
- June 26, 2025. Implemented comprehensive Bus Routes system - created transportation.json storage, admin-only upload functionality for PDF/image files, social features (like/dislike, comments, share), file detail views with preview capabilities, secure file serving, integrated navigation and homepage section
- June 30, 2025. Added Canteen management system - created canteen.json storage, admin upload panel with green '+ Add Canteen' button, responsive card display with static image sizing, delete functionality, secure photo serving via /canteen/photo/<filename>, integrated into navigation bar and homepage, follows same design patterns as Student Clubs and Bus Routes
- June 30, 2025. Implemented Campus Places system - created places.json storage for location data, manual place addition with name, description, photo upload, and Google Maps integration, responsive card display with static image sizing, clickable Google Maps links with copy functionality, delete controls, secure photo serving via /places/photo/<filename>, integrated into navigation and homepage
- June 30, 2025. Added Hostel Information system - created hostels.json storage, admin panel for adding hostel details with required name and photo, Boys/Girls category dropdown, optional description and Google Maps links, facilities checkboxes (Mess, Canteen, Wifi, Study Room, Sports Area, Gym), basic rules text area, responsive card display with category badges and facility icons, secure photo serving via /hostels/photo/<filename>, integrated into navigation and homepage
- June 30, 2025. Implemented Upcoming Events system - created events.json storage, admin panel for event management with required name, date, time and category fields, optional description, registration links, and poster uploads, category-based event classification (Tech Fest, Cultural Fest, Hackathon, Orientation, Induction, Entrance Exam, Others), automatic sorting by date with upcoming events first, registration link copying functionality, secure poster serving via /events/poster/<filename>, integrated into navigation and homepage
- July 1, 2025. Enhanced Community features - added like/dislike buttons to community replies with vote count display, implemented discussion sorting options (Latest First, Most Replies, Most Likes), updated community.json storage to include likes/dislikes for discussions and replies, added vote tracking functionality with AJAX updates, improved UI with hover effects and responsive vote buttons

## User Preferences

Preferred communication style: Simple, everyday language.