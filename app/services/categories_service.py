from app.db_base import update_in_db
from app.models import Category

def get_all_categories():
    return Category.query.all()

def set_new_champion(category_id: int, fighter_id: int) -> None:
    update_in_db(Category, {'category_id': category_id}, {'champion_id': fighter_id})