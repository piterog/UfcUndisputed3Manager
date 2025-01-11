from flask import render_template
from app.services.categories_service import get_ranking


def index():
    return "Home"

def ranking():
    list_category = get_ranking()

    return render_template('ranking.html', categories=list_category)