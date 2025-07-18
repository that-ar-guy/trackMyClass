from flask import Flask
from models import db, Class

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///attendance.db'
app.config['SECRET_KEY'] = "THIS IS A SECRET KEY"
db.init_app(app)

classes = [
    "CSE-A", "CSE-B", "AIML", "IoT", "DS", "IT", "MEC", "CIV", "ECE","IOT"
]

years = ["1st", "2nd", "3rd", "4th"]

with app.app_context():
    for branch in classes:
        for year in years:
            new_class = Class(branch=branch, year=year)
            db.session.add(new_class)

    db.session.commit()
    print("All classes inserted successfully!")
