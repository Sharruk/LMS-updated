#!/usr/bin/env python3
"""
Database initialization script for College Materials & PYQs Portal
Creates tables and seeds initial data
"""

import os
import sys
from datetime import datetime
from werkzeug.security import generate_password_hash

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app
from models import db, Subject, File, User

# Sample subject data
SUBJECT_DATA = {
    'UG': {
        'CSE': {
            '1': [
                {'code': 'CS1101', 'name': 'Programming in C', 'category': 'CAT'},
                {'code': 'MA1101', 'name': 'Engineering Mathematics I', 'category': 'ESE'},
                {'code': 'PH1101', 'name': 'Physics for Engineers', 'category': 'CAT'},
                {'code': 'CH1101', 'name': 'Engineering Chemistry', 'category': 'ESE'},
                {'code': 'EG1101', 'name': 'Engineering Graphics', 'category': 'Practical'},
            ],
            '2': [
                {'code': 'CS1201', 'name': 'Data Structures', 'category': 'CAT'},
                {'code': 'EC1202', 'name': 'Digital Logic Design', 'category': 'ESE'},
                {'code': 'MA1201', 'name': 'Engineering Mathematics II', 'category': 'CAT'},
                {'code': 'CS1202', 'name': 'Object Oriented Programming', 'category': 'ESE'},
                {'code': 'CS1203', 'name': 'Data Structures Lab', 'category': 'Practical'},
            ],
            '3': [
                {'code': 'CS2101', 'name': 'Computer Organization', 'category': 'CAT'},
                {'code': 'CS2102', 'name': 'Database Management Systems', 'category': 'ESE'},
                {'code': 'CS2103', 'name': 'Operating Systems', 'category': 'CAT'},
                {'code': 'MA2101', 'name': 'Discrete Mathematics', 'category': 'ESE'},
                {'code': 'CS2104', 'name': 'DBMS Lab', 'category': 'Practical'},
            ],
            '4': [
                {'code': 'CS2201', 'name': 'Algorithm Analysis', 'category': 'CAT'},
                {'code': 'CS2202', 'name': 'Computer Networks', 'category': 'ESE'},
                {'code': 'CS2203', 'name': 'Software Engineering', 'category': 'CAT'},
                {'code': 'CS2204', 'name': 'Theory of Computation', 'category': 'ESE'},
                {'code': 'CS2205', 'name': 'Networks Lab', 'category': 'Practical'},
            ],
            '5': [
                {'code': 'CS3101', 'name': 'Compiler Design', 'category': 'CAT'},
                {'code': 'CS3102', 'name': 'Machine Learning', 'category': 'ESE'},
                {'code': 'CS3103', 'name': 'Web Technologies', 'category': 'CAT'},
                {'code': 'CS3104', 'name': 'Computer Graphics', 'category': 'ESE'},
                {'code': 'CS3105', 'name': 'ML Lab', 'category': 'Practical'},
            ],
            '6': [
                {'code': 'CS3201', 'name': 'Artificial Intelligence', 'category': 'CAT'},
                {'code': 'CS3202', 'name': 'Distributed Systems', 'category': 'ESE'},
                {'code': 'CS3203', 'name': 'Information Security', 'category': 'CAT'},
                {'code': 'CS3204', 'name': 'Mobile Computing', 'category': 'ESE'},
                {'code': 'CS3205', 'name': 'Project Work I', 'category': 'Practical'},
            ],
            '7': [
                {'code': 'CS4101', 'name': 'Data Science', 'category': 'CAT'},
                {'code': 'CS4102', 'name': 'Cloud Computing', 'category': 'ESE'},
                {'code': 'CS4103', 'name': 'Blockchain Technology', 'category': 'CAT'},
                {'code': 'CS4104', 'name': 'IoT Systems', 'category': 'ESE'},
                {'code': 'CS4105', 'name': 'Internship', 'category': 'Practical'},
            ],
            '8': [
                {'code': 'CS4201', 'name': 'Deep Learning', 'category': 'CAT'},
                {'code': 'CS4202', 'name': 'Software Testing', 'category': 'ESE'},
                {'code': 'CS4203', 'name': 'DevOps', 'category': 'CAT'},
                {'code': 'CS4204', 'name': 'Project Work II', 'category': 'Practical'},
                {'code': 'CS4205', 'name': 'Seminar', 'category': 'SAT'},
            ],
        },
        'MECH': {
            '1': [
                {'code': 'ME1101', 'name': 'Engineering Graphics', 'category': 'CAT'},
                {'code': 'PH1102', 'name': 'Physics for Engineers', 'category': 'ESE'},
                {'code': 'MA1101', 'name': 'Engineering Mathematics I', 'category': 'CAT'},
                {'code': 'CH1101', 'name': 'Engineering Chemistry', 'category': 'ESE'},
                {'code': 'ME1102', 'name': 'Workshop Technology', 'category': 'Practical'},
            ],
            '2': [
                {'code': 'ME1201', 'name': 'Thermodynamics', 'category': 'CAT'},
                {'code': 'ME1202', 'name': 'Fluid Mechanics', 'category': 'ESE'},
                {'code': 'MA1201', 'name': 'Engineering Mathematics II', 'category': 'CAT'},
                {'code': 'ME1203', 'name': 'Materials Science', 'category': 'ESE'},
                {'code': 'ME1204', 'name': 'CAD Lab', 'category': 'Practical'},
            ],
            '3': [
                {'code': 'ME2101', 'name': 'Strength of Materials', 'category': 'CAT'},
                {'code': 'ME2102', 'name': 'Manufacturing Processes', 'category': 'ESE'},
                {'code': 'ME2103', 'name': 'Machine Design', 'category': 'CAT'},
                {'code': 'ME2104', 'name': 'Heat Transfer', 'category': 'ESE'},
                {'code': 'ME2105', 'name': 'Manufacturing Lab', 'category': 'Practical'},
            ],
            '4': [
                {'code': 'ME2201', 'name': 'Dynamics of Machinery', 'category': 'CAT'},
                {'code': 'ME2202', 'name': 'Fluid Machinery', 'category': 'ESE'},
                {'code': 'ME2203', 'name': 'Control Systems', 'category': 'CAT'},
                {'code': 'ME2204', 'name': 'Vibrations', 'category': 'ESE'},
                {'code': 'ME2205', 'name': 'Thermal Lab', 'category': 'Practical'},
            ],
        },
        'IT': {
            '1': [
                {'code': 'IT1101', 'name': 'Programming Fundamentals', 'category': 'CAT'},
                {'code': 'MA1101', 'name': 'Engineering Mathematics I', 'category': 'ESE'},
                {'code': 'PH1101', 'name': 'Physics for Engineers', 'category': 'CAT'},
                {'code': 'CH1101', 'name': 'Engineering Chemistry', 'category': 'ESE'},
                {'code': 'IT1102', 'name': 'Programming Lab', 'category': 'Practical'},
            ],
            '2': [
                {'code': 'IT1201', 'name': 'Data Structures and Algorithms', 'category': 'CAT'},
                {'code': 'IT1202', 'name': 'Digital Systems', 'category': 'ESE'},
                {'code': 'MA1201', 'name': 'Engineering Mathematics II', 'category': 'CAT'},
                {'code': 'IT1203', 'name': 'Computer Organization', 'category': 'ESE'},
                {'code': 'IT1204', 'name': 'DSA Lab', 'category': 'Practical'},
            ],
        },
    },
    'PG': {
        'mtech_cse': {
            '1': [
                {'code': 'MCS1101', 'name': 'Advanced Data Structures', 'category': 'CAT'},
                {'code': 'MCS1102', 'name': 'Advanced Algorithms', 'category': 'ESE'},
                {'code': 'MCS1103', 'name': 'Research Methodology', 'category': 'CAT'},
                {'code': 'MCS1104', 'name': 'Machine Learning', 'category': 'ESE'},
                {'code': 'MCS1105', 'name': 'ML Lab', 'category': 'Practical'},
            ],
            '2': [
                {'code': 'MCS1201', 'name': 'Deep Learning', 'category': 'CAT'},
                {'code': 'MCS1202', 'name': 'Computer Vision', 'category': 'ESE'},
                {'code': 'MCS1203', 'name': 'Natural Language Processing', 'category': 'CAT'},
                {'code': 'MCS1204', 'name': 'Big Data Analytics', 'category': 'ESE'},
                {'code': 'MCS1205', 'name': 'DL Lab', 'category': 'Practical'},
            ],
        },
    },
    'MBA': {
        'general_mba': {
            '1': [
                {'code': 'MBA1101', 'name': 'Principles of Management', 'category': 'CAT'},
                {'code': 'MBA1102', 'name': 'Financial Accounting', 'category': 'ESE'},
                {'code': 'MBA1103', 'name': 'Business Economics', 'category': 'CAT'},
                {'code': 'MBA1104', 'name': 'Organizational Behavior', 'category': 'ESE'},
                {'code': 'MBA1105', 'name': 'Case Study Analysis', 'category': 'Practical'},
            ],
            '2': [
                {'code': 'MBA1201', 'name': 'Marketing Management', 'category': 'CAT'},
                {'code': 'MBA1202', 'name': 'Financial Management', 'category': 'ESE'},
                {'code': 'MBA1203', 'name': 'Operations Management', 'category': 'CAT'},
                {'code': 'MBA1204', 'name': 'Human Resource Management', 'category': 'ESE'},
                {'code': 'MBA1205', 'name': 'Business Simulation', 'category': 'Practical'},
            ],
        },
    },
}

def create_tables():
    """Create all database tables"""
    print("Creating database tables...")
    with app.app_context():
        db.create_all()
        print("Tables created successfully!")

def seed_subjects():
    """Seed the database with sample subject data"""
    print("Seeding subject data...")
    with app.app_context():
        # Clear existing subjects
        Subject.query.delete()
        db.session.commit()
        
        subject_count = 0
        created_codes = set()
        
        for course_type, departments in SUBJECT_DATA.items():
            for dept_key, semesters in departments.items():
                for semester, subjects in semesters.items():
                    for subject_info in subjects:
                        # Make subject codes unique by adding department prefix if needed
                        base_code = subject_info['code']
                        unique_code = base_code
                        counter = 1
                        
                        while unique_code in created_codes:
                            if course_type == 'UG' and dept_key != 'CSE':
                                unique_code = f"{dept_key[:2]}{base_code[2:]}"
                            else:
                                unique_code = f"{base_code}_{counter}"
                                counter += 1
                        
                        created_codes.add(unique_code)
                        
                        subject = Subject(
                            code=unique_code,
                            name=subject_info['name'],
                            course_type=course_type,
                            department=dept_key,
                            semester=semester,
                            category=subject_info['category']
                        )
                        db.session.add(subject)
                        subject_count += 1
        
        db.session.commit()
        print(f"Seeded {subject_count} subjects successfully!")

def create_admin_user():
    """Create default admin user"""
    print("Creating admin user...")
    with app.app_context():
        # Check if admin user already exists
        admin = User.query.filter_by(username='admin').first()
        if admin:
            print("Admin user already exists!")
            return
        
        admin_user = User(
            username='admin',
            email='admin@college.edu',
            password_hash=generate_password_hash('admin123'),
            is_admin=True
        )
        
        db.session.add(admin_user)
        db.session.commit()
        print("Admin user created successfully!")
        print("Username: admin")
        print("Password: admin123")

def migrate_existing_files():
    """Migrate existing JSON file data to database"""
    print("Migrating existing file data...")
    
    from app import load_data
    
    with app.app_context():
        # Load existing JSON data
        try:
            data = load_data()
            existing_files = data.get('files', [])
            
            if not existing_files:
                print("No existing files to migrate!")
                return
            
            # Clear existing file records
            File.query.delete()
            
            migrated_count = 0
            for file_data in existing_files:
                # Try to find matching subject
                subject = None
                if file_data.get('subject'):
                    subject = Subject.query.filter_by(
                        name=file_data['subject']
                    ).first()
                
                # Create file record
                file_record = File(
                    filename=file_data.get('filename', ''),
                    original_filename=file_data.get('original_filename', ''),
                    custom_filename=file_data.get('custom_filename', ''),
                    course_type=file_data.get('course_type', 'UG'),
                    department=file_data.get('department', ''),
                    semester=str(file_data.get('semester', '1')),
                    category=file_data.get('category', 'CAT'),
                    subject_id=subject.id if subject else None,
                    subject_name=file_data.get('subject', ''),
                    file_type='QP',  # Default to Question Paper
                    size=file_data.get('size', ''),
                    file_path=file_data.get('file_path', ''),
                    upload_date=datetime.fromisoformat(file_data['upload_date']) if file_data.get('upload_date') else datetime.utcnow()
                )
                
                db.session.add(file_record)
                migrated_count += 1
            
            db.session.commit()
            print(f"Migrated {migrated_count} files successfully!")
            
        except Exception as e:
            print(f"Error migrating files: {str(e)}")

def main():
    """Main initialization function"""
    print("Initializing College Materials & PYQs Portal Database...")
    print("=" * 60)
    
    # Create tables
    create_tables()
    
    # Seed subjects
    seed_subjects()
    
    # Create admin user
    create_admin_user()
    
    # Migrate existing files
    migrate_existing_files()
    
    print("=" * 60)
    print("Database initialization completed successfully!")
    print("\nYou can now:")
    print("1. Log in as admin (username: admin, password: admin123)")
    print("2. Use the global search functionality")
    print("3. Upload files with subject associations")
    print("4. Manage subjects through the admin interface")

if __name__ == '__main__':
    main()