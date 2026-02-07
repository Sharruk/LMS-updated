import os
from app import app, db
from models import User
from werkzeug.security import generate_password_hash
import sys

def change_admin(new_username, new_password):
    with app.app_context():
        user = User.query.filter_by(is_admin=True).first()
        if not user:
            user = User(username=new_username, email="admin@example.com", is_admin=True)
            db.session.add(user)
        
        user.username = new_username
        user.password_hash = generate_password_hash(new_password)
        db.session.commit()
        print(f"Admin credentials updated: Username: {new_username}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python update_admin.py <new_username> <new_password>")
    else:
        change_admin(sys.argv[1], sys.argv[2])
