from flask import render_template, request, redirect, url_for, flash, jsonify

from app.services.events_service import mark_event_completed
from app.services.fighters_service import update_fighters_data
from app.services.fights_service import get_fight, format_fight_data, get_fight_winner_id, get_fight_loser_id, \
    update_fight_result, is_event_completed


def fight_save_results(event_id, fight_id):
    try:
        fight = get_fight(fight_id)
        if not fight:
            return "Event not found", 404

        fight_data = format_fight_data(fight.id, request.form.to_dict())

        update_fight_result(fight, fight_data)

        update_fighters_data(fight_id)

        if is_event_completed(event_id):
            mark_event_completed(event_id)

    except Exception as e:
        import traceback
        traceback.print_exc(e)
        return str(e), 500

    return redirect(url_for('event_fights', event_id=event_id))


def teste():
    fight_id = 2
    return update_fighters_data(fight_id)
    return "A"