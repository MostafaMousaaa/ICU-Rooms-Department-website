from __init__ import app, db
from sqlalchemy import inspect
import pprint

def check_table_columns():
    """Check the actual columns in the database tables"""
    with app.app_context():
        inspector = inspect(db.engine)
        
        print("Available tables:")
        tables = inspector.get_table_names()
        print(tables)
        
        for table in tables:
            print(f"\n=== Table: {table} ===")
            columns = inspector.get_columns(table)
            for column in columns:
                print(f"- {column['name']}: {column['type']}")

if __name__ == "__main__":
    check_table_columns()
