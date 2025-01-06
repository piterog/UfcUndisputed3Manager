from app.services.categories_service import get_ranking
from flask import jsonify

def ranking_by_category(category_id: int):
    list_category = get_ranking(category_id)

    return jsonify(list_category)