from typing import List, Dict
from app.db_base import save_to_db
from app.models import Reward
from app.services.category_fighters_service import update_ranking, get_fighter_ranking
from app.services.fights_service import get_fight
from app.services.ranking_historics_service import add_historic


def add_rewards(rewards: List[Dict[str, List[str]]]) -> None:
    for reward in rewards:
        best_fight = reward.get('best_fight')
        if best_fight:
            fight = get_fight(best_fight)
            if fight:
                add_best_fight(fight.winner.id, fight.loser.id, fight.id, fight.category_id, fight.event_id)

        best_submission = reward.get('best_submission')
        if best_submission:
            fight = get_fight(best_submission)
            if fight:
                add_reward("submission", fight.winner_id, fight.id, fight.category_id, fight.event_id)

        best_ko = reward.get('best_ko')
        if best_ko:
            fight = get_fight(best_ko)
            if fight:
                add_reward("ko", fight.winner_id, fight.id, fight.category_id, fight.event_id)

        best_performance = reward.get('best_performance')
        if best_performance:
            fight = get_fight(best_performance)
            if fight:
                add_reward("performance", fight.winner_id, fight.id, fight.category_id, fight.event_id)

def add_best_fight(winner_id: int, loser_id: int, fight_id: int, category_id: int, event_id: int) -> None:
    add_reward("fight", winner_id, fight_id, category_id, event_id)
    update_ranking(winner_id, category_id, get_fighter_ranking(winner_id, category_id) + 30)
    add_reward("fight", loser_id, fight_id, category_id, event_id)
    update_ranking(loser_id, category_id, get_fighter_ranking(loser_id, category_id) + 30)

def add_reward(type_reward: str, fighter_id: int, fight_id: int, category_id: int, event_id: int) -> None:
    reward = save_to_db(Reward(type=type_reward, fighter_id=fighter_id, fight_id=fight_id, event_id=event_id))
    update_ranking(fighter_id, category_id, get_fighter_ranking(fighter_id, category_id) + 30)
    add_historic(30, type(reward).__name__, reward.id, fighter_id, category_id)

def has_reward(event_id: int) -> bool:
    return Reward.query.filter_by(event_id=event_id).count() > 0

def get_rewards(event_id: int):
    return Reward.query.filter_by(event_id=event_id).all()

def get_rewards_details(event_id: int):
    all_rewards = get_rewards(event_id)

    award_list = []
    previous_type = None
    previous_fighter = None

    for reward in all_rewards:
        current_type = reward.type

        if current_type == previous_type and current_type == "fight":
            fighter_name = f"{reward.fighter.name} vs {previous_fighter}"
            award_list.pop()
        else:
            fighter_name = reward.fighter.name

        award_list.append({
            'winner_fighter': fighter_name,
            'fighters': f"{reward.fight.red_corner.name} vs {reward.fight.blue_corner.name}",
            'fight_number': reward.fight.number,
            'round': reward.fight.round,
            'time': reward.fight.time,
            'type': current_type,
        })

        if current_type == "fight":
            previous_fighter = fighter_name
            previous_type = current_type
        else:
            previous_type = None
            previous_fighter = None

    return award_list