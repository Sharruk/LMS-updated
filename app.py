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
app.secret_key = os.environ.get("SESSION_SECRET")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///tn_board_portal.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}
db.init_app(app)

with app.app_context():
    import models  # noqa: F401
    db.create_all()

# Configuration
UPLOAD_FOLDER = 'uploads'
DATA_FILE = 'data.json'
MAX_FILE_SIZE = None
ALLOWED_EXTENSIONS = {'pdf'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def load_data():
    """Load data from JSON file"""
    try:
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r') as f:
                data = json.load(f)
        else:
            data = {"classes": {}, "files": [], "exam_categories": []}

        # Ensure standard hierarchy exists
        if 'classes' not in data:
            data['classes'] = {}
        
        # Standard subjects for Class 9 & 10
        common_subjects = {
            "tamil": "Tamil",
            "english": "English",
            "maths": "Mathematics",
            "science": "Science",
            "social": "Social Science"
        }
        
        # Higher secondary subjects for Class 11 & 12
        hs_subjects = {
            "tamil": "Tamil",
            "english": "English",
            "maths": "Mathematics",
            "physics": "Physics",
            "chemistry": "Chemistry",
            "biology": "Biology",
            "csc": "Computer Science",
            "capp": "Computer Applications",
            "acc": "Accountancy",
            "comm": "Commerce",
            "eco": "Economics"
        }

        for cid in ["9", "10"]:
            if cid not in data['classes']:
                data['classes'][cid] = {"name": f"Class {cid}", "subjects": {}}
            for sid, sname in common_subjects.items():
                if sid not in data['classes'][cid]['subjects']:
                    data['classes'][cid]['subjects'][sid] = sname

        for cid in ["11", "12"]:
            if cid not in data['classes']:
                data['classes'][cid] = {"name": f"Class {cid}", "subjects": {}}
            for sid, sname in hs_subjects.items():
                if sid not in data['classes'][cid]['subjects']:
                    data['classes'][cid]['subjects'][sid] = sname

        if 'exam_categories' not in data or not data['exam_categories']:
            data['exam_categories'] = [
                {"name": "Unit Tests", "types": ["Unit Test 1", "Unit Test 2", "Unit Test 3", "Unit Test 4", "Unit Test 5"]},
                {"name": "Midterm Tests", "types": ["Midterm Test 1", "Midterm Test 2"]},
                {"name": "Quarterly Exam", "types": ["Quarterly Exam"]},
                {"name": "Half Yearly Exam", "types": ["Half Yearly Exam"]},
                {"name": "Practical Exam", "types": ["Practical Exam"]},
                {"name": "Annual Exam", "types": ["Annual Exam", "Public Exam"]}
            ]
        
        if 'files' not in data:
            data['files'] = []
            
        return data
    except Exception as e:
        logging.error(f"Error loading data: {e}")
        return {"classes": {}, "files": [], "exam_categories": []}

def save_data(data):
    """Save data to JSON file"""
    try:
        with open(DATA_FILE, 'w') as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        logging.error(f"Error saving data: {e}")

# Admin access configuration
ADMIN_SECRET_PATH = os.environ.get("ADMIN_SECRET_PATH", "admin")

def is_admin():
    return session.get('is_admin', False)

@app.route(f'/{ADMIN_SECRET_PATH}', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password) and user.is_admin:
            session['is_admin'] = True
            session['username'] = username
            flash('Admin login successful!', 'success')
            return redirect(url_for('admin_dashboard'))
        flash('Invalid admin credentials', 'error')
    return render_template('admin/login.html')

@app.route(f'/{ADMIN_SECRET_PATH}/dashboard')
def admin_dashboard():
    if not is_admin():
        return redirect(url_for('index'))
    return render_template('admin/dashboard.html')

@app.route('/admin/logout')
def admin_logout():
    session.pop('is_admin', None)
    session.pop('username', None)
    flash('Logged out successfully', 'success')
    return redirect(url_for('index'))

@app.route('/')
def index():
    data = load_data()
    return render_template('index.html', classes=data['classes'])

@app.route('/class-<class_id>')
def view_class(class_id):
    data = load_data()
    if class_id not in data['classes']:
        flash('Class not found', 'error')
        return redirect(url_for('index'))
    return render_template('class_view.html', class_id=class_id, class_data=data['classes'][class_id])

@app.route('/class-<class_id>/<subject_id>')
def view_subject(class_id, subject_id):
    data = load_data()
    if class_id not in data['classes'] or subject_id not in data['classes'][class_id]['subjects']:
        flash('Subject not found', 'error')
        return redirect(url_for('view_class', class_id=class_id))
    
    subject_name = data['classes'][class_id]['subjects'][subject_id]
    exam_categories = data.get('exam_categories', [])
    return render_template('subject_view.html', 
                         class_id=class_id, 
                         subject_id=subject_id, 
                         subject_name=subject_name,
                         exam_categories=exam_categories)

@app.route('/class-<class_id>/<subject_id>/<exam_type_slug>')
def view_exam_type(class_id, subject_id, exam_type_slug):
    data = load_data()
    exam_display_name = exam_type_slug.replace('-', ' ').title()
    if class_id not in data['classes'] or subject_id not in data['classes'][class_id]['subjects']:
         return redirect(url_for('index'))
    subject_name = data['classes'][class_id]['subjects'].get(subject_id)
    relevant_files = [f for f in data['files'] if 
                     str(f.get('class_level')) == str(class_id) and 
                     (str(f.get('subject_id')) == str(subject_id) or f.get('subject_name') == subject_name) and
                     exam_type_slug in f.get('category', '').lower().replace(' ', '-')]
    
    return render_template('exam_type_view.html', 
                         class_id=class_id, 
                         subject_id=subject_id, 
                         subject_name=subject_name,
                         exam_display_name=exam_display_name,
                         files=relevant_files)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if not is_admin():
        flash('Access denied', 'error')
        return redirect(url_for('index'))
    if request.method == 'POST':
        # Implementation for file upload
        pass
    data = load_data()
    # Handle both old and new data structure for template compatibility
    exam_types = []
    if 'exam_categories' in data:
        for cat in data['exam_categories']:
            exam_types.extend(cat['types'])
    else:
        exam_types = data.get('exam_types', [])
    return render_template('upload.html', classes=data['classes'], exam_types=exam_types)

@app.route('/search')
def search():
    return render_template('search.html')

@app.route('/file/<int:file_id>')
def file_detail(file_id):
    data = load_data()
    file_found = next((f for f in data['files'] if f['id'] == file_id), None)
    if not file_found or (not file_found.get('is_published', True) and not is_admin()):
        flash('File not found', 'error')
        return redirect(url_for('index'))
    return render_template('file_detail.html', file=file_found)

@app.route('/download/<int:file_id>')
def download_file(file_id):
    data = load_data()
    file_found = next((f for f in data['files'] if f['id'] == file_id), None)
    if not file_found or (not file_found.get('is_published', True) and not is_admin()):
        flash('Access denied', 'error')
        return redirect(url_for('index'))
    return send_from_directory(app.config['UPLOAD_FOLDER'], file_found['filename'])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
