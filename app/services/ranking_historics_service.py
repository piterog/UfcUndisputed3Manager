from app.db_base import save_to_db
from app.models import RankingPointsHistoric


def add_historic(points: int, model_type: str, model_id: int, fighter_id: int, category_id: int) -> None:
    save_to_db(RankingPointsHistoric(points=points, model_type=model_type, model_id=model_id, fighter_id=fighter_id, category_id=category_id))