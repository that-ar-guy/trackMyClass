# app.py
from flask import Flask, render_template, url_for, request, redirect, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
import bcrypt
from models import Users, Student, Class,Record,ClassSession

from models import db, Users  # ✅ Import from models.py

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///attendance.db'
app.config['SECRET_KEY'] = "THIS IS A SECRET KEY"

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

with app.app_context():
    db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(Users, int(user_id))

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        role = request.form.get('role', 'teacher')

        if Users.query.filter_by(email=email).first():
            flash('Email already registered.', 'warning')
            return redirect(url_for('register'))

        new_user = Users(username=username, email=email, password=password, role=role)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful. Please login.', 'success')
        return redirect(url_for('login'))

    return render_template("register.html")

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = Users.query.filter_by(email=email).first()

        if user and bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials', 'danger')
            return redirect(url_for('login'))

    return render_template("login.html")

@app.route("/dashboard", methods=['GET', 'POST'])
@login_required
def dashboard():
    if current_user.role == 'teacher':
        branches = db.session.query(Class.branch).distinct().all()
        years = db.session.query(Class.year).distinct().all()
        print(branches)
        selected_branch = request.form.get('branch')
        selected_year = request.form.get('year')
        students = []

        if request.method == 'POST' and selected_branch and selected_year:
            matched_classes = Class.query.filter_by(branch=selected_branch, year=selected_year).all()
            class_ids = [cls.id for cls in matched_classes]
            students = Student.query.filter(Student.class_id.in_(class_ids)).all()

        return render_template("teacher_dashboard.html", 
                               branches=[b[0] for b in branches], 
                               years=[y[0] for y in years], 
                               students=students)

    return f"Welcome {current_user.username}"

from datetime import datetime

@app.route("/mark_attendance", methods=['POST'])
@login_required
def mark_attendance():
    class_id = int(request.form.get("class_id"))
    subject = request.form.get("subject")
    present_students = request.form.getlist("present_students")  # Checked roll numbers

    # Fetch all students of the class
    all_students = Student.query.filter_by(class_id=class_id).all()

    # Count the number of students marked present
    num_present = len(present_students)

    # Create a session
    new_session = ClassSession(
        teacher_id=current_user.id,
        class_id=class_id,
        subject=subject,
        time=datetime.now(),
        num_present=num_present
    )
    db.session.add(new_session)
    db.session.commit()

    # Create record for each student — present or absent
    for student in all_students:
        status = 'present' if student.rollno in present_students else 'absent'
        new_record = Record(
            session_id=new_session.id,
            student_rollno=student.rollno,
            status=status
        )
        db.session.add(new_record)

    db.session.commit()
    flash(f"Attendance marked successfully: {num_present} present, {len(all_students) - num_present} absent.", "success")
    return redirect(url_for("dashboard"))

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash('Logged out successfully.', 'info')
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)
