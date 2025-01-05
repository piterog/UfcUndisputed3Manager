from flask import render_template, request, redirect, url_for, flash, jsonify

from app.services.categories_service import get_category
from app.services.category_fighters_service import get_fighter_ranking
from app.services.fighters_service import get_by_category, format_record


def index():
    return "Home"

def ranking():
    list_fighters = []
    list_category = []

    for category_id in range(1, 7):
        fighters = get_by_category(category_id, sort_by_ranking=True)
        category = get_category(category_id)
        for fighter in fighters:
            list_fighters.append({
                'name': fighter.name,
                'record': format_record(fighter),
                'ranking': get_fighter_ranking(fighter.id, category_id)
            })

        list_category.append({
            'category': category.description,
            'fighters': list_fighters
        })

        list_fighters = []

    return render_template('ranking.html', categories=list_category)