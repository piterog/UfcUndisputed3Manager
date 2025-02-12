from flask import render_template
from app.services.categories_service import get_ranking
from app.services.dashboards_service import get_last_n_fights, get_methods_statistics, get_pound_4_pound_ranking, \
    get_fighter_statistics

def index():
    last_fights = get_last_n_fights()
    fight_statistics = get_methods_statistics()
    pound_4_pound = get_pound_4_pound_ranking()
    fighter_statistics = get_fighter_statistics()

    return render_template('dashboard.html', last_n_fights=last_fights, fight_statistics=fight_statistics, pound_4_pound_ranking=pound_4_pound, fighter_statistics=fighter_statistics)

def ranking():
    list_category = get_ranking()

    return render_template('ranking.html', categories=list_category)
