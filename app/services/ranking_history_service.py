from app.db_base import save_to_db
from app.models import RankingHistory
from app.services.categories_service import get_ranking
from app.services.events_service import get_last_event_id

def snapshot_fighters() -> None:
    category_range = range(1, 8)
    last_event_id = get_last_event_id()

    for category_range in category_range:
        for ranking in get_ranking(category_range):
            for index, fighter in enumerate(ranking['fighters']):
                history = RankingHistory(event_id=last_event_id, fighter_id=fighter['id'], category_id=category_range, order=index+1)
                save_to_db(history)


def get_position_change(fighter_id:int, category_id: int):
    last_event_id = get_last_event_id()
    penultimate_event_id = get_last_event_id(1)

    last_ranking_position = RankingHistory.query.filter_by(event_id=last_event_id, fighter_id=fighter_id, category_id=category_id).order_by(RankingHistory.id.desc()).first()
    penultimate_ranking_position = RankingHistory.query.filter_by(event_id=penultimate_event_id, fighter_id=fighter_id, category_id=category_id).order_by(RankingHistory.id.desc()).first()

    if last_ranking_position is None or penultimate_ranking_position is None:
        return 0

    return penultimate_ranking_position.order - last_ranking_position.order