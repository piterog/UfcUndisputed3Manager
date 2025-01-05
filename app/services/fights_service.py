from datetime import datetime
from typing import List, Any, Union
from app.db_base import update_in_db, save_to_db
from app.models import Fight, CategoryFighter
from app.services.categories_service import format_short_category
from sqlalchemy import func


def get_fight(fight_id: int) -> Fight:
    return Fight.query.filter_by(id=fight_id).first()

def get_fights_from_event(event_id: int) -> List[Fight] or None:
    return Fight.query.filter_by(event_id=event_id).all()

def create_fight(fight_data: dict) -> Fight:
    fight = Fight(**fight_data)
    save_to_db(fight)

    return fight

def format_fight_data(fight_id: int, form_data: dict) -> dict[str, Any]:
    return {
        "result": form_data.get(f"result[{fight_id}]"),
        "method": form_data.get(f"method[{fight_id}]"),
        "round": form_data.get(f"round[{fight_id}]"),
        "time": form_data.get(f"time[{fight_id}]"),
    }

def get_fight_winner_id(result: str, fight: Fight) -> Union[int, None]:
    if result == "red":
        return fight.red_corner_id
    elif result == "blue":
        return fight.blue_corner_id

    return None

def get_fight_loser_id(result: str, fight: Fight) -> Union[int, None]:
    if result == "blue":
        return fight.red_corner_id
    elif result == "red":
        return fight.blue_corner_id

    return None

def update_fight_result(fight: Fight, fight_data: dict) -> None:
    data = {
        "winner_id" : get_fight_winner_id(fight_data['result'], fight),
        "loser_id" : get_fight_loser_id(fight_data['result'], fight),
        "method" : fight_data['method'],
        "round" : fight_data['round'],
        "time" : fight_data['time'],
        "save_fight_at" : datetime.now()
    }

    update_in_db(Fight, {"id": fight.id}, data)

def is_match_drawn(fight: Fight) -> bool:
    return fight.winner_id is None and fight.loser_id is None

def count_consecutive_wins(fighter_id: int) -> int:
    fights = Fight.query.filter(
        (Fight.red_corner_id == fighter_id) | (Fight.blue_corner_id == fighter_id)
    ).order_by(
        Fight.created_at.desc()
    ).all()

    win_streak = 0
    for fight in fights:
        if fight.winner_id == fighter_id:
            win_streak += 1
        else:
            break
    return win_streak

def calculate_ranking_points(fight: Fight) -> dict[str, int]:
    winner = fight.winner
    loser = fight.loser

    winner_points = 70
    loser_points = -70

    winner_actual_ranking = CategoryFighter.query.filter_by(fighter_id=winner.id, category_id=fight.category_id).scalar().ranking
    loser_actual_ranking = CategoryFighter.query.filter_by(fighter_id=loser.id, category_id=fight.category_id).scalar().ranking

    if winner_actual_ranking < loser_actual_ranking:
        winner_points += 50
        loser_points -= 100
        print(f"STEP 1 - IF ({winner_points} | {loser_points})")
    else:
        winner_points += 25
        loser_points -= 25
        print(f"STEP 1 - ELSE ({winner_points} | {loser_points})")

    if fight.round == 1:
        winner_points += 40
        loser_points -= 35
        print(f"STEP 2[ROUND == 1]  ({winner_points} | {loser_points})")

    if fight.round == 2:
        winner_points += 20
        loser_points -= 15
        print(f"STEP 2[ROUND == 2] ({winner_points} | {loser_points})")

    if  fight.method == 'KO' or fight.method == 'SUBMISSION':
        winner_points += 20
        loser_points -= 20
        print(f"STEP 3[METHOD KO OR SUBM]  ({winner_points} | {loser_points})")

    if  fight.method == 'TKO':
        winner_points += 12
        loser_points -= 12
        print(f"STEP 3[METHOD TKO] ({winner_points} | {loser_points})")

    winner_consecutive_wins = count_consecutive_wins(winner.id)
    if winner_consecutive_wins >= 3 & winner_consecutive_wins < 5:
        winner_points += 15
        loser_points += 7
        print(f"STEP 4[WSTREAK 3~5] ({winner_points} | {loser_points})")

    if winner_consecutive_wins >= 5:
        winner_points += 25
        loser_points += 10
        print(f"STEP 4[WSTREAK 5>] ({winner_points} | {loser_points})")

    if fight.number == 1:
        winner_points += 35
        loser_points += 20
        print(f"STEP 5[NUMBER == 1] ({winner_points} | {loser_points})")
    elif fight.number == 2:
        winner_points += 25
        loser_points += 12
        print(f"STEP 5[NUMBER == 2] ({winner_points} | {loser_points})")
    elif fight.number == 3 | fight.number == 4:
        winner_points += 12
        loser_points += 5
        print(f"STEP 5[NUMBER == 3 | 4] ({winner_points} | {loser_points})")

    return {
        "winner": winner_points,
        "loser": loser_points
    }

def remove_fights_by_event(event_id: int) -> None:
    Fight.query.filter_by(event_id=event_id).delete()

def is_event_completed(event_id: int) -> bool:
    events_fights_done = Fight.query.filter(Fight.event_id == event_id,
                                              Fight.save_fight_at.isnot(None)).count()
    all_events_fight = Fight.query.filter(Fight.event_id == event_id).count()

    return events_fights_done == all_events_fight

def has_event_started(event_id: int) -> bool:
    return Fight.query.filter(Fight.event_id == event_id, Fight.save_fight_at.isnot(None)).count()


def get_opponent_id(fight_id: int, fighter_id:int) -> int:
    fight = get_fight(fight_id)
    if fight.red_corner_id == fighter_id:
        return fight.blue_corner_id

    return fight.red_corner_id

def get_fight_historic(fighter_id: int) -> dict:
    from app.services.fighters_service import get_fighter

    fights = Fight.query.filter(
                (Fight.red_corner_id == fighter_id) | (Fight.blue_corner_id == fighter_id)
            ).order_by(
                Fight.created_at.desc()
            ).all()

    fight_list = []
    for fight in fights:
        opponent_id = get_opponent_id(fight.id, fighter_id)
        result = "D"
        if fight.winner_id == fighter_id:
            result = "W"
        elif fight.loser_id == fighter_id:
            result = "L"

        fighter_controlled = False
        if fighter_id == fight.red_corner_id & fight.control == 1:
            fighter_controlled = True

        if fighter_id == fight.blue_corner_id & fight.control == 2:
            fighter_controlled = True

        fight_list.append({
            "event_id": fight.event_id,
            "event_description": fight.event.description,
            "category_id": fight.category_id,
            "category_description": fight.category.description,
            "category_short": format_short_category(fight.category.description),
            "opponent_id": opponent_id,
            "opponent_name": get_fighter(opponent_id).name,
            "belt_dispute": fight.belt_dispute,
            "result": result,
            "fighter_controlled": fighter_controlled,
            "method": fight.method,
            "time": fight.time,
            "round": fight.round
        })

    return fight_list

def get_lost_or_won_fights_grouped_by_method(fighter_id: int, winner: bool) -> list:
    filter_to_compare = Fight.winner_id if winner else Fight.loser_id

    return (Fight.query.with_entities(Fight.method, func.count(Fight.method))
            .filter(filter_to_compare == fighter_id)
            .group_by(Fight.method)
            .all())