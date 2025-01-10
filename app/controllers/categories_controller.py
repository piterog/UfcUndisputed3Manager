from app.services.categories_service import get_ranking
from app.services.fighters_service import fighters_list_inactivity
from flask import jsonify

def ranking_by_category(category_id: int):
    list_category = get_ranking(category_id)
    inactivity_list = fighters_list_inactivity()

    for list in list_category:
        for fighters in list['fighters']:
            fighters['since_last_fight'] = inactivity_list[fighters['id']]

    return jsonify(list_category)