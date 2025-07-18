from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
import bcrypt
from datetime import datetime

db = SQLAlchemy()

class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='teacher')

    def __init__(self, username, email, password, role='teacher'):
        self.username = username
        self.email = email
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        self.role = role

# Table for classes
class Class(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    branch = db.Column(db.String(50), nullable=False)
    year = db.Column(db.String(10), nullable=False)

# Table for students
class Student(db.Model):
    rollno = db.Column(db.String(20), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    class_id = db.Column(db.Integer, db.ForeignKey('class.id'), nullable=False)

# Table for sessions
class ClassSession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    class_id = db.Column(db.Integer, db.ForeignKey('class.id'), nullable=False)
    subject = db.Column(db.String(100), nullable=False)
    time = db.Column(db.DateTime, default=datetime.utcnow)
    num_present = db.Column(db.Integer, nullable=False) 
class Record(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey('class_session.id'), nullable=False)
    student_rollno = db.Column(db.String(20), db.ForeignKey('student.rollno'), nullable=False)
    status = db.Column(db.String(10), nullable=False)  # 'Present' or 'Absent'

    session = db.relationship('ClassSession', backref='records')
    student = db.relationship('Student', backref='records')
