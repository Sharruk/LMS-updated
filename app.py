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
# How to set SECRET_KEY in Replit Secrets:
# Left side -> Click 🔒 Secrets -> Add Name: SECRET_KEY, Value: your-random-secret
app.secret_key = os.environ.get("SESSION_SECRET")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Database configuration for Render/Replit
DATABASE_URL = os.environ.get('DATABASE_URL')
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL or 'sqlite:///tn_board_portal.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}

# Initialize database
db.init_app(app)

with app.app_context():
    db.create_all()

# Configuration
UPLOAD_FOLDER = 'uploads'
DATA_FILE = 'data.json'
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'ppt', 'pptx', 'xls', 'xlsx', 'csv', 'txt', 'jpg', 'png', 'jpeg', 'mp4'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def load_data():
    """Load data from JSON file"""
    try:
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r') as f:
                data = json.load(f)
        else:
            data = {"classes": {}, "files": [], "exam_categories": []}
        
        # Standard subjects for Class 9 & 10
        common_subjects = {
            "tamil": "Tamil", "english": "English", "maths": "Mathematics",
            "science": "Science", "social": "Social Science"
        }
        # Higher secondary subjects for Class 11 & 12
        hs_subjects = {
            "tamil": "Tamil", "english": "English", "maths": "Mathematics",
            "physics": "Physics", "chemistry": "Chemistry", "biology": "Biology",
            "csc": "Computer Science", "capp": "Computer Applications",
            "acc": "Accountancy", "comm": "Commerce", "eco": "Economics"
        }
        theory_only = ["tamil", "english", "maths", "social"]

        for cid in ["9", "10"]:
            if cid not in data['classes']:
                data['classes'][cid] = {"name": f"Class {cid}", "subjects": {}}
            for sid, sname in common_subjects.items():
                if sid not in data['classes'][cid]['subjects']:
                    data['classes'][cid]['subjects'][sid] = {"name": sname, "is_theory_only": sid in theory_only}

        for cid in ["11", "12"]:
            if cid not in data['classes']:
                data['classes'][cid] = {"name": f"Class {cid}", "subjects": {}}
            for sid, sname in hs_subjects.items():
                if sid not in data['classes'][cid]['subjects']:
                    data['classes'][cid]['subjects'][sid] = {"name": sname, "is_theory_only": sid in theory_only}

        if 'exam_categories' not in data or not data['exam_categories']:
            data['exam_categories'] = [
                {"name": "Unit Tests", "types": ["Unit Test 1", "Unit Test 2", "Unit Test 3", "Unit Test 4", "Unit Test 5"]},
                {"name": "Midterm Tests", "types": ["Midterm Test 1", "Midterm Test 2"]},
                {"name": "Quarterly Exam", "types": ["Quarterly Exam"]},
                {"name": "Half Yearly Exam", "types": ["Half Yearly Exam"]},
                {"name": "Practical Exam", "types": ["Practical Exam"]},
                {"name": "Annual Exam", "types": ["Annual Exam", "Public Exam"]}
            ]
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

# How to set ADMIN_USERNAME and ADMIN_PASSWORD in Replit Secrets:
# Left side -> Click 🔒 Secrets -> Add Name: ADMIN_USERNAME, Value: your-username
# Left side -> Click 🔒 Secrets -> Add Name: ADMIN_PASSWORD, Value: your-password
ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "admin123")
ADMIN_SECRET_PATH = os.environ.get("ADMIN_SECRET_PATH", "admin")

def is_admin():
    return session.get('is_admin', False)

@app.route(f'/{ADMIN_SECRET_PATH}', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Admin check using environment variables
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['is_admin'] = True
            session['username'] = username
            flash('Admin login successful!', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid admin credentials', 'error')
    return render_template('admin/login.html')

@app.route(f'/{ADMIN_SECRET_PATH}/dashboard')
def admin_dashboard():
    if not is_admin():
        return redirect(url_for('index'))
    return render_template('admin/dashboard.html')

@app.route('/admin/comments')
def admin_comments():
    if not is_admin():
        return redirect(url_for('index'))
    comments = Comment.query.order_by(Comment.created_at.desc()).all()
    return render_template('admin/comments.html', comments=comments)

@app.route('/admin/delete-comment/<int:comment_id>', methods=['POST'])
def delete_comment(comment_id):
    if not is_admin():
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403
    comment = Comment.query.get_or_404(comment_id)
    try:
        db.session.delete(comment)
        db.session.commit()
        flash('Comment deleted successfully', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting comment: {str(e)}', 'error')
    return redirect(url_for('admin_comments'))

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
    
    subject_info = data['classes'][class_id]['subjects'][subject_id]
    subject_name = subject_info.get('name') if isinstance(subject_info, dict) else subject_info

    exam_categories = [
        {"name": "Unit Tests", "types": ["Unit Test 1", "Unit Test 2", "Unit Test 3", "Unit Test 4", "Unit Test 5"]},
        {"name": "Midterm Tests", "types": ["Midterm Test 1", "Midterm Test 2"]},
        {"name": "Quarterly Exam", "types": ["Quarterly Exam"]},
        {"name": "Half Yearly Exam", "types": ["Half Yearly Exam"]},
        {"name": "Practical Exam", "types": ["Practical Exam"]},
        {"name": "Annual Exam", "types": ["Annual Exam", "Public Exam"]}
    ]
    priority = ["Unit Tests", "Midterm Tests", "Quarterly Exam", "Half Yearly Exam", "Annual Exam", "Practical Exam"]
    exam_categories.sort(key=lambda x: priority.index(x['name']) if x['name'] in priority else 99)

    practical_subjects = ["Science", "Physics", "Chemistry", "Biology", "Computer Science", "Computer Applications"]
    if subject_name not in practical_subjects:
        exam_categories = [c for c in exam_categories if c['name'] != "Practical Exam"]

    files = data.get('files', [])
    for cat in exam_categories:
        cat['counts'] = {}
        cat['total_count'] = 0
        for etype in cat.get('types', []):
            etype_slug = etype.lower().replace(' ', '-')
            count = len([f for f in files if 
                         str(f.get('class_level')) == str(class_id) and 
                         (str(f.get('subject_id')) == str(subject_id) or f.get('subject_name') == subject_name) and
                         etype_slug in f.get('exam_type', '').lower().replace(' ', '-') and
                         (f.get('visible', True) or is_admin())])
            cat['counts'][etype] = count
            cat['total_count'] += count

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
    
    subject_info = data['classes'][class_id]['subjects'].get(subject_id)
    subject_name = subject_info.get('name') if isinstance(subject_info, dict) else subject_info

    relevant_files = [f for f in data.get('files', []) if 
                     str(f.get('class_level')) == str(class_id) and 
                     (str(f.get('subject_id')) == str(subject_id) or f.get('subject_name') == subject_name) and
                     exam_type_slug in f.get('exam_type', '').lower().replace(' ', '-') and
                     (f.get('visible', True) or is_admin())]
    
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
        file = request.files.get('file')
        if not file or file.filename == '':
            flash('No file selected', 'error')
            return redirect(request.url)
        
        class_level = request.form.get('class')
        subject_id = request.form.get('subject')
        exam_type = request.form.get('exam_type')
        year = request.form.get('year')
        description = request.form.get('description', '')
        custom_filename = request.form.get('custom_filename', '').strip()
        
        subject = Subject.query.get(subject_id)
        if not subject:
            flash('Invalid subject', 'error')
            return redirect(request.url)

        original_filename = secure_filename(file.filename)
        extension = os.path.splitext(original_filename)[1]
        timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
        stored_filename = f"{timestamp}_{original_filename}"
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], stored_filename)
        file.save(file_path)
        
        final_custom_name = custom_filename if custom_filename else os.path.splitext(file.filename)[0]
        if not final_custom_name.lower().endswith(extension.lower()):
            final_custom_name += extension
            
        file_size = os.path.getsize(file_path)
        size_str = f"{file_size / 1024:.1f} KB" if file_size < 1024 * 1024 else f"{file_size / (1024*1024):.1f} MB"
        
        new_file = File(
            filename=stored_filename,
            original_filename=file.filename,
            custom_filename=final_custom_name,
            class_level=class_level,
            subject_id=subject.id,
            subject_name=subject.name,
            exam_type=exam_type,
            year=year,
            description=description,
            file_path=file_path,
            size=size_str
        )
        db.session.add(new_file)
        db.session.commit()
        
        data = load_data()
        data['files'].append(new_file.to_dict())
        save_data(data)
        
        flash('File uploaded successfully!', 'success')
        return redirect(url_for('admin_dashboard'))

    subjects = Subject.query.all()
    exam_types = ["Unit Test 1", "Unit Test 2", "Unit Test 3", "Quarterly Exam", "Half Yearly Exam", "Revision Test", "Model Practical", "Practical Exam", "Annual Exam"]
    return render_template('upload.html', subjects=subjects, exam_types=exam_types)

@app.route('/admin/manage-files')
def manage_files():
    if not is_admin():
        return redirect(url_for('index'))
    files = File.query.all()
    return render_template('admin/manage_files.html', files=files)

@app.route('/admin/delete-file/<int:file_id>', methods=['POST'])
def delete_file(file_id):
    if not is_admin():
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403
    file_to_delete = File.query.get_or_404(file_id)
    try:
        if os.path.exists(file_to_delete.file_path):
            os.remove(file_to_delete.file_path)
        db.session.delete(file_to_delete)
        db.session.commit()
        data = load_data()
        data['files'] = [f for f in data['files'] if f['id'] != file_id]
        save_data(data)
        flash('File deleted successfully', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting file: {str(e)}', 'error')
    return redirect(url_for('manage_files'))

@app.route('/admin/toggle-visibility/<int:file_id>', methods=['POST'])
def toggle_visibility(file_id):
    if not is_admin():
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403
    file_item = File.query.get_or_404(file_id)
    file_item.visible = not file_item.visible
    db.session.commit()
    data = load_data()
    for f in data['files']:
        if f['id'] == file_id:
            f['visible'] = file_item.visible
            break
    save_data(data)
    return redirect(url_for('manage_files'))

@app.route('/api/comment/<int:file_id>', methods=['POST'])
def add_comment(file_id):
    data = request.json
    author = data.get('author')
    content = data.get('content')
    if not author or not content:
        return jsonify({'success': False, 'message': 'Missing fields'}), 400
    comment = Comment(file_id=file_id, author_name=author, content=content)
    db.session.add(comment)
    db.session.commit()
    return jsonify({'success': True, 'comment': comment.to_dict()})

@app.route('/api/vote/<int:file_id>', methods=['POST'])
def vote(file_id):
    data = request.json
    vote_type = data.get('type')
    file_item = File.query.get_or_404(file_id)
    if vote_type == 'like':
        file_item.likes += 1
    elif vote_type == 'dislike':
        file_item.dislikes += 1
    db.session.commit()
    return jsonify({'success': True, 'likes': file_item.likes, 'dislikes': file_item.dislikes})

@app.route("/search")
def search():
    query = request.args.get("q", "").strip().lower()
    data = load_data()
    all_files = data.get('files', [])
    
    if not query:
        return render_template('search.html', all_files=all_files, query="")

    filtered_files = []
    for f in all_files:
        # Search by: Subject name, Class, Year, File title
        subject_name = str(f.get('subject_name', '')).lower()
        class_level = f"class {f.get('class_level', '')}".lower()
        year = str(f.get('year', '')).lower()
        title = str(f.get('custom_filename', '')).lower()
        
        if (query in subject_name or 
            query in class_level or 
            query in year or 
            query in title):
            filtered_files.append(f)
            
    return render_template('search.html', all_files=filtered_files, query=query)

@app.route('/file/<int:file_id>')
def file_detail(file_id):
    data = load_data()
    file_found = next((f for f in data['files'] if f['id'] == file_id), None)
    if not file_found or (not file_found.get('visible', True) and not is_admin()):
        flash('File not found', 'error')
        return redirect(url_for('index'))
    return render_template('file_detail.html', file=file_found)

@app.route('/download/<int:file_id>')
def download_file(file_id):
    data = load_data()
    file_found = next((f for f in data['files'] if f['id'] == file_id), None)
    if not file_found or (not file_found.get('visible', True) and not is_admin()):
        flash('Access denied', 'error')
        return redirect(url_for('index'))
    return send_from_directory(app.config['UPLOAD_FOLDER'], file_found['filename'])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
