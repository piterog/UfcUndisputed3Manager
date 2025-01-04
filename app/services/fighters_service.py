from typing import Optional, Dict
from app.models import Fighter, CategoryFighter
from app.db_base import update_in_db
from app.services.categories_service import set_new_champion
from app.services.category_fighters_service import get_fighter_ranking, update_ranking
from app.services.fights_service import get_fight, is_match_drawn, calculate_ranking_points


def get_all_fighters():
    return Fighter.query.all()

def get_fighter(fighter_id) -> Optional[Fighter]:
    return Fighter.query.filter_by(id=fighter_id).first()

def get_by_category(category_id: int):
    return Fighter.query.join(CategoryFighter, Fighter.id == CategoryFighter.fighter_id).filter(
        CategoryFighter.category_id == category_id).all()

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
    if points > 999:
        points = 999

    if is_belt_dispute:
        points = 1000
        set_new_champion(category_id, fighter.id)

    update_ranking(fighter.id, category_id, points)

def update_loser_ranking(fighter: Fighter, category_id: int, ranking_points: int) -> None:
    actual_ranking = get_fighter_ranking(fighter.id, category_id)

    ranking_points += actual_ranking

    update_ranking(fighter.id, category_id, ranking_points)

# def update_fighters_data(fight_id: int) -> None:
def update_fighters_data(fight_id: int):
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
        update_in_db(Fighter, {'id': loser.id}, {'defeats': loser.defeats + 1})

        fight_points = calculate_ranking_points(fight)

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

    return {
        "victories": victories,
        "defeats": defeats,
        "draws": draws,
        "no_contest": no_contests,
        "cartel": f"{victories}-{defeats}-{draws}-{no_contests}",
    }