from app import app, db
from sqlalchemy import text

with app.app_context():
    try:
        db.session.execute(text('ALTER TABLE class_session ADD COLUMN num_present INTEGER DEFAULT 0'))
        db.session.commit()
        print("✅ 'num_present' column added successfully.")
    except Exception as e:
        print("❌ Error adding column:", e)
