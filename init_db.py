from app import create_app
from extensions import db
import os

def init_database():
    app = create_app()
    with app.app_context():
        # Verifica se as tabelas já existem
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        existing_tables = inspector.get_table_names()
        
        if not existing_tables:
            db.create_all()
            print("Database tables created successfully!")
        else:
            print("Tables already exist, preserving data")

if __name__ == "__main__":
    init_database()
