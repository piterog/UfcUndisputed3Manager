from app.db_base import update_in_db
from app.models import Category

def get_category(category_id: int):
    return Category.query.get(category_id)

def get_all_categories():
    return Category.query.all()

def set_new_champion(category_id: int, fighter_id: int) -> None:
    update_in_db(Category, {'id': category_id}, {'champion_id': fighter_id})

def get_category_champion_id(category_id: int) -> int:
    return Category.query.get(category_id).champion_id

def format_short_category(category_description: str) -> str:
    if category_description == "Bantamweight":
        return "BW"
    elif category_description == "Featherweight":
        return "FW"
    elif category_description == "Lightweight":
        return "LW"
    elif category_description == "Welterweight":
        return "WW"
    elif category_description == "Middleweight":
        return "MW"
    elif category_description == "Light Heavyweight":
        return "LHW"
    elif category_description == "Heavyweight":
        return "HW"