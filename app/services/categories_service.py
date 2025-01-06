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

def get_ranking(category_id: int = None) -> list:
    from app.services.category_fighters_service import get_fighter_ranking
    from app.services.fighters_service import get_by_category, format_record

    list_fighters = []
    list_category = []
    category_range = range(1, 8)

    if category_id:
        category_range = [category_id]

    for category_id in category_range:
        fighters = get_by_category(category_id, sort_by_ranking=True)
        category = get_category(category_id)
        for fighter in fighters:
            list_fighters.append({
                'id': fighter.id,
                'name': fighter.name,
                'record': format_record(fighter),
                'ranking': get_fighter_ranking(fighter.id, category_id)
            })

        list_category.append({
            'category': category.description,
            'fighters': list_fighters
        })

        list_fighters = []

    return list_category