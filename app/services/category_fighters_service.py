from typing import Optional
from app.db_base import update_in_db
from app.models import CategoryFighter
from app.services.categories_service import get_category_champion_id

def get_fighter_ranking(fighter_id: int, category_id: int) -> Optional[int]:
    return CategoryFighter.query.filter_by(fighter_id=fighter_id,
                                           category_id=category_id).first().ranking

def update_ranking(fighter_id: int, category_id: int, ranking: int) -> None:
    if get_category_champion_id(category_id) == fighter_id:
        ranking = 1000
    elif ranking > 999:
        ranking = 999

    update_in_db(CategoryFighter, {'fighter_id': fighter_id, 'category_id': category_id}, {'ranking': ranking})