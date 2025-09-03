# College Materials & PYQs Portal

A comprehensive Flask-based web portal for college students to upload, organize, and download study materials, previous year question papers (PYQs), and academic resources.

## Features

- **Hierarchical Navigation**: Organized by Course Types (UG/PG/MBA) → Departments → Semesters → Categories
- **File Upload**: Drag-and-drop interface with all file type support
- **File Management**: Download and delete functionality with confirmation dialogs
- **Academic Calculators**: GPA, CGPA, Percentage, and Internal Marks calculators
- **Responsive Design**: Bootstrap 5 with mobile-first approach
- **Syllabus Management**: Separate section for curriculum documents

## Project Structure

```
├── app.py                 # Main Flask application
├── main.py               # Entry point
├── models.py             # Database models (PostgreSQL ready)
├── data.json             # JSON-based file storage
├── requirements.txt      # Python dependencies
├── templates/            # Jinja2 templates
│   ├── base.html
│   ├── index.html
│   ├── upload.html
│   ├── category.html
│   └── calculators/
├── static/              # CSS, JS, images
│   ├── css/
│   └── js/
└── uploads/             # File storage directory
```

## Installation

### Local Development

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd college-materials-portal
   ```

2. Create and activate virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # or
   venv\Scripts\activate     # Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:
   ```bash
   python main.py
   ```

5. Open browser to `http://localhost:5000`

### Production Deployment

The application uses Gunicorn for production deployment:

```bash
gunicorn --bind 0.0.0.0:5000 --reuse-port --reload main:app
```

## Configuration

- **Storage**: Currently uses JSON-based file storage (`data.json`)
- **Database**: PostgreSQL support included but not required
- **File Uploads**: No size restrictions (configurable)
- **Session Management**: Uses Flask sessions with configurable secret key

## Usage

1. **Navigate**: Start from homepage → Select course type → Choose department → Pick semester → Select category
2. **Upload**: Use drag-and-drop interface or browse files
3. **Download**: Click download button on any file
4. **Delete**: Use delete button with confirmation dialog
5. **Calculate**: Access GPA/CGPA calculators from main menu

## Technical Details

- **Framework**: Flask 3.1+
- **Frontend**: Bootstrap 5.3, Font Awesome 6.4
- **Storage**: JSON + Local filesystem
- **Server**: Gunicorn WSGI server
- **Security**: Werkzeug secure filename handling

## Contributing

1. Fork the repository
2. Create feature branch
3. Make changes
4. Test functionality
5. Submit pull request

## License

MIT License - See LICENSE file for details