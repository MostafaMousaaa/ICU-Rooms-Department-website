from __init__ import app, db
from sqlalchemy import inspect

def check_doctor_fields():
    """Check the actual fields in the doctor table"""
    with app.app_context():
        inspector = inspect(db.engine)
        
        print("Checking doctor table structure...")
        if 'doctor' in inspector.get_table_names():
            columns = inspector.get_columns('doctor')
            print("Doctor table columns:")
            for column in columns:
                print(f"- {column['name']}: {column['type']}")
        else:
            print("Doctor table does not exist!")

if __name__ == "__main__":
    check_doctor_fields()
