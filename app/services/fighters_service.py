from typing import Optional, Dict
from app.models import Fighter, CategoryFighter
from app.db_base import update_in_db
from app.services.categories_service import set_new_champion
from app.services.category_fighters_service import get_fighter_ranking, update_ranking
from app.services.fights_service import get_fight, is_match_drawn, calculate_ranking_points, get_fight_historic, \
    get_lost_or_won_fights_grouped_by_method
from app.services.ranking_historics_service import add_historic


def get_all_fighters():
    return Fighter.query.all()

def get_fighter(fighter_id) -> Optional[Fighter]:
    return Fighter.query.filter_by(id=fighter_id).first()

def get_by_category(category_id: int, sort_by_ranking: bool = False) -> Optional[Fighter]:
    fighters = Fighter.query.join(CategoryFighter, Fighter.id == CategoryFighter.fighter_id).filter(
        CategoryFighter.category_id == category_id)

    if sort_by_ranking:
        fighters = fighters.order_by(CategoryFighter.ranking.desc())

    return fighters.all()

def add_victory(fighter: Fighter) -> None:
    update_in_db(Fighter, {'id': fighter.id}, {'victories': fighter.victories + 1})

def add_defeat(fighter: Fighter) -> None:
    update_in_db(Fighter, {'id': fighter.id}, {'defeats': fighter.defeats + 1})

def add_draw(fighter_red: Fighter, fighter_blue: Fighter) -> None:
    update_in_db(Fighter, {'id': fighter_red.id}, {'draws': fighter_red.draws + 1})
    update_in_db(Fighter, {'id': fighter_blue.id}, {'draws': fighter_blue.draws + 1})

def update_winner_ranking(fighter: Fighter, category_id: int, is_belt_dispute: bool, ranking_points: int) -> None:
    actual_ranking = get_fighter_ranking(fighter.id, category_id)

    points = ranking_points
    points += actual_ranking

    if is_belt_dispute:
        set_new_champion(category_id, fighter.id)

    update_ranking(fighter.id, category_id, points)

def update_loser_ranking(fighter: Fighter, category_id: int, ranking_points: int) -> None:
    actual_ranking = get_fighter_ranking(fighter.id, category_id)

    ranking_points += actual_ranking

    update_ranking(fighter.id, category_id, ranking_points)

def update_fighters_data(fight_id: int) -> None:
    fight = get_fight(fight_id)
    red_fighter = fight.red_corner
    blue_fighter = fight.blue_corner

    if is_match_drawn(fight):
        add_draw(red_fighter, blue_fighter)
    else:
        winner = fight.winner
        loser = fight.loser

        add_victory(winner)
        add_defeat(loser)

        fight_points = calculate_ranking_points(fight)

        add_historic(fight_points['winner'], type(fight).__name__, fight.id, winner.id, fight.category_id)
        add_historic(fight_points['loser'], type(fight).__name__, fight.id, loser.id, fight.category_id)

        is_belt_dispute = fight.belt_dispute
        update_winner_ranking(winner, fight.category_id, is_belt_dispute, fight_points['winner'])
        update_loser_ranking(loser, fight.category_id, fight_points['loser'])

def format_record(fighter: Fighter) -> Dict[str, int]:
    record = fighter.record
    victories, defeats, draws, no_contests = map(int, record.split('-'))

    victories += fighter.victories or 0
    defeats += fighter.defeats or 0
    draws += fighter.draws or 0
    no_contests += fighter.no_contests or 0

    fighter_stats = get_fighter_stats(fighter.id)

    return {
        "victories": victories,
        "defeats": defeats,
        "draws": draws,
        "no_contest": no_contests,
        "cartel": f"{victories}-{defeats}-{draws}-{no_contests}",
        "only_manager": {
            "victories": fighter.victories,
            "defeats": fighter.defeats,
            "draws": fighter.draws,
            "no_contest": fighter.no_contests,
            "cartel": f"{fighter.victories}-{fighter.defeats}-{fighter.draws}-{fighter.no_contests}",
            "wins_methods": fighter_stats['wins_methods'],
            "loss_methods": fighter_stats['loss_methods'],
        },
    }

def get_fighter_details(fighter_id):
    fighter = get_fighter(fighter_id)

    fights = get_fight_historic(fighter_id)

    return dict(fighter={
        'name': fighter.name,
        'age': fighter.age,
        'record': format_record(fighter),
        'from': fighter.country,
    }, fights=fights)

def get_fighter_stats(fighter_id: int):
    wins = get_lost_or_won_fights_grouped_by_method(fighter_id, True)
    total_wins = sum(count for _, count in wins)

    losses = get_lost_or_won_fights_grouped_by_method(fighter_id, False)
    total_losses = sum(count for _, count in losses)

    wins_methods = {
        "ko_total": 0,
        "submission_total": 0,
        "decision_total": 0,
    }
    loss_methods = {
        "ko_total": 0,
        "submission_total": 0,
        "decision_total": 0,
    }

    for method, count in wins:
        if method in ['ko', 'tko']:
            wins_methods['ko_total'] += count
        elif method == 'submission':
            wins_methods['submission_total'] += count
        elif method in ['unanimous_decision', 'majority_decision']:
            wins_methods['decision_total'] += count

    for method, count in losses:
        if method in ['ko', 'tko']:
            loss_methods['ko_total'] += count
        elif method == 'submission':
            loss_methods['submission_total'] += count
        elif method in ['unanimous_decision', 'majority_decision']:
            loss_methods['decision_total'] += count

    for key in list(wins_methods.keys()):
        if total_wins > 0:
            wins_methods[f"{key.split('_')[0]}_percentage"] = (wins_methods[key] / total_wins) * 100
        else:
            wins_methods[f"{key.split('_')[0]}_percentage"] = 0

    for key in list(loss_methods.keys()):
        if total_losses > 0:
            loss_methods[f"{key.split('_')[0]}_percentage"] = (loss_methods[key] / total_losses) * 100
        else:
            loss_methods[f"{key.split('_')[0]}_percentage"] = 0

    return {
        "wins_methods": wins_methods,
        "loss_methods": loss_methods,
    }
