#!/usr/bin/env python3
"""
Database initialization script for TN State Board Portal
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

# Sample school subject data
SUBJECT_DATA = {
    '9': [
        {'code': 'TAM09', 'name': 'Tamil', 'category': 'Theory'},
        {'code': 'ENG09', 'name': 'English', 'category': 'Theory'},
        {'code': 'MAT09', 'name': 'Mathematics', 'category': 'Theory'},
        {'code': 'SCI09', 'name': 'Science', 'category': 'Theory'},
        {'code': 'SOC09', 'name': 'Social Science', 'category': 'Theory'},
    ],
    '10': [
        {'code': 'TAM10', 'name': 'Tamil', 'category': 'Theory'},
        {'code': 'ENG10', 'name': 'English', 'category': 'Theory'},
        {'code': 'MAT10', 'name': 'Mathematics', 'category': 'Theory'},
        {'code': 'SCI10', 'name': 'Science', 'category': 'Theory'},
        {'code': 'SOC10', 'name': 'Social Science', 'category': 'Theory'},
    ],
    '11': [
        {'code': 'TAM11', 'name': 'Tamil', 'category': 'Theory'},
        {'code': 'ENG11', 'name': 'English', 'category': 'Theory'},
        {'code': 'MAT11', 'name': 'Mathematics', 'category': 'Theory'},
        {'code': 'PHY11', 'name': 'Physics', 'category': 'Theory'},
        {'code': 'CHE11', 'name': 'Chemistry', 'category': 'Theory'},
        {'code': 'BIO11', 'name': 'Biology', 'category': 'Theory'},
        {'code': 'CSC11', 'name': 'Computer Science', 'category': 'Theory'},
    ],
    '12': [
        {'code': 'TAM12', 'name': 'Tamil', 'category': 'Theory'},
        {'code': 'ENG12', 'name': 'English', 'category': 'Theory'},
        {'code': 'MAT12', 'name': 'Mathematics', 'category': 'Theory'},
        {'code': 'PHY12', 'name': 'Physics', 'category': 'Theory'},
        {'code': 'CHE12', 'name': 'Chemistry', 'category': 'Theory'},
        {'code': 'BIO12', 'name': 'Biology', 'category': 'Theory'},
        {'code': 'CSC12', 'name': 'Computer Science', 'category': 'Theory'},
    ],
}

def create_tables():
    """Create all database tables"""
    print("Creating database tables...")
    with app.app_context():
        db.drop_all()
        db.create_all()
        print("Tables created successfully!")

def seed_subjects():
    """Seed the database with sample subject data"""
    print("Seeding subject data...")
    with app.app_context():
        subject_count = 0
        for class_level, subjects in SUBJECT_DATA.items():
            for subj_info in subjects:
                subject = Subject(
                    code=subj_info['code'],
                    name=subj_info['name'],
                    class_level=class_level,
                    category=subj_info['category']
                )
                db.session.add(subject)
                subject_count += 1
        db.session.commit()
        print(f"Seeded {subject_count} subjects successfully!")

def create_admin_user():
    """Create default admin user"""
    print("Creating admin user...")
    with app.app_context():
        admin_user = User(
            username='admin',
            email='admin@tnboard.edu',
            password_hash=generate_password_hash('admin123'),
            is_admin=True
        )
        db.session.add(admin_user)
        db.session.commit()
        print("Admin user created successfully!")

def main():
    """Main initialization function"""
    print("Initializing TN State Board Portal Database...")
    print("=" * 60)
    create_tables()
    seed_subjects()
    create_admin_user()
    print("=" * 60)
    print("Database initialization completed successfully!")

if __name__ == '__main__':
    main()
