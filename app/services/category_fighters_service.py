from typing import Optional
from app.db_base import update_in_db
from app.models import CategoryFighter

def get_fighter_ranking(fighter_id: int, category_id: int) -> Optional[int]:
    return CategoryFighter.query.filter_by(fighter_id=fighter_id,
                                           category_id=category_id).first().ranking

def update_ranking(fighter_id: int, category_id: int, ranking: int) -> None:
    update_in_db(CategoryFighter, {'fighter_id': fighter_id, 'category_id': category_id}, {'ranking': ranking})