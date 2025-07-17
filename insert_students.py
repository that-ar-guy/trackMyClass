from models import db, Class, Student
from app import app

with app.app_context():
    classes = Class.query.all()

    for class_obj in classes:
        for i in range(1, 5):  # 4 students
            # Include class_id to ensure uniqueness
            rollno = f"{class_obj.branch[:3].upper()}{class_obj.year}{class_obj.id:02d}{i:02d}"
            name = f"Student{i}_{class_obj.branch}_{class_obj.year}"
            student = Student(rollno=rollno, name=name, class_id=class_obj.id)
            db.session.add(student)

    db.session.commit()
    print("✅ Unique students added for each class.")
