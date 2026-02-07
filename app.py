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
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///tn_board_portal.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db.init_app(app)

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
            if 'classes' not in data and 'course_types' in data:
                data['classes'] = data['course_types']
            if 'exam_types' not in data:
                data['exam_types'] = [
                    "CAT", "ESE", "SAT", "Practical"
                ]
            return data
        else:
            data = {
                "course_types": {},
                "classes": {},
                "exam_types": [
                    "CAT", "ESE", "SAT", "Practical"
                ],
                "files": []
            }
            save_data(data)
            return data
    except Exception as e:
        app.logger.error(f"Error loading data: {e}")
        return {"classes": {}, "files": [], "exam_types": []}

def save_data(data):
    """Save data to JSON file"""
    try:
        with open(DATA_FILE, 'w') as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        app.logger.error(f"Error saving data: {e}")

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

@app.route('/class/<class_id>')
def view_class(class_id):
    data = load_data()
    if class_id not in data['classes']:
        flash('Class not found', 'error')
        return redirect(url_for('index'))
    return render_template('class_view.html', class_id=class_id, class_data=data['classes'][class_id])

@app.route('/subject/<class_id>/<subject_id>')
def view_subject(class_id, subject_id):
    data = load_data()
    exam_types = data.get('exam_types', [])
    return render_template('subject_view.html', class_id=class_id, subject_id=subject_id, exam_types=exam_types)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if not is_admin():
        flash('Access denied', 'error')
        return redirect(url_for('index'))
    if request.method == 'POST':
        # Implementation for file upload
        pass
    data = load_data()
    return render_template('upload.html', classes=data['classes'], exam_types=data['exam_types'])

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
