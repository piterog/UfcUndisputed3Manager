from extensions import db
from sqlalchemy.exc import SQLAlchemyError

def save_to_db(instance):
    try:
        db.session.add(instance)
        db.session.commit()
        return instance
    except SQLAlchemyError as e:
        db.session.rollback()
        print(f"Error on save: {e}")
        raise

def update_in_db(model, filters: dict, updates: dict):
    try:
        instance = model.query.filter_by(**filters).first()
        if not instance:
            print("Register not found!")
            return None
        for key, value in updates.items():
            setattr(instance, key, value)
        db.session.commit()
        return instance
    except SQLAlchemyError as e:
        db.session.rollback()
        print(f"Error on update: {e}")
        raise
