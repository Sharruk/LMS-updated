import os
import json
import logging
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, send_file, send_from_directory, jsonify, session
from werkzeug.utils import secure_filename
from werkzeug.middleware.proxy_fix import ProxyFix
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, Subject, File, User

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key-change-in-production")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///college_portal.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db.init_app(app)

# Configuration
UPLOAD_FOLDER = 'uploads'
DATA_FILE = 'data.json'
MAX_FILE_SIZE = None  # No file size limit
ALLOWED_EXTENSIONS = set()  # Allow all file types

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# Remove file size limit completely

# Ensure directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def load_community_data():
    """Load community data from JSON file"""
    try:
        if os.path.exists('community.json'):
            with open('community.json', 'r') as f:
                return json.load(f)
        else:
            return {"discussions": []}
    except Exception as e:
        app.logger.error(f"Error loading community data: {str(e)}")
        return {"discussions": []}

def save_community_data(data):
    """Save community data to JSON file"""
    try:
        with open('community.json', 'w') as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        app.logger.error(f"Error saving community data: {str(e)}")

def load_clubs_data():
    """Load clubs data from JSON file"""
    try:
        if os.path.exists('clubs.json'):
            with open('clubs.json', 'r') as f:
                return json.load(f)
        else:
            return {"clubs": [], "next_id": 1}
    except Exception as e:
        app.logger.error(f"Error loading clubs data: {str(e)}")
        return {"clubs": [], "next_id": 1}

def save_clubs_data(data):
    """Save clubs data to JSON file"""
    try:
        with open('clubs.json', 'w') as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        app.logger.error(f"Error saving clubs data: {str(e)}")
        raise

def load_transportation_data():
    """Load transportation data from JSON file"""
    try:
        if os.path.exists('transportation.json'):
            with open('transportation.json', 'r') as f:
                return json.load(f)
        else:
            return {"bus_routes": [], "next_id": 1}
    except Exception as e:
        app.logger.error(f"Error loading transportation data: {str(e)}")
        return {"bus_routes": [], "next_id": 1}

def save_transportation_data(data):
    """Save transportation data to JSON file"""
    try:
        with open('transportation.json', 'w') as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        app.logger.error(f"Error saving transportation data: {str(e)}")
        raise

def load_canteen_data():
    """Load canteen data from JSON file"""
    try:
        if os.path.exists('canteen.json'):
            with open('canteen.json', 'r') as f:
                return json.load(f)
        else:
            return {"canteens": [], "next_id": 1}
    except Exception as e:
        app.logger.error(f"Error loading canteen data: {str(e)}")
        return {"canteens": [], "next_id": 1}

def save_canteen_data(data):
    """Save canteen data to JSON file"""
    try:
        with open('canteen.json', 'w') as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        app.logger.error(f"Error saving canteen data: {str(e)}")
        raise

def load_places_data():
    """Load places data from JSON file"""
    try:
        if os.path.exists('places.json'):
            with open('places.json', 'r') as f:
                return json.load(f)
        else:
            return {"places": [], "next_id": 1}
    except Exception as e:
        app.logger.error(f"Error loading places data: {str(e)}")
        return {"places": [], "next_id": 1}

def save_places_data(data):
    """Save places data to JSON file"""
    try:
        with open('places.json', 'w') as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        app.logger.error(f"Error saving places data: {str(e)}")
        raise

def load_hostels_data():
    """Load hostels data from JSON file"""
    try:
        if os.path.exists('hostels.json'):
            with open('hostels.json', 'r') as f:
                return json.load(f)
        else:
            return {"hostels": [], "next_id": 1}
    except Exception as e:
        app.logger.error(f"Error loading hostels data: {str(e)}")
        return {"hostels": [], "next_id": 1}

def save_hostels_data(data):
    """Save hostels data to JSON file"""
    try:
        with open('hostels.json', 'w') as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        app.logger.error(f"Error saving hostels data: {str(e)}")
        raise

def load_events_data():
    """Load events data from JSON file"""
    try:
        if os.path.exists('events.json'):
            with open('events.json', 'r') as f:
                return json.load(f)
        else:
            return {"events": [], "next_id": 1}
    except Exception as e:
        app.logger.error(f"Error loading events data: {str(e)}")
        return {"events": [], "next_id": 1}

def save_events_data(data):
    """Save events data to JSON file"""
    try:
        with open('events.json', 'w') as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        app.logger.error(f"Error saving events data: {str(e)}")
        raise

def load_data():
    """Load data from JSON file"""
    try:
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r') as f:
                return json.load(f)
        else:
            # Initialize with sample data
            data = {
                "course_types": {
                    "ug": {
                        "name": "Under Graduate (UG)",
                        "departments": {
                            "cse": {
                                "name": "Computer Science & Engineering",
                                "semesters": {str(i): {"name": f"Semester {i}"} for i in range(1, 9)}
                            },
                            "mech": {
                                "name": "Mechanical Engineering", 
                                "semesters": {str(i): {"name": f"Semester {i}"} for i in range(1, 9)}
                            },
                            "eee": {
                                "name": "Electrical & Electronics Engineering",
                                "semesters": {str(i): {"name": f"Semester {i}"} for i in range(1, 9)}
                            },
                            "ece": {
                                "name": "Electronics & Communication Engineering",
                                "semesters": {str(i): {"name": f"Semester {i}"} for i in range(1, 9)}
                            },
                            "it": {
                                "name": "Information Technology",
                                "semesters": {str(i): {"name": f"Semester {i}"} for i in range(1, 9)}
                            },
                            "chem": {
                                "name": "Chemical Engineering",
                                "semesters": {str(i): {"name": f"Semester {i}"} for i in range(1, 9)}
                            },
                            "civil": {
                                "name": "Civil Engineering",
                                "semesters": {str(i): {"name": f"Semester {i}"} for i in range(1, 9)}
                            }
                        }
                    },
                    "pg": {
                        "name": "Post Graduate (PG)",
                        "departments": {
                            "mtech_cse": {
                                "name": "M.Tech CSE (5-Year)",
                                "semesters": {str(i): {"name": f"Semester {i}"} for i in range(1, 11)}
                            },
                            "me_applied_electronics": {
                                "name": "M.E Applied Electronics",
                                "semesters": {str(i): {"name": f"Semester {i}"} for i in range(1, 5)}
                            },
                            "me_structural": {
                                "name": "M.E Structural",
                                "semesters": {str(i): {"name": f"Semester {i}"} for i in range(1, 5)}
                            },
                            "me_ped": {
                                "name": "M.E PED",
                                "semesters": {str(i): {"name": f"Semester {i}"} for i in range(1, 5)}
                            }
                        }
                    },
                    "mba": {
                        "name": "Master of Business Administration (MBA)",
                        "departments": {
                            "general_mba": {
                                "name": "General MBA",
                                "semesters": {str(i): {"name": f"Semester {i}"} for i in range(1, 5)}
                            }
                        }
                    }
                },
                "files": []
            }
            save_data(data)
            return data
    except Exception as e:
        app.logger.error(f"Error loading data: {e}")
        return {"course_types": {}, "files": []}

def save_data(data):
    """Save data to JSON file"""
    try:
        with open(DATA_FILE, 'w') as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        app.logger.error(f"Error saving data: {e}")

def allowed_file(filename):
    """Allow all file types"""
    return True  # Accept all file types

def get_file_size(filepath):
    """Get human readable file size"""
    size = os.path.getsize(filepath)
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024.0:
            return f"{size:.1f} {unit}"
        size /= 1024.0
    return f"{size:.1f} TB"

@app.route('/')
def index():
    """Homepage showing main sections: Question Papers and Syllabus"""
    return render_template('index.html')

@app.route('/materials')
def materials_home():
    """Materials homepage showing course types for question papers"""
    data = load_data()
    return render_template('materials/home.html', course_types=data['course_types'])

@app.route('/calculators')
def calculators_home():
    """Calculators homepage showing available calculators"""
    return render_template('calculators/home.html')

@app.route('/calculators/gpa')
def gpa_calculator():
    """GPA Calculator page"""
    return render_template('calculators/gpa.html')

@app.route('/calculators/cgpa')
def cgpa_calculator():
    """CGPA Calculator page"""
    return render_template('calculators/cgpa.html')

@app.route('/calculators/percentage')
def percentage_calculator():
    """Percentage Calculator page"""
    return render_template('calculators/percentage.html')

@app.route('/calculators/internal')
def internal_calculator():
    """Internal Marks Calculator page"""
    return render_template('calculators/internal.html')

@app.route('/course/<course_type_id>')
def course_type(course_type_id):
    """Course type page showing list of departments"""
    data = load_data()
    if course_type_id not in data['course_types']:
        flash('Course type not found', 'error')
        return redirect(url_for('index'))
    
    course_data = data['course_types'][course_type_id]
    return render_template('course_type.html', 
                         course_type=course_data,
                         course_type_id=course_type_id)

@app.route('/department/<course_type_id>/<dept_id>')
def department(course_type_id, dept_id):
    """Department page showing list of semesters"""
    data = load_data()
    if course_type_id not in data['course_types'] or dept_id not in data['course_types'][course_type_id]['departments']:
        flash('Department not found', 'error')
        return redirect(url_for('index'))
    
    course_data = data['course_types'][course_type_id]
    department_data = course_data['departments'][dept_id]
    return render_template('department.html', 
                         course_type=course_data,
                         course_type_id=course_type_id,
                         department=department_data, 
                         dept_id=dept_id)

@app.route('/semester/<course_type_id>/<dept_id>/<semester_id>')
def semester(course_type_id, dept_id, semester_id):
    """Semester page showing list of categories"""
    data = load_data()
    if (course_type_id not in data['course_types'] or 
        dept_id not in data['course_types'][course_type_id]['departments']):
        flash('Department not found', 'error')
        return redirect(url_for('index'))
    
    course_data = data['course_types'][course_type_id]
    department_data = course_data['departments'][dept_id]
    categories = ['CAT', 'ESE', 'SAT', 'Practical']
    
    return render_template('semester.html', 
                         course_type=course_data,
                         course_type_id=course_type_id,
                         department=department_data,
                         dept_id=dept_id,
                         semester_id=semester_id,
                         categories=categories)

@app.route('/category/<course_type_id>/<dept_id>/<semester_id>/<category>')
def category_view(course_type_id, dept_id, semester_id, category):
    """Category page showing downloadable files"""
    data = load_data()
    if (course_type_id not in data['course_types'] or 
        dept_id not in data['course_types'][course_type_id]['departments']):
        flash('Department not found', 'error')
        return redirect(url_for('index'))
    
    # Filter files for this specific category (case-insensitive matching)
    filtered_files = [
        f for f in data['files'] 
        if f['course_type'].lower() == course_type_id.lower() and
           f['department'].lower() == dept_id.lower() and 
           f['semester'] == semester_id and 
           f['category'].upper() == category.upper()
    ]
    
    course_data = data['course_types'][course_type_id]
    department_data = course_data['departments'][dept_id]
    
    return render_template('category.html',
                         course_type=course_data,
                         course_type_id=course_type_id,
                         department=department_data,
                         dept_id=dept_id,
                         semester_id=semester_id,
                         category=category,
                         files=filtered_files)

@app.route('/api/search')
def api_search():
    """API endpoint for global search"""
    try:
        # Get search parameters
        query = request.args.get('q', '').strip()
        course_type = request.args.get('course_type', '').strip()
        department = request.args.get('department', '').strip()
        semester = request.args.get('semester', '').strip()
        category = request.args.get('category', '').strip()
        file_type = request.args.get('file_type', '').strip()
        
        # For now, use JSON data until database is fully migrated
        data = load_data()
        all_files = data.get('files', [])
        
        # Apply filters
        filtered_files = []
        for file in all_files:
            # Text search
            if query:
                subject_name = (file.get('subject') or '').lower()
                filename = (file.get('custom_filename') or '').lower()
                if query.lower() not in subject_name and query.lower() not in filename:
                    continue
            
            # Course type filter
            if course_type and file.get('course_type', '').upper() != course_type.upper():
                continue
                
            # Department filter
            if department and file.get('department', '').lower() != department.lower():
                continue
                
            # Semester filter
            if semester and str(file.get('semester', '')) != semester:
                continue
                
            # Category filter
            if category and file.get('category', '').upper() != category.upper():
                continue
                
            # File type filter (assume QP for now)
            if file_type and file_type != 'QP':
                continue
            
            # Add file type for display
            file['file_type'] = 'QP'
            file['subject_code'] = None  # Will be populated when subjects are linked
            
            filtered_files.append(file)
        
        # Limit results for performance
        results = filtered_files[:50]
        
        return jsonify({
            'success': True,
            'results': results,
            'count': len(results)
        })
        
    except Exception as e:
        app.logger.error(f"Search API error: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e),
            'results': [],
            'count': 0
        }), 500

@app.route('/vote/<int:file_id>', methods=['POST'])
def vote_file(file_id):
    """Handle like/dislike votes for files"""
    try:
        vote_type = request.json.get('vote_type')  # 'like' or 'dislike'
        
        if vote_type not in ['like', 'dislike']:
            return jsonify({'success': False, 'error': 'Invalid vote type'}), 400
        
        data = load_data()
        files = data.get('files', [])
        
        # Find the file
        file_found = False
        for file in files:
            if file['id'] == file_id:
                file_found = True
                
                # Initialize vote counts if not present
                if 'likes' not in file:
                    file['likes'] = 0
                if 'dislikes' not in file:
                    file['dislikes'] = 0
                
                # Increment the vote count
                if vote_type == 'like':
                    file['likes'] += 1
                else:
                    file['dislikes'] += 1
                
                break
        
        if not file_found:
            return jsonify({'success': False, 'error': 'File not found'}), 404
        
        # Save updated data
        save_data(data)
        
        return jsonify({
            'success': True,
            'likes': file['likes'],
            'dislikes': file['dislikes']
        })
        
    except Exception as e:
        app.logger.error(f"Vote error: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/comment/<int:file_id>', methods=['POST'])
def add_comment(file_id):
    """Add a comment to a file"""
    try:
        comment_data = request.json
        name = comment_data.get('name', '').strip()
        comment_text = comment_data.get('comment', '').strip()
        file_type = comment_data.get('file_type', 'QP')  # 'QP' or 'Syllabus'
        
        if not name or not comment_text:
            return jsonify({'success': False, 'error': 'Name and comment are required'}), 400
        
        data = load_data()
        
        # Choose the right file list based on file type
        if file_type == 'Syllabus':
            files = data.get('syllabus_files', [])
        else:
            files = data.get('files', [])
        
        # Find the file
        file_found = False
        for file in files:
            if file['id'] == file_id:
                file_found = True
                
                # Initialize comments if not present
                if 'comments' not in file:
                    file['comments'] = []
                
                # Add the new comment
                new_comment = {
                    'name': name,
                    'comment': comment_text,
                    'date': datetime.now().strftime('%Y-%m-%d %H:%M')
                }
                file['comments'].append(new_comment)
                
                break
        
        if not file_found:
            return jsonify({'success': False, 'error': 'File not found'}), 404
        
        # Save updated data
        save_data(data)
        
        return jsonify({
            'success': True,
            'comment': new_comment,
            'total_comments': len(file['comments'])
        })
        
    except Exception as e:
        app.logger.error(f"Comment error: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/vote_syllabus/<int:file_id>', methods=['POST'])
def vote_syllabus_file(file_id):
    """Handle like/dislike votes for syllabus files"""
    try:
        vote_type = request.json.get('vote_type')  # 'like' or 'dislike'
        
        if vote_type not in ['like', 'dislike']:
            return jsonify({'success': False, 'error': 'Invalid vote type'}), 400
        
        data = load_data()
        files = data.get('syllabus_files', [])
        
        # Find the file
        file_found = False
        for file in files:
            if file['id'] == file_id:
                file_found = True
                
                # Initialize vote counts if not present
                if 'likes' not in file:
                    file['likes'] = 0
                if 'dislikes' not in file:
                    file['dislikes'] = 0
                
                # Increment the vote count
                if vote_type == 'like':
                    file['likes'] += 1
                else:
                    file['dislikes'] += 1
                
                break
        
        if not file_found:
            return jsonify({'success': False, 'error': 'File not found'}), 404
        
        # Save updated data
        save_data(data)
        
        return jsonify({
            'success': True,
            'likes': file['likes'],
            'dislikes': file['dislikes']
        })
        
    except Exception as e:
        app.logger.error(f"Vote error: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/file/<int:file_id>')
def file_detail(file_id):
    """Display detailed view of a file"""
    try:
        data = load_data()
        
        # Search in regular files first
        file_found = None
        file_type = 'QP'
        
        for file in data.get('files', []):
            if file['id'] == file_id:
                file_found = file
                file_type = 'QP'
                break
        
        # Search in syllabus files if not found
        if not file_found:
            for file in data.get('syllabus_files', []):
                if file['id'] == file_id:
                    file_found = file
                    file_type = 'Syllabus'
                    break
        
        if not file_found:
            flash('File not found.', 'error')
            return redirect(url_for('index'))
        
        # Check if the physical file exists
        if 'filename' in file_found:
            file_path = os.path.join(UPLOAD_FOLDER, file_found['filename'])
            if not os.path.exists(file_path):
                app.logger.warning(f"Database has file {file_found['filename']} but physical file missing")
                flash('File has been deleted or moved. Please contact administrator.', 'error')
                return redirect(url_for('index'))
        
        # Ensure social fields exist
        if 'likes' not in file_found:
            file_found['likes'] = 0
        if 'dislikes' not in file_found:
            file_found['dislikes'] = 0
        if 'comments' not in file_found:
            file_found['comments'] = []
        
        return render_template('file_detail.html', 
                             file=file_found, 
                             file_type=file_type)
        
    except Exception as e:
        app.logger.error(f"File detail error: {str(e)}")
        flash('Error loading file details.', 'error')
        return redirect(url_for('index'))

def highlight_search_terms(file, query):
    """Add highlighting to search terms in file data"""
    highlighted_file = file.copy()
    
    # Fields to highlight
    highlight_fields = ['subject', 'custom_filename', 'original_filename']
    
    for field in highlight_fields:
        if field in highlighted_file and highlighted_file[field]:
            original_text = highlighted_file[field]
            # Simple highlighting - wrap matched terms with <mark> tags
            highlighted_text = original_text
            
            # Case-insensitive replacement
            import re
            pattern = re.compile(re.escape(query), re.IGNORECASE)
            highlighted_text = pattern.sub(f'<mark>{query}</mark>', highlighted_text)
            
            highlighted_file[f'{field}_highlighted'] = highlighted_text
    
    return highlighted_file

@app.route('/search')
def search():
    """Search page for all files"""
    data = load_data()
    all_files = data.get('files', [])
    
    return render_template('search.html', all_files=all_files)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    """Upload new files"""
    data = load_data()
    
    if request.method == 'POST':
        try:
            # Get form data
            course_type = request.form.get('course_type')
            department = request.form.get('department')
            semester = request.form.get('semester')
            category = request.form.get('category')
            subject = request.form.get('subject')
            description = request.form.get('description', '').strip()
            custom_filename = request.form.get('filename')
            
            # Check if file was uploaded
            if 'file' not in request.files:
                flash('No file selected', 'error')
                return redirect(request.url)
            
            file = request.files['file']
            if file.filename == '':
                flash('No file selected', 'error')
                return redirect(request.url)
            
            if file and file.filename and allowed_file(file.filename):
                try:
                    # Use custom filename if provided, otherwise use original
                    if custom_filename:
                        filename = secure_filename(custom_filename)
                        # Add extension if not present
                        if '.' in file.filename:
                            ext = file.filename.rsplit('.', 1)[1].lower()
                            if not filename.endswith('.' + ext):
                                filename += '.' + ext
                    else:
                        filename = secure_filename(file.filename)
                    
                    # Validate filename
                    if not filename or filename == '':
                        raise ValueError("Invalid filename after security processing")
                    
                    # Handle duplicate filenames
                    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    counter = 1
                    base_name, extension = os.path.splitext(filename)
                    
                    while os.path.exists(filepath):
                        filename = f"{base_name}_{counter}{extension}"
                        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                        counter += 1
                    
                    # Ensure upload directory exists
                    os.makedirs(os.path.dirname(filepath), exist_ok=True)
                    
                    # Save the file
                    file.save(filepath)
                    
                    # Verify file was saved
                    if not os.path.exists(filepath):
                        raise IOError("File was not saved successfully")
                    
                    # Generate unique ID safely
                    max_id = 0
                    for existing_file in data.get('files', []):
                        if existing_file.get('id', 0) > max_id:
                            max_id = existing_file['id']
                    new_id = max_id + 1
                    
                    # Normalize department and course type to match data structure keys
                    def normalize_course_type(ct):
                        return ct.lower() if ct else ct
                    
                    def normalize_department(dept, course_type):
                        if not dept:
                            return dept
                        
                        # Map frontend department names to data structure keys
                        dept_map = {
                            'CSE': 'cse',
                            'MECH': 'mech', 
                            'EEE': 'eee',
                            'ECE': 'ece',
                            'IT': 'it',
                            'CHEM': 'chem',
                            'CIVIL': 'civil',
                            'M.Tech CSE (5-Year)': 'mtech_cse',
                            'M.E Applied Electronics': 'applied_electronics',
                            'M.E Structural': 'structural',
                            'M.E PED': 'ped',
                            'General MBA': 'general_mba'
                        }
                        
                        return dept_map.get(dept, dept.lower())
                    
                    normalized_course_type = normalize_course_type(course_type)
                    normalized_department = normalize_department(department, course_type)
                    
                    # Add file metadata to JSON
                    file_data = {
                        "id": new_id,
                        "filename": filename,
                        "original_filename": file.filename,
                        "custom_filename": custom_filename or filename,
                        "course_type": normalized_course_type,
                        "department": normalized_department,
                        "semester": semester,
                        "category": category,
                        "subject": subject,
                        "description": description,
                        "size": get_file_size(filepath),
                        "upload_date": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        "file_path": filepath,
                        "likes": 0,
                        "dislikes": 0,
                        "comments": []
                    }
                    
                    data['files'].append(file_data)
                    save_data(data)
                    
                    app.logger.info(f"File uploaded successfully: {filename}")
                    try:
                        flash('File uploaded successfully!', 'success')
                    except:
                        app.logger.error("Could not flash success message")
                    
                    return redirect(url_for('category_view', 
                                  course_type_id=normalized_course_type,
                                  dept_id=normalized_department, 
                                  semester_id=semester, 
                                  category=category))
                
                except Exception as file_error:
                    app.logger.error(f"File processing error: {str(file_error)}")
                    try:
                        flash(f'File processing error: {str(file_error)}', 'error')
                    except:
                        app.logger.error("Could not flash file processing error")
            else:
                flash('File type not allowed', 'error')
                
        except Exception as e:
            app.logger.error(f"Upload error: {str(e)}")
            try:
                flash(f'Upload error: {str(e)}', 'error')
            except:
                app.logger.error("Failed to display error message to user")
    
    return render_template('upload.html', course_types=data['course_types'])

@app.route('/delete/<int:file_id>', methods=['POST', 'GET'])
def delete_file(file_id):
    """Delete a file"""
    try:
        data = load_data()
        file_data = None
        
        # Find the file
        for file_info in data.get('files', []):
            if file_info.get('id') == file_id:
                file_data = file_info
                break
        
        if not file_data:
            flash('File not found', 'error')
            return redirect(url_for('index'))
        
        # Delete physical file
        file_path = file_data.get('file_path')
        if file_path and os.path.exists(file_path):
            os.remove(file_path)
            app.logger.info(f"Physical file deleted: {file_path}")
        
        # Remove from data.json
        data['files'] = [f for f in data['files'] if f.get('id') != file_id]
        save_data(data)
        
        flash('File deleted successfully!', 'success')
        app.logger.info(f"File deleted successfully: {file_data.get('custom_filename', 'Unknown')}")
        
        # Redirect back to the category page
        return redirect(url_for('category_view',
                              course_type_id=file_data.get('course_type', 'ug'),
                              dept_id=file_data.get('department', 'cse'),
                              semester_id=file_data.get('semester', '1'),
                              category=file_data.get('category', 'CAT')))
        
    except Exception as e:
        app.logger.error(f"Delete error: {str(e)}")
        flash(f'Delete error: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.route('/download/<int:file_id>')
def download(file_id):
    """Download a file"""
    try:
        data = load_data()
        file_data = None
        
        for f in data['files']:
            if f['id'] == file_id:
                file_data = f
                break
        
        if not file_data:
            flash('File not found', 'error')
            return redirect(url_for('index'))
        
        filepath = file_data['file_path']
        if os.path.exists(filepath) and os.path.isfile(filepath):
            return send_file(filepath, as_attachment=True, download_name=file_data['custom_filename'])
        else:
            flash('File not found on disk', 'error')
            return redirect(url_for('index'))
    
    except Exception as e:
        app.logger.error(f"Download error: {str(e)}")
        flash('Error downloading file', 'error')
        return redirect(url_for('index'))

# Syllabus Routes
@app.route('/syllabus')
def syllabus_home():
    """Syllabus homepage showing course types"""
    course_types = {
        'ug': {
            'name': 'Under Graduate (UG)',
            'icon': 'fas fa-user-graduate',
            'color': 'primary'
        },
        'pg': {
            'name': 'Post Graduate (PG)', 
            'icon': 'fas fa-graduation-cap',
            'color': 'success'
        },
        'mba': {
            'name': 'Master of Business Administration (MBA)',
            'icon': 'fas fa-briefcase',
            'color': 'warning'
        }
    }
    return render_template('syllabus/home.html', course_types=course_types)

@app.route('/syllabus/<course_type>')
def syllabus_course_type(course_type):
    """Syllabus course type page showing departments"""
    departments = {
        'ug': {
            'name': 'Under Graduate (UG)',
            'departments': {
                'cse': 'Computer Science & Engineering',
                'mech': 'Mechanical Engineering',
                'eee': 'Electrical & Electronics Engineering',
                'ece': 'Electronics & Communication Engineering',
                'it': 'Information Technology',
                'chem': 'Chemical Engineering',
                'civil': 'Civil Engineering'
            }
        },
        'pg': {
            'name': 'Post Graduate (PG)',
            'departments': {
                'mtech_cse_5yr': 'M.Tech CSE (5-Year)',
                'me_applied_electronics': 'M.E Applied Electronics',
                'me_structural': 'M.E Structural',
                'me_ped': 'M.E PED'
            }
        },
        'mba': {
            'name': 'Master of Business Administration (MBA)',
            'departments': {
                'general_mba': 'General MBA'
            }
        }
    }
    
    if course_type not in departments:
        flash('Course type not found', 'error')
        return redirect(url_for('syllabus_home'))
    
    course_data = departments[course_type]
    return render_template('syllabus/course_type.html', 
                         course_type=course_data,
                         course_type_id=course_type)

@app.route('/syllabus/<course_type>/<dept_id>')
def syllabus_department(course_type, dept_id):
    """Syllabus department page showing regulations"""
    regulations = ['2017', '2023', '2025']
    
    departments = {
        'ug': {
            'name': 'Under Graduate (UG)',
            'departments': {
                'cse': 'Computer Science & Engineering',
                'mech': 'Mechanical Engineering',
                'eee': 'Electrical & Electronics Engineering',
                'ece': 'Electronics & Communication Engineering',
                'it': 'Information Technology',
                'chem': 'Chemical Engineering',
                'civil': 'Civil Engineering'
            }
        },
        'pg': {
            'name': 'Post Graduate (PG)',
            'departments': {
                'mtech_cse_5yr': 'M.Tech CSE (5-Year)',
                'me_applied_electronics': 'M.E Applied Electronics',
                'me_structural': 'M.E Structural',
                'me_ped': 'M.E PED'
            }
        },
        'mba': {
            'name': 'Master of Business Administration (MBA)',
            'departments': {
                'general_mba': 'General MBA'
            }
        }
    }
    
    if course_type not in departments or dept_id not in departments[course_type]['departments']:
        flash('Department not found', 'error')
        return redirect(url_for('syllabus_home'))
    
    course_data = departments[course_type]
    dept_name = departments[course_type]['departments'][dept_id]
    
    return render_template('syllabus/department.html',
                         course_type=course_data,
                         course_type_id=course_type,
                         dept_name=dept_name,
                         dept_id=dept_id,
                         regulations=regulations)

@app.route('/syllabus/<course_type>/<dept_id>/<regulation>')
def syllabus_regulation(course_type, dept_id, regulation):
    """Syllabus regulation page showing files and upload"""
    data = load_data()
    
    # Filter syllabus files for this specific regulation
    syllabus_files = []
    for file_data in data.get('syllabus_files', []):
        if (file_data['course_type'] == course_type and 
            file_data['department'] == dept_id and 
            file_data['regulation'] == regulation):
            syllabus_files.append(file_data)
    
    departments = {
        'ug': {
            'name': 'Under Graduate (UG)',
            'departments': {
                'cse': 'Computer Science & Engineering',
                'mech': 'Mechanical Engineering',
                'eee': 'Electrical & Electronics Engineering',
                'ece': 'Electronics & Communication Engineering',
                'it': 'Information Technology',
                'chem': 'Chemical Engineering',
                'civil': 'Civil Engineering'
            }
        },
        'pg': {
            'name': 'Post Graduate (PG)',
            'departments': {
                'mtech_cse_5yr': 'M.Tech CSE (5-Year)',
                'me_applied_electronics': 'M.E Applied Electronics',
                'me_structural': 'M.E Structural',
                'me_ped': 'M.E PED'
            }
        },
        'mba': {
            'name': 'Master of Business Administration (MBA)',
            'departments': {
                'general_mba': 'General MBA'
            }
        }
    }
    
    if course_type not in departments or dept_id not in departments[course_type]['departments']:
        flash('Department not found', 'error')
        return redirect(url_for('syllabus_home'))
    
    course_data = departments[course_type]
    dept_name = departments[course_type]['departments'][dept_id]
    
    return render_template('syllabus/regulation.html',
                         course_type=course_data,
                         course_type_id=course_type,
                         dept_name=dept_name,
                         dept_id=dept_id,
                         regulation=regulation,
                         syllabus_files=syllabus_files)

@app.route('/syllabus/upload/<course_type>/<dept_id>/<regulation>', methods=['POST'])
def upload_syllabus(course_type, dept_id, regulation):
    """Upload syllabus file"""
    try:
        if 'file' not in request.files:
            flash('No file selected', 'error')
            return redirect(url_for('syllabus_regulation', course_type=course_type, dept_id=dept_id, regulation=regulation))
        
        file = request.files['file']
        if file.filename == '':
            flash('No file selected', 'error')
            return redirect(url_for('syllabus_regulation', course_type=course_type, dept_id=dept_id, regulation=regulation))
        
        if file and file.filename and allowed_file(file.filename):
            try:
                # Load existing data
                data = load_data()
                if 'syllabus_files' not in data:
                    data['syllabus_files'] = []
                
                # Generate unique filename
                original_filename = file.filename
                filename = secure_filename(original_filename)
                
                # Validate filename
                if not filename or filename == '':
                    raise ValueError("Invalid filename after security processing")
                
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                unique_filename = f"syllabus_{timestamp}_{filename}"
                filepath = os.path.join(UPLOAD_FOLDER, unique_filename)
                
                # Ensure upload directory exists
                os.makedirs(UPLOAD_FOLDER, exist_ok=True)
                
                # Save file
                file.save(filepath)
                
                # Verify file was saved
                if not os.path.exists(filepath):
                    raise IOError("Syllabus file was not saved successfully")
                
                # Get file info
                file_size = os.path.getsize(filepath)
                file_extension = filename.rsplit('.', 1)[1].lower()
                
                # Generate unique ID safely
                max_id = 0
                for existing_file in data.get('syllabus_files', []):
                    if existing_file.get('id', 0) > max_id:
                        max_id = existing_file['id']
                new_id = max_id + 1
                
                # Add to data
                # Get form data for syllabus
                custom_filename = request.form.get('custom_filename', '').strip()
                description = request.form.get('description', '').strip()
                
                file_info = {
                    'id': new_id,
                    'filename': unique_filename,
                    'original_filename': original_filename,
                    'custom_filename': custom_filename or original_filename,
                    'file_size': file_size,
                    'file_extension': file_extension,
                    'course_type': course_type,
                    'department': dept_id,
                    'regulation': regulation,
                    'description': description,
                    'size': f"{file_size / (1024*1024):.1f} MB" if file_size > 1024*1024 else f"{file_size / 1024:.1f} KB",
                    'upload_date': datetime.now().isoformat(),
                    'file_path': filepath,
                    'likes': 0,
                    'dislikes': 0,
                    'comments': []
                }
                
                data['syllabus_files'].append(file_info)
                save_data(data)
                
                app.logger.info(f"Syllabus uploaded successfully: {original_filename}")
                try:
                    flash('Syllabus uploaded successfully!', 'success')
                except:
                    app.logger.error("Could not flash syllabus success message")
            
            except Exception as syllabus_error:
                app.logger.error(f"Syllabus file processing error: {str(syllabus_error)}")
                try:
                    flash(f'Syllabus upload error: {str(syllabus_error)}', 'error')
                except:
                    app.logger.error("Could not flash syllabus processing error")
        else:
            flash('File uploaded successfully!', 'success')
    
    except Exception as e:
        app.logger.error(f"Syllabus upload error: {str(e)}")
        try:
            flash(f'Upload error: {str(e)}', 'error')
        except:
            app.logger.error("Failed to display syllabus error message to user")
    
    return redirect(url_for('syllabus_regulation', course_type=course_type, dept_id=dept_id, regulation=regulation))

@app.route('/syllabus/download/<int:file_id>')
def download_syllabus(file_id):
    """Download syllabus file"""
    try:
        data = load_data()
        file_data = None
        
        for f in data.get('syllabus_files', []):
            if f['id'] == file_id:
                file_data = f
                break
        
        if not file_data:
            flash('File not found', 'error')
            return redirect(url_for('syllabus_home'))
        
        filepath = file_data['file_path']
        if os.path.exists(filepath) and os.path.isfile(filepath):
            return send_file(filepath, as_attachment=True, download_name=file_data['original_filename'])
        else:
            flash('File not found on disk', 'error')
            return redirect(url_for('syllabus_home'))
    
    except Exception as e:
        app.logger.error(f"Syllabus download error: {str(e)}")
        flash('Error downloading file', 'error')
        return redirect(url_for('syllabus_home'))

@app.route('/syllabus/delete/<int:file_id>', methods=['POST', 'GET'])
def delete_syllabus(file_id):
    """Delete syllabus file"""
    try:
        data = load_data()
        file_data = None
        file_index = -1
        
        for i, f in enumerate(data.get('syllabus_files', [])):
            if f['id'] == file_id:
                file_data = f
                file_index = i
                break
        
        if not file_data:
            flash('File not found', 'error')
            return redirect(url_for('syllabus_home'))
        
        # Delete physical file
        filepath = file_data['file_path']
        if os.path.exists(filepath) and os.path.isfile(filepath):
            os.remove(filepath)
        
        # Remove from JSON data
        if 'syllabus_files' not in data:
            data['syllabus_files'] = []
        data['syllabus_files'].pop(file_index)
        save_data(data)
        
        flash('Syllabus deleted successfully', 'success')
        return redirect(url_for('syllabus_regulation',
                      course_type=file_data['course_type'],
                      dept_id=file_data['department'],
                      regulation=file_data['regulation']))
    
    except Exception as e:
        app.logger.error(f"Syllabus delete error: {str(e)}")
        flash('Error deleting file', 'error')
        return redirect(url_for('syllabus_home'))

@app.errorhandler(413)
def file_too_large(error):
    """Handle file too large error"""
    flash('File uploaded successfully. No size restrictions.', 'success')
    return redirect(url_for('upload'))

@app.errorhandler(404)
def page_not_found(error):
    """Handle 404 errors"""
    return redirect(url_for('index'))

@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    """Serve uploaded files securely"""
    try:
        # Security check: ensure filename doesn't contain path traversal
        if '..' in filename or filename.startswith('/'):
            app.logger.warning(f"Invalid file path attempted: {filename}")
            return "Invalid file path", 400
        
        # Construct absolute path
        file_path = os.path.join(os.path.abspath(UPLOAD_FOLDER), filename)
        
        # Check if file exists
        if not os.path.exists(file_path):
            app.logger.error(f"File not found: {file_path}")
            # List available files for debugging
            available_files = []
            if os.path.exists(UPLOAD_FOLDER):
                available_files = os.listdir(UPLOAD_FOLDER)
            app.logger.info(f"Available files in uploads: {available_files}")
            return "File not found", 404
        
        # Verify file is within uploads directory (additional security)
        if not file_path.startswith(os.path.abspath(UPLOAD_FOLDER)):
            app.logger.warning(f"File path outside uploads directory: {file_path}")
            return "Invalid file path", 400
            
        return send_from_directory(os.path.abspath(UPLOAD_FOLDER), filename, as_attachment=False)
    except Exception as e:
        app.logger.error(f"Error serving file {filename}: {str(e)}")
        return f"Error serving file: {str(e)}", 500

@app.route('/community')
def community():
    """Community discussion page"""
    try:
        community_data = load_community_data()
        discussions = community_data.get('discussions', [])
        
        # Get sorting parameter
        sort_by = request.args.get('sort', 'latest')
        
        # Sort discussions based on selected option
        if sort_by == 'replies':
            discussions = sorted(discussions, key=lambda x: len(x.get('replies', [])), reverse=True)
        elif sort_by == 'likes':
            discussions = sorted(discussions, key=lambda x: x.get('likes', 0), reverse=True)
        else:  # latest (default)
            discussions = sorted(discussions, key=lambda x: x.get('date', ''), reverse=True)
        
        return render_template('community.html', discussions=discussions, current_sort=sort_by)
    except Exception as e:
        app.logger.error(f"Error loading community data: {str(e)}")
        flash('Error loading community discussions', 'error')
        return redirect(url_for('index'))

@app.route('/community/create', methods=['POST'])
def create_discussion():
    """Create a new discussion"""
    try:
        data = request.json
        name = data.get('name', 'Anonymous').strip()
        title = data.get('title', '').strip()
        description = data.get('description', '').strip()
        
        if not title or not description:
            return jsonify({'success': False, 'error': 'Title and description are required'}), 400
        
        community_data = load_community_data()
        
        # Generate unique ID
        max_id = 0
        for discussion in community_data.get('discussions', []):
            if discussion.get('id', 0) > max_id:
                max_id = discussion['id']
        new_id = max_id + 1
        
        # Create new discussion
        new_discussion = {
            'id': new_id,
            'name': name,
            'title': title,
            'description': description,
            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'likes': 0,
            'dislikes': 0,
            'replies': []
        }
        
        community_data['discussions'].insert(0, new_discussion)  # Add to beginning
        save_community_data(community_data)
        
        return jsonify({'success': True, 'discussion': new_discussion})
        
    except Exception as e:
        app.logger.error(f"Error creating discussion: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/community/reply', methods=['POST'])
def add_discussion_reply():
    """Add a reply to a discussion"""
    try:
        data = request.json
        discussion_id = data.get('discussion_id')
        name = data.get('name', 'Anonymous').strip()  
        message = data.get('message', '').strip()
        
        if not discussion_id or not message:
            return jsonify({'success': False, 'error': 'Discussion ID and message are required'}), 400
        
        community_data = load_community_data()
        
        # Find the discussion
        discussion_found = False
        for discussion in community_data.get('discussions', []):
            if discussion['id'] == discussion_id:
                discussion_found = True
                
                # Initialize replies if not present
                if 'replies' not in discussion:
                    discussion['replies'] = []
                
                # Generate unique reply ID within discussion
                reply_id = len(discussion['replies']) + 1
                
                # Add new reply
                new_reply = {
                    'id': reply_id,
                    'name': name,
                    'message': message,
                    'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'likes': 0,
                    'dislikes': 0
                }
                
                discussion['replies'].append(new_reply)
                break
        
        if not discussion_found:
            return jsonify({'success': False, 'error': 'Discussion not found'}), 404
        
        save_community_data(community_data)
        
        return jsonify({'success': True})
        
    except Exception as e:
        app.logger.error(f"Error adding reply: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/community/reply/vote/<int:discussion_id>/<int:reply_id>', methods=['POST'])
def vote_reply(discussion_id, reply_id):
    """Vote on a community reply"""
    try:
        data = request.json
        vote_type = data.get('vote_type')  # 'like' or 'dislike'
        
        if vote_type not in ['like', 'dislike']:
            return jsonify({'success': False, 'error': 'Invalid vote type'}), 400
        
        community_data = load_community_data()
        
        # Find the discussion and reply
        reply_found = False
        for discussion in community_data.get('discussions', []):
            if discussion['id'] == discussion_id:
                for reply in discussion.get('replies', []):
                    if reply['id'] == reply_id:
                        reply_found = True
                        
                        # Initialize vote counts if not present
                        if 'likes' not in reply:
                            reply['likes'] = 0
                        if 'dislikes' not in reply:
                            reply['dislikes'] = 0
                        
                        # Update vote count
                        if vote_type == 'like':
                            reply['likes'] += 1
                        else:  # dislike
                            reply['dislikes'] += 1
                        
                        break
                break
        
        if not reply_found:
            return jsonify({'success': False, 'error': 'Reply not found'}), 404
        
        save_community_data(community_data)
        
        return jsonify({'success': True})
        
    except Exception as e:
        app.logger.error(f"Error voting on reply: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/clubs')
def clubs():
    """Student Clubs page"""
    clubs_data = load_clubs_data()
    return render_template('clubs.html', clubs=clubs_data.get('clubs', []))

@app.route('/clubs/add')
def add_club():
    """Add new club page (admin only)"""
    # Simple admin check via URL parameter
    if request.args.get('admin') != 'true':
        flash('Admin access required to add clubs.', 'error')
        return redirect(url_for('clubs'))
    
    return render_template('add_club.html')

@app.route('/clubs/add', methods=['POST'])
def add_club_post():
    """Handle club addition"""
    try:
        # Simple admin check
        if request.args.get('admin') != 'true':
            flash('Admin access required to add clubs.', 'error')
            return redirect(url_for('clubs'))
        
        club_name = request.form.get('club_name', '').strip()
        description = request.form.get('description', '').strip()
        instagram_link = request.form.get('instagram_link', '').strip()
        
        if not club_name:
            flash('Club name is required.', 'error')
            return redirect(url_for('add_club') + '?admin=true')
        
        # Handle file upload
        screenshot_filename = None
        if 'instagram_screenshot' in request.files:
            file = request.files['instagram_screenshot']
            if file and file.filename:
                # Create clubs upload directory
                clubs_upload_dir = os.path.join(UPLOAD_FOLDER, 'clubs')
                os.makedirs(clubs_upload_dir, exist_ok=True)
                
                # Secure filename and save
                filename = secure_filename(file.filename)
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_')
                screenshot_filename = timestamp + filename
                file_path = os.path.join(clubs_upload_dir, screenshot_filename)
                file.save(file_path)
        
        # Load existing clubs data
        clubs_data = load_clubs_data()
        
        # Create new club entry
        new_club = {
            'id': clubs_data.get('next_id', 1),
            'name': club_name,
            'description': description if description else None,
            'instagram_link': instagram_link if instagram_link else None,
            'instagram_screenshot': screenshot_filename,
            'created_at': datetime.now().isoformat()
        }
        
        # Add to clubs list and update next_id
        clubs_data['clubs'].append(new_club)
        clubs_data['next_id'] = clubs_data.get('next_id', 1) + 1
        
        # Save to file
        save_clubs_data(clubs_data)
        
        flash(f'Club "{club_name}" added successfully!', 'success')
        return redirect(url_for('clubs'))
        
    except Exception as e:
        app.logger.error(f"Error adding club: {str(e)}")
        flash(f'Error adding club: {str(e)}', 'error')
        return redirect(url_for('add_club') + '?admin=true')

@app.route('/clubs/screenshot/<filename>')
def club_screenshot(filename):
    """Serve club screenshots securely"""
    try:
        # Security check: ensure filename doesn't contain path traversal
        if '..' in filename or filename.startswith('/'):
            app.logger.warning(f"Invalid file path attempted: {filename}")
            return "Invalid file path", 400
        
        clubs_dir = os.path.join(UPLOAD_FOLDER, 'clubs')
        file_path = os.path.join(clubs_dir, filename)
        
        # Check if file exists
        if not os.path.exists(file_path):
            app.logger.error(f"Club screenshot not found: {file_path}")
            return "File not found", 404
        
        # Verify file is within clubs directory (fix path normalization)
        clubs_dir_abs = os.path.abspath(clubs_dir)
        file_path_abs = os.path.abspath(file_path)
        if not file_path_abs.startswith(clubs_dir_abs):
            app.logger.warning(f"File path outside clubs directory: {file_path_abs}")
            return "Invalid file path", 400
            
        return send_from_directory(clubs_dir_abs, filename, as_attachment=False)
    except Exception as e:
        app.logger.error(f"Error serving club screenshot {filename}: {str(e)}")
        return f"Error serving file: {str(e)}", 500

@app.route('/admin/clubs/delete/<int:club_id>', methods=['POST'])
def delete_club(club_id):
    """Delete a club (admin only)"""
    try:
        # Simple admin check
        if request.args.get('admin') != 'true':
            return jsonify({'success': False, 'error': 'Admin access required'}), 403
        
        clubs_data = load_clubs_data()
        clubs = clubs_data.get('clubs', [])
        
        # Find and remove the club
        club_found = False
        club_to_delete = None
        for i, club in enumerate(clubs):
            if club['id'] == club_id:
                club_to_delete = clubs.pop(i)
                club_found = True
                break
        
        if not club_found:
            return jsonify({'success': False, 'error': 'Club not found'}), 404
        
        # Delete screenshot file if exists
        if club_to_delete and club_to_delete.get('instagram_screenshot'):
            screenshot_path = os.path.join(UPLOAD_FOLDER, 'clubs', club_to_delete['instagram_screenshot'])
            if os.path.exists(screenshot_path):
                try:
                    os.remove(screenshot_path)
                except Exception as e:
                    app.logger.warning(f"Could not delete screenshot file: {str(e)}")
        
        # Save updated data
        save_clubs_data(clubs_data)
        
        return jsonify({'success': True})
        
    except Exception as e:
        app.logger.error(f"Error deleting club: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

# Bus Routes Routes
@app.route('/bus-routes')
def bus_routes():
    """Bus Routes page showing all uploaded routes"""
    try:
        data = load_transportation_data()
        bus_routes = data.get('bus_routes', [])
        
        # Sort by upload date (newest first)
        bus_routes = sorted(bus_routes, key=lambda x: x.get('upload_date', ''), reverse=True)
        
        # Check if user is admin (simple check)
        is_admin = request.args.get('admin') == 'true'
        
        return render_template('bus_routes.html', 
                             bus_routes=bus_routes,
                             is_admin=is_admin)
    except Exception as e:
        app.logger.error(f"Error loading bus routes: {str(e)}")
        flash('Error loading bus routes', 'error')
        return redirect(url_for('index'))

@app.route('/bus-routes/upload', methods=['POST'])
def upload_bus_route():
    """Upload new bus route file (admin only)"""
    try:
        # Simple admin check
        if request.args.get('admin') != 'true':
            flash('Admin access required', 'error')
            return redirect(url_for('bus_routes'))
        
        if 'file' not in request.files:
            flash('No file selected', 'error')
            return redirect(url_for('bus_routes') + '?admin=true')
        
        file = request.files['file']
        if file.filename == '':
            flash('No file selected', 'error')
            return redirect(url_for('bus_routes') + '?admin=true')
        
        # Get form data
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        
        if not title:
            flash('Title is required', 'error')
            return redirect(url_for('bus_routes') + '?admin=true')
        
        if file and file.filename and allowed_file(file.filename):
            # Load existing data
            data = load_transportation_data()
            
            # Generate unique filename
            original_filename = file.filename
            filename = secure_filename(original_filename)
            
            if not filename or filename == '':
                raise ValueError("Invalid filename after security processing")
            
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            unique_filename = f"bus_route_{timestamp}_{filename}"
            
            # Create uploads/bus_routes directory
            bus_routes_dir = os.path.join(UPLOAD_FOLDER, 'bus_routes')
            os.makedirs(bus_routes_dir, exist_ok=True)
            
            filepath = os.path.join(bus_routes_dir, unique_filename)
            
            # Save file
            file.save(filepath)
            
            # Verify file was saved
            if not os.path.exists(filepath):
                raise IOError("File was not saved successfully")
            
            # Get file info
            file_size = os.path.getsize(filepath)
            file_extension = filename.rsplit('.', 1)[1].lower()
            
            # Generate unique ID
            new_id = data.get('next_id', 1)
            data['next_id'] = new_id + 1
            
            # Create file info
            file_info = {
                'id': new_id,
                'title': title,
                'description': description,
                'filename': unique_filename,
                'original_filename': original_filename,
                'file_size': file_size,
                'file_extension': file_extension,
                'size': f"{file_size / (1024*1024):.1f} MB" if file_size > 1024*1024 else f"{file_size / 1024:.1f} KB",
                'upload_date': datetime.now().isoformat(),
                'file_path': filepath,
                'likes': 0,
                'dislikes': 0,
                'comments': []
            }
            
            data['bus_routes'].append(file_info)
            save_transportation_data(data)
            
            flash('Bus route uploaded successfully!', 'success')
            
        else:
            flash('Invalid file type. Please upload PDF or image files.', 'error')
    
    except Exception as e:
        app.logger.error(f"Bus route upload error: {str(e)}")
        flash(f'Upload error: {str(e)}', 'error')
    
    return redirect(url_for('bus_routes') + '?admin=true')

@app.route('/bus-routes/download/<int:file_id>')
def download_bus_route(file_id):
    """Download bus route file"""
    try:
        data = load_transportation_data()
        file_data = None
        
        for f in data.get('bus_routes', []):
            if f['id'] == file_id:
                file_data = f
                break
        
        if not file_data:
            flash('File not found', 'error')
            return redirect(url_for('bus_routes'))
        
        filepath = file_data['file_path']
        if os.path.exists(filepath) and os.path.isfile(filepath):
            return send_file(filepath, as_attachment=True, download_name=file_data['original_filename'])
        else:
            flash('File not found on disk', 'error')
            return redirect(url_for('bus_routes'))
    
    except Exception as e:
        app.logger.error(f"Bus route download error: {str(e)}")
        flash('Error downloading file', 'error')
        return redirect(url_for('bus_routes'))

@app.route('/bus-routes/delete/<int:file_id>', methods=['POST'])
def delete_bus_route(file_id):
    """Delete bus route file (admin only)"""
    try:
        # Simple admin check
        if request.args.get('admin') != 'true':
            return jsonify({'success': False, 'error': 'Admin access required'}), 403
        
        data = load_transportation_data()
        file_data = None
        file_index = -1
        
        for i, f in enumerate(data.get('bus_routes', [])):
            if f['id'] == file_id:
                file_data = f
                file_index = i
                break
        
        if not file_data:
            return jsonify({'success': False, 'error': 'File not found'}), 404
        
        # Delete physical file
        filepath = file_data['file_path']
        if os.path.exists(filepath) and os.path.isfile(filepath):
            os.remove(filepath)
        
        # Remove from data
        data['bus_routes'].pop(file_index)
        save_transportation_data(data)
        
        return jsonify({'success': True})
        
    except Exception as e:
        app.logger.error(f"Error deleting bus route: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/bus-routes/file/<filename>')
def bus_route_file(filename):
    """Serve bus route files securely"""
    try:
        # Security check: ensure filename doesn't contain path traversal
        if '..' in filename or filename.startswith('/'):
            app.logger.warning(f"Invalid file path attempted: {filename}")
            return "Invalid file path", 400
        
        bus_routes_dir = os.path.join(UPLOAD_FOLDER, 'bus_routes')
        file_path = os.path.join(bus_routes_dir, filename)
        
        # Check if file exists
        if not os.path.exists(file_path):
            app.logger.error(f"Bus route file not found: {file_path}")
            return "File not found", 404
        
        # Verify file is within bus_routes directory
        bus_routes_dir_abs = os.path.abspath(bus_routes_dir)
        file_path_abs = os.path.abspath(file_path)
        if not file_path_abs.startswith(bus_routes_dir_abs):
            app.logger.warning(f"File path outside bus_routes directory: {file_path_abs}")
            return "Invalid file path", 400
            
        return send_from_directory(bus_routes_dir_abs, filename, as_attachment=False)
    except Exception as e:
        app.logger.error(f"Error serving bus route file {filename}: {str(e)}")
        return f"Error serving file: {str(e)}", 500

@app.route('/bus-routes/vote/<int:file_id>', methods=['POST'])
def vote_bus_route(file_id):
    """Handle like/dislike votes for bus route files"""
    try:
        vote_type = request.json.get('vote_type')
        if vote_type not in ['like', 'dislike']:
            return jsonify({'error': 'Invalid vote type'}), 400
        
        data = load_transportation_data()
        file_data = None
        
        for file_item in data.get('bus_routes', []):
            if file_item['id'] == file_id:
                file_data = file_item
                break
        
        if not file_data:
            return jsonify({'error': 'File not found'}), 404
        
        # Update vote counts
        if vote_type == 'like':
            file_data['likes'] = file_data.get('likes', 0) + 1
        else:
            file_data['dislikes'] = file_data.get('dislikes', 0) + 1
        
        save_transportation_data(data)
        
        return jsonify({
            'success': True,
            'likes': file_data.get('likes', 0),
            'dislikes': file_data.get('dislikes', 0)
        })
    
    except Exception as e:
        app.logger.error(f"Bus route vote error: {str(e)}")
        return jsonify({'error': 'Failed to process vote'}), 500

@app.route('/bus-routes/comment/<int:file_id>', methods=['POST'])
def add_bus_route_comment(file_id):
    """Add a comment to a bus route file"""
    try:
        comment_text = request.json.get('comment', '').strip()
        commenter_name = request.json.get('name', '').strip()
        
        if not comment_text:
            return jsonify({'error': 'Comment text is required'}), 400
        
        if not commenter_name:
            commenter_name = 'Anonymous'
        
        data = load_transportation_data()
        file_data = None
        
        for file_item in data.get('bus_routes', []):
            if file_item['id'] == file_id:
                file_data = file_item
                break
        
        if not file_data:
            return jsonify({'error': 'File not found'}), 404
        
        # Add comment
        new_comment = {
            'name': commenter_name,
            'comment': comment_text,
            'timestamp': datetime.now().isoformat()
        }
        
        if 'comments' not in file_data:
            file_data['comments'] = []
        
        file_data['comments'].append(new_comment)
        save_transportation_data(data)
        
        return jsonify({
            'success': True,
            'comment': new_comment
        })
    
    except Exception as e:
        app.logger.error(f"Bus route comment error: {str(e)}")
        return jsonify({'error': 'Failed to add comment'}), 500

@app.route('/bus-routes/detail/<int:file_id>')
def bus_route_detail(file_id):
    """Display detailed view of a bus route file"""
    try:
        data = load_transportation_data()
        file_data = None
        
        for file_item in data.get('bus_routes', []):
            if file_item['id'] == file_id:
                file_data = file_item
                break
        
        if not file_data:
            flash('File not found', 'error')
            return redirect(url_for('bus_routes'))
        
        # Check if user is admin
        is_admin = request.args.get('admin') == 'true'
        
        return render_template('bus_route_detail.html', 
                             file_data=file_data,
                             is_admin=is_admin)
    
    except Exception as e:
        app.logger.error(f"Error loading bus route detail: {str(e)}")
        flash('Error loading file details', 'error')
        return redirect(url_for('bus_routes'))

# Canteen Routes
@app.route('/canteen')
def canteen():
    """Canteen page showing all canteens"""
    try:
        data = load_canteen_data()
        canteens = data.get('canteens', [])
        
        # Sort by upload date (newest first)
        canteens = sorted(canteens, key=lambda x: x.get('date_added', ''), reverse=True)
        
        return render_template('canteen.html', canteens=canteens)
    except Exception as e:
        app.logger.error(f"Error loading canteen data: {str(e)}")
        flash('Error loading canteen information', 'error')
        return redirect(url_for('index'))

@app.route('/canteen/add', methods=['POST'])
def add_canteen():
    """Add new canteen (admin functionality)"""
    try:
        canteen_name = request.form.get('canteen_name', '').strip()
        canteen_description = request.form.get('canteen_description', '').strip()
        
        if not canteen_name:
            flash('Canteen name is required', 'error')
            return redirect(url_for('canteen'))
        
        # Handle file upload
        if 'canteen_photo' not in request.files:
            flash('Canteen photo is required', 'error')
            return redirect(url_for('canteen'))
        
        file = request.files['canteen_photo']
        if file.filename == '':
            flash('No file selected', 'error')
            return redirect(url_for('canteen'))
        
        # Check file extension
        file_ext = file.filename.rsplit('.', 1)[1].lower() if '.' in file.filename else ''
        if file_ext not in ['jpg', 'jpeg', 'png']:
            flash('Only JPG and PNG images are allowed', 'error')
            return redirect(url_for('canteen'))
        
        # Create canteen directory if it doesn't exist
        canteen_dir = os.path.join(UPLOAD_FOLDER, 'canteen')
        os.makedirs(canteen_dir, exist_ok=True)
        
        # Generate secure filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        secure_name = secure_filename(file.filename)
        filename = f"canteen_{timestamp}_{secure_name}"
        file_path = os.path.join(canteen_dir, filename)
        
        # Save file
        file.save(file_path)
        
        # Load existing data
        data = load_canteen_data()
        
        # Create new canteen entry
        new_canteen = {
            'id': data.get('next_id', 1),
            'name': canteen_name,
            'description': canteen_description,
            'photo_filename': filename,
            'photo_path': file_path,
            'date_added': datetime.now().isoformat()
        }
        
        # Add to data
        if 'canteens' not in data:
            data['canteens'] = []
        
        data['canteens'].append(new_canteen)
        data['next_id'] = data.get('next_id', 1) + 1
        
        # Save data
        save_canteen_data(data)
        
        flash('Canteen added successfully!', 'success')
        return redirect(url_for('canteen'))
        
    except Exception as e:
        app.logger.error(f"Error adding canteen: {str(e)}")
        flash('Error adding canteen', 'error')
        return redirect(url_for('canteen'))

@app.route('/canteen/delete/<int:canteen_id>', methods=['POST'])
def delete_canteen(canteen_id):
    """Delete canteen (admin only)"""
    try:
        data = load_canteen_data()
        canteen_found = False
        canteen_to_delete = None
        
        for i, canteen in enumerate(data.get('canteens', [])):
            if canteen['id'] == canteen_id:
                canteen_to_delete = data['canteens'].pop(i)
                canteen_found = True
                break
        
        if not canteen_found:
            return jsonify({'success': False, 'error': 'Canteen not found'}), 404
        
        # Delete photo file if exists
        if canteen_to_delete and canteen_to_delete.get('photo_path'):
            photo_path = canteen_to_delete['photo_path']
            if os.path.exists(photo_path):
                try:
                    os.remove(photo_path)
                except Exception as e:
                    app.logger.warning(f"Could not delete photo file: {str(e)}")
        
        # Save updated data
        save_canteen_data(data)
        
        return jsonify({'success': True})
        
    except Exception as e:
        app.logger.error(f"Error deleting canteen: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/canteen/photo/<filename>')
def canteen_photo(filename):
    """Serve canteen photos securely"""
    try:
        # Security check: ensure filename doesn't contain path traversal
        if '..' in filename or filename.startswith('/'):
            app.logger.warning(f"Invalid file path attempted: {filename}")
            return "Invalid file path", 400
        
        canteen_dir = os.path.join(UPLOAD_FOLDER, 'canteen')
        file_path = os.path.join(canteen_dir, filename)
        
        # Check if file exists
        if not os.path.exists(file_path):
            app.logger.error(f"Canteen photo not found: {file_path}")
            return "File not found", 404
        
        # Verify file is within canteen directory
        canteen_dir_abs = os.path.abspath(canteen_dir)
        file_path_abs = os.path.abspath(file_path)
        if not file_path_abs.startswith(canteen_dir_abs):
            app.logger.warning(f"File path outside canteen directory: {file_path_abs}")
            return "Invalid file path", 400
            
        return send_from_directory(canteen_dir_abs, filename, as_attachment=False)
    except Exception as e:
        app.logger.error(f"Error serving canteen photo {filename}: {str(e)}")
        return f"Error serving file: {str(e)}", 500

# Campus Places Routes
@app.route('/places')
def campus_places():
    """Campus Places page showing all places"""
    try:
        data = load_places_data()
        places = data.get('places', [])
        
        # Sort by upload date (newest first)
        places = sorted(places, key=lambda x: x.get('date_added', ''), reverse=True)
        
        return render_template('campus_places.html', places=places)
    except Exception as e:
        app.logger.error(f"Error loading places data: {str(e)}")
        flash('Error loading places information', 'error')
        return redirect(url_for('index'))

@app.route('/places/add', methods=['POST'])
def add_place():
    """Add new campus place"""
    try:
        place_name = request.form.get('place_name', '').strip()
        place_description = request.form.get('place_description', '').strip()
        maps_link = request.form.get('maps_link', '').strip()
        
        if not place_name:
            flash('Place name is required', 'error')
            return redirect(url_for('campus_places'))
        
        # Handle optional file upload
        photo_filename = None
        photo_path = None
        
        if 'place_photo' in request.files:
            file = request.files['place_photo']
            if file and file.filename and file.filename != '':
                # Check file extension
                file_ext = file.filename.rsplit('.', 1)[1].lower() if '.' in file.filename else ''
                if file_ext not in ['jpg', 'jpeg', 'png']:
                    flash('Only JPG and PNG images are allowed', 'error')
                    return redirect(url_for('campus_places'))
                
                # Create places directory if it doesn't exist
                places_dir = os.path.join(UPLOAD_FOLDER, 'places')
                os.makedirs(places_dir, exist_ok=True)
                
                # Generate secure filename
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                secure_name = secure_filename(file.filename)
                photo_filename = f"place_{timestamp}_{secure_name}"
                photo_path = os.path.join(places_dir, photo_filename)
                
                # Save file
                file.save(photo_path)
        
        # Load existing data
        data = load_places_data()
        
        # Create new place entry
        new_place = {
            'id': data.get('next_id', 1),
            'name': place_name,
            'description': place_description,
            'maps_link': maps_link,
            'photo_filename': photo_filename,
            'photo_path': photo_path,
            'date_added': datetime.now().isoformat()
        }
        
        # Add to data
        if 'places' not in data:
            data['places'] = []
        
        data['places'].append(new_place)
        data['next_id'] = data.get('next_id', 1) + 1
        
        # Save data
        save_places_data(data)
        
        flash('Campus place added successfully!', 'success')
        return redirect(url_for('campus_places'))
        
    except Exception as e:
        app.logger.error(f"Error adding place: {str(e)}")
        flash('Error adding place', 'error')
        return redirect(url_for('campus_places'))

@app.route('/places/delete/<int:place_id>', methods=['POST'])
def delete_place(place_id):
    """Delete campus place (admin only)"""
    try:
        data = load_places_data()
        place_found = False
        place_to_delete = None
        
        for i, place in enumerate(data.get('places', [])):
            if place['id'] == place_id:
                place_to_delete = data['places'].pop(i)
                place_found = True
                break
        
        if not place_found:
            return jsonify({'success': False, 'error': 'Place not found'}), 404
        
        # Delete photo file if exists
        if place_to_delete and place_to_delete.get('photo_path'):
            photo_path = place_to_delete['photo_path']
            if os.path.exists(photo_path):
                try:
                    os.remove(photo_path)
                except Exception as e:
                    app.logger.warning(f"Could not delete photo file: {str(e)}")
        
        # Save updated data
        save_places_data(data)
        
        return jsonify({'success': True})
        
    except Exception as e:
        app.logger.error(f"Error deleting place: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/places/photo/<filename>')
def place_photo(filename):
    """Serve place photos securely"""
    try:
        # Security check: ensure filename doesn't contain path traversal
        if '..' in filename or filename.startswith('/'):
            app.logger.warning(f"Invalid file path attempted: {filename}")
            return "Invalid file path", 400
        
        places_dir = os.path.join(UPLOAD_FOLDER, 'places')
        file_path = os.path.join(places_dir, filename)
        
        # Check if file exists
        if not os.path.exists(file_path):
            app.logger.error(f"Place photo not found: {file_path}")
            return "File not found", 404
        
        # Verify file is within places directory
        places_dir_abs = os.path.abspath(places_dir)
        file_path_abs = os.path.abspath(file_path)
        if not file_path_abs.startswith(places_dir_abs):
            app.logger.warning(f"File path outside places directory: {file_path_abs}")
            return "Invalid file path", 400
            
        return send_from_directory(places_dir_abs, filename, as_attachment=False)
    except Exception as e:
        app.logger.error(f"Error serving place photo {filename}: {str(e)}")
        return f"Error serving file: {str(e)}", 500

# Hostel Information Routes
@app.route('/hostels')
def hostel_info():
    """Hostel Information page showing all hostels"""
    try:
        data = load_hostels_data()
        hostels = data.get('hostels', [])
        
        # Sort by upload date (newest first)
        hostels = sorted(hostels, key=lambda x: x.get('date_added', ''), reverse=True)
        
        return render_template('hostel_info.html', hostels=hostels)
    except Exception as e:
        app.logger.error(f"Error loading hostels data: {str(e)}")
        flash('Error loading hostel information', 'error')
        return redirect(url_for('index'))

@app.route('/hostels/add', methods=['POST'])
def add_hostel():
    """Add new hostel information"""
    try:
        hostel_name = request.form.get('hostel_name', '').strip()
        hostel_category = request.form.get('hostel_category', '').strip()
        hostel_description = request.form.get('hostel_description', '').strip()
        maps_link = request.form.get('maps_link', '').strip()
        basic_rules = request.form.get('basic_rules', '').strip()
        
        # Get facilities (checkboxes)
        facilities = request.form.getlist('facilities')
        
        if not hostel_name:
            flash('Hostel name is required', 'error')
            return redirect(url_for('hostel_info'))
        
        if not hostel_category or hostel_category not in ['Boys', 'Girls']:
            flash('Please select a valid hostel category', 'error')
            return redirect(url_for('hostel_info'))
        
        # Handle required file upload
        if 'hostel_photo' not in request.files:
            flash('Hostel photo is required', 'error')
            return redirect(url_for('hostel_info'))
        
        file = request.files['hostel_photo']
        if file.filename == '':
            flash('No file selected', 'error')
            return redirect(url_for('hostel_info'))
        
        # Check file extension
        file_ext = file.filename.rsplit('.', 1)[1].lower() if '.' in file.filename else ''
        if file_ext not in ['jpg', 'jpeg', 'png']:
            flash('Only JPG and PNG images are allowed', 'error')
            return redirect(url_for('hostel_info'))
        
        # Create hostels directory if it doesn't exist
        hostels_dir = os.path.join(UPLOAD_FOLDER, 'hostels')
        os.makedirs(hostels_dir, exist_ok=True)
        
        # Generate secure filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        secure_name = secure_filename(file.filename)
        photo_filename = f"hostel_{timestamp}_{secure_name}"
        photo_path = os.path.join(hostels_dir, photo_filename)
        
        # Save file
        file.save(photo_path)
        
        # Load existing data
        data = load_hostels_data()
        
        # Create new hostel entry
        new_hostel = {
            'id': data.get('next_id', 1),
            'name': hostel_name,
            'category': hostel_category,
            'description': hostel_description,
            'maps_link': maps_link,
            'facilities': facilities,
            'basic_rules': basic_rules,
            'photo_filename': photo_filename,
            'photo_path': photo_path,
            'date_added': datetime.now().isoformat()
        }
        
        # Add to data
        if 'hostels' not in data:
            data['hostels'] = []
        
        data['hostels'].append(new_hostel)
        data['next_id'] = data.get('next_id', 1) + 1
        
        # Save data
        save_hostels_data(data)
        
        flash('Hostel information added successfully!', 'success')
        return redirect(url_for('hostel_info'))
        
    except Exception as e:
        app.logger.error(f"Error adding hostel: {str(e)}")
        flash('Error adding hostel information', 'error')
        return redirect(url_for('hostel_info'))

@app.route('/hostels/delete/<int:hostel_id>', methods=['POST'])
def delete_hostel(hostel_id):
    """Delete hostel information (admin only)"""
    try:
        data = load_hostels_data()
        hostel_found = False
        hostel_to_delete = None
        
        for i, hostel in enumerate(data.get('hostels', [])):
            if hostel['id'] == hostel_id:
                hostel_to_delete = data['hostels'].pop(i)
                hostel_found = True
                break
        
        if not hostel_found:
            return jsonify({'success': False, 'error': 'Hostel not found'}), 404
        
        # Delete photo file if exists
        if hostel_to_delete and hostel_to_delete.get('photo_path'):
            photo_path = hostel_to_delete['photo_path']
            if os.path.exists(photo_path):
                try:
                    os.remove(photo_path)
                except Exception as e:
                    app.logger.warning(f"Could not delete photo file: {str(e)}")
        
        # Save updated data
        save_hostels_data(data)
        
        return jsonify({'success': True})
        
    except Exception as e:
        app.logger.error(f"Error deleting hostel: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/hostels/photo/<filename>')
def hostel_photo(filename):
    """Serve hostel photos securely"""
    try:
        # Security check: ensure filename doesn't contain path traversal
        if '..' in filename or filename.startswith('/'):
            app.logger.warning(f"Invalid file path attempted: {filename}")
            return "Invalid file path", 400
        
        hostels_dir = os.path.join(UPLOAD_FOLDER, 'hostels')
        file_path = os.path.join(hostels_dir, filename)
        
        # Check if file exists
        if not os.path.exists(file_path):
            app.logger.error(f"Hostel photo not found: {file_path}")
            return "File not found", 404
        
        # Verify file is within hostels directory
        hostels_dir_abs = os.path.abspath(hostels_dir)
        file_path_abs = os.path.abspath(file_path)
        if not file_path_abs.startswith(hostels_dir_abs):
            app.logger.warning(f"File path outside hostels directory: {file_path_abs}")
            return "Invalid file path", 400
            
        return send_from_directory(hostels_dir_abs, filename, as_attachment=False)
    except Exception as e:
        app.logger.error(f"Error serving hostel photo {filename}: {str(e)}")
        return f"Error serving file: {str(e)}", 500

# Upcoming Events Routes
@app.route('/events')
def upcoming_events():
    """Upcoming Events page showing all events"""
    try:
        data = load_events_data()
        events = data.get('events', [])
        
        # Sort events by date (upcoming first)
        from datetime import datetime
        current_time = datetime.now()
        
        # Parse dates and sort
        upcoming_events = []
        past_events = []
        
        for event in events:
            try:
                event_datetime = datetime.fromisoformat(event.get('event_datetime', ''))
                if event_datetime >= current_time:
                    upcoming_events.append(event)
                else:
                    past_events.append(event)
            except:
                # If date parsing fails, treat as upcoming
                upcoming_events.append(event)
        
        # Sort upcoming events by date (nearest first)
        upcoming_events.sort(key=lambda x: x.get('event_datetime', ''))
        # Sort past events by date (most recent first)
        past_events.sort(key=lambda x: x.get('event_datetime', ''), reverse=True)
        
        # Combine lists (upcoming first)
        sorted_events = upcoming_events + past_events
        
        return render_template('upcoming_events.html', events=sorted_events, upcoming_count=len(upcoming_events))
    except Exception as e:
        app.logger.error(f"Error loading events data: {str(e)}")
        flash('Error loading events', 'error')
        return redirect(url_for('index'))

@app.route('/events/add', methods=['POST'])
def add_event():
    """Add new event"""
    try:
        event_name = request.form.get('event_name', '').strip()
        event_description = request.form.get('event_description', '').strip()
        event_date = request.form.get('event_date', '').strip()
        event_time = request.form.get('event_time', '').strip()
        event_category = request.form.get('event_category', '').strip()
        registration_link = request.form.get('registration_link', '').strip()
        
        if not event_name:
            flash('Event name is required', 'error')
            return redirect(url_for('upcoming_events'))
        
        if not event_date or not event_time:
            flash('Event date and time are required', 'error')
            return redirect(url_for('upcoming_events'))
        
        # Valid categories
        valid_categories = ['Tech Fest', 'Cultural Fest', 'Hackathon', 'Orientation', 'Induction', 'Entrance Exam', 'Others']
        if not event_category or event_category not in valid_categories:
            flash('Please select a valid event category', 'error')
            return redirect(url_for('upcoming_events'))
        
        # Combine date and time
        try:
            from datetime import datetime
            event_datetime = datetime.strptime(f"{event_date} {event_time}", "%Y-%m-%d %H:%M").isoformat()
        except ValueError:
            flash('Invalid date or time format', 'error')
            return redirect(url_for('upcoming_events'))
        
        # Handle optional poster upload
        poster_filename = None
        if 'poster_image' in request.files:
            file = request.files['poster_image']
            if file and file.filename != '':
                # Check file extension
                file_ext = file.filename.rsplit('.', 1)[1].lower() if '.' in file.filename else ''
                if file_ext not in ['jpg', 'jpeg', 'png']:
                    flash('Only JPG and PNG images are allowed for poster', 'error')
                    return redirect(url_for('upcoming_events'))
                
                # Create events directory if it doesn't exist
                events_dir = os.path.join(UPLOAD_FOLDER, 'events')
                os.makedirs(events_dir, exist_ok=True)
                
                # Generate secure filename
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                secure_name = secure_filename(file.filename)
                poster_filename = f"event_{timestamp}_{secure_name}"
                poster_path = os.path.join(events_dir, poster_filename)
                
                # Save file
                file.save(poster_path)
        
        # Load existing data
        data = load_events_data()
        
        # Create new event entry
        new_event = {
            'id': data.get('next_id', 1),
            'name': event_name,
            'description': event_description,
            'event_datetime': event_datetime,
            'category': event_category,
            'registration_link': registration_link,
            'poster_filename': poster_filename,
            'date_added': datetime.now().isoformat()
        }
        
        # Add to data
        if 'events' not in data:
            data['events'] = []
        
        data['events'].append(new_event)
        data['next_id'] = data.get('next_id', 1) + 1
        
        # Save data
        save_events_data(data)
        
        flash('Event added successfully!', 'success')
        return redirect(url_for('upcoming_events'))
        
    except Exception as e:
        app.logger.error(f"Error adding event: {str(e)}")
        flash('Error adding event', 'error')
        return redirect(url_for('upcoming_events'))

@app.route('/events/delete/<int:event_id>', methods=['POST'])
def delete_event(event_id):
    """Delete event (admin only)"""
    try:
        data = load_events_data()
        event_found = False
        event_to_delete = None
        
        for i, event in enumerate(data.get('events', [])):
            if event['id'] == event_id:
                event_to_delete = data['events'].pop(i)
                event_found = True
                break
        
        if not event_found:
            return jsonify({'success': False, 'error': 'Event not found'}), 404
        
        # Delete poster file if exists
        if event_to_delete and event_to_delete.get('poster_filename'):
            poster_path = os.path.join(UPLOAD_FOLDER, 'events', event_to_delete['poster_filename'])
            if os.path.exists(poster_path):
                try:
                    os.remove(poster_path)
                except Exception as e:
                    app.logger.warning(f"Could not delete poster file: {str(e)}")
        
        # Save updated data
        save_events_data(data)
        
        return jsonify({'success': True})
        
    except Exception as e:
        app.logger.error(f"Error deleting event: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/events/poster/<filename>')
def event_poster(filename):
    """Serve event poster images securely"""
    try:
        # Security check: ensure filename doesn't contain path traversal
        if '..' in filename or filename.startswith('/'):
            app.logger.warning(f"Invalid file path attempted: {filename}")
            return "Invalid file path", 400
        
        events_dir = os.path.join(UPLOAD_FOLDER, 'events')
        file_path = os.path.join(events_dir, filename)
        
        # Check if file exists
        if not os.path.exists(file_path):
            app.logger.error(f"Event poster not found: {file_path}")
            return "File not found", 404
        
        # Verify file is within events directory
        events_dir_abs = os.path.abspath(events_dir)
        file_path_abs = os.path.abspath(file_path)
        if not file_path_abs.startswith(events_dir_abs):
            app.logger.warning(f"File path outside events directory: {file_path_abs}")
            return "Invalid file path", 400
            
        return send_from_directory(events_dir_abs, filename, as_attachment=False)
    except Exception as e:
        app.logger.error(f"Error serving event poster {filename}: {str(e)}")
        return f"Error serving file: {str(e)}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)