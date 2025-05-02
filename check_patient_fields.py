from __init__ import app, db
from sqlalchemy import inspect

def check_patient_fields():
    """Check the actual fields in the patient table"""
    with app.app_context():
        inspector = inspect(db.engine)
        
        print("Checking patient table structure...")
        if 'patient' in inspector.get_table_names():
            columns = inspector.get_columns('patient')
            print("Patient table columns:")
            for column in columns:
                print(f"- {column['name']}: {column['type']}")
        else:
            print("Patient table does not exist!")

if __name__ == "__main__":
    check_patient_fields()
