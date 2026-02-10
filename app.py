import os
import json
import logging
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, send_file, send_from_directory, jsonify, session
from werkzeug.utils import secure_filename
from werkzeug.middleware.proxy_fix import ProxyFix
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, Subject, File, User, Comment

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
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'doc', 'xls', 'xlsx', 'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def load_data():
    """Load config data like exam types from JSON file"""
    try:
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r') as f:
                return json.load(f)
        else:
            data = {
                "exam_types": [
                    "Unit Test 1", "Unit Test 2", "Unit Test 3",
                    "Quarterly Exam", "Half Yearly Exam",
                    "Revision Test", "Model Practical",
                    "Practical Exam", "Annual Exam"
                ]
            }
            with open(DATA_FILE, 'w') as f:
                json.dump(data, f, indent=2)
            return data
    except Exception as e:
        app.logger.error(f"Error loading data: {e}")
        return {"exam_types": []}

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
    classes = {"9": "Class 9", "10": "Class 10", "11": "Class 11", "12": "Class 12"}
    return render_template('index.html', classes=classes)

@app.route('/class/<class_id>')
def view_class(class_id):
    files = File.query.filter_by(class_level=class_id, visible=True).all()
    subjects = sorted(list(set([f.subject_name for f in files])))
    class_name = f"Class {class_id}"
    return render_template('class_view.html', class_id=class_id, class_name=class_name, subjects=subjects)

@app.route('/subject/<class_id>/<subject_name>')
def view_subject(class_id, subject_name):
    data = load_data()
    exam_types = data.get('exam_types', [])
    return render_template('subject_view.html', class_id=class_id, subject_name=subject_name, exam_types=exam_types)

@app.route('/exams/<class_id>/<subject_name>/<exam_type>')
def view_exams(class_id, subject_name, exam_type):
    try:
        files = File.query.filter_by(class_level=class_id, subject_name=subject_name, exam_type=exam_type, visible=True).all()
        return render_template('files_list.html', class_id=class_id, subject_name=subject_name, exam_type=exam_type, files=files)
    except Exception as e:
        app.logger.error(f"Error in view_exams: {e}")
        return render_template('files_list.html', class_id=class_id, subject_name=subject_name, exam_type=exam_type, files=[])

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if not is_admin():
        flash('Access denied', 'error')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        class_level = request.form.get('class_level')
        subject_name = request.form.get('subject_name')
        exam_type = request.form.get('exam_type')
        year = request.form.get('year')
        custom_name = request.form.get('custom_filename')
        description = request.form.get('description')
        file = request.files.get('file')

        if file and allowed_file(file.filename):
            filename = secure_filename(f"{class_level}_{subject_name}_{exam_type}_{year}_{file.filename}")
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            display_name = custom_name if custom_name else f"{subject_name} - {exam_type} ({year})"

            new_file = File(
                filename=filename,
                original_filename=file.filename,
                custom_filename=display_name,
                class_level=class_level,
                subject_name=subject_name,
                exam_type=exam_type,
                year=year,
                description=description,
                file_path=file_path,
                size=f"{os.path.getsize(file_path) / 1024:.1f} KB",
                visible=True
            )
            db.session.add(new_file)
            db.session.commit()
            flash('File uploaded successfully!', 'success')
            return redirect(url_for('admin_dashboard'))
        flash('Invalid file. Allowed formats: PDF, DOCX, Images, XLS.', 'error')

    data = load_data()
    return render_template('upload.html', exam_types=data['exam_types'])

@app.route('/search')
def search():
    query = request.args.get('q', '')
    if query:
        files = File.query.filter(File.custom_filename.ilike(f'%{query}%'), File.visible==True).all()
    else:
        files = []
    return render_template('search.html', files=files, query=query)

@app.route('/file/<int:file_id>')
def file_detail(file_id):
    file_item = File.query.get_or_404(file_id)
    if not file_item.visible and not is_admin():
        flash('File not found', 'error')
        return redirect(url_for('index'))
    return render_template('file_detail.html', file=file_item)

@app.route('/download/<int:file_id>')
def download(file_id):
    file_item = File.query.get_or_404(file_id)
    return send_from_directory(app.config['UPLOAD_FOLDER'], file_item.filename)

@app.route('/api/vote/<int:file_id>', methods=['POST'])
def vote(file_id):
    file_item = File.query.get_or_404(file_id)
    vote_type = request.json.get('vote_type')
    if vote_type == 'like':
        file_item.likes += 1
    elif vote_type == 'dislike':
        file_item.dislikes += 1
    db.session.commit()
    return jsonify({'success': True, 'likes': file_item.likes, 'dislikes': file_item.dislikes})

@app.route('/api/comment/<int:file_id>', methods=['POST'])
def add_comment(file_id):
    author = request.json.get('name')
    content = request.json.get('comment')
    if author and content:
        new_comment = Comment(file_id=file_id, author_name=author, content=content)
        db.session.add(new_comment)
        db.session.commit()
        return jsonify({'success': True})
    return jsonify({'success': False}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
