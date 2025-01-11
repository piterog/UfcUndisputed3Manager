from flask import render_template, request, redirect, url_for, flash, jsonify
from app.services.events_service import mark_event_completed
from app.services.fighters_service import update_fighters_data
from app.services.fights_service import get_fight, format_fight_data, update_fight_result, is_event_completed
from app.services.ranking_history_service import snapshot_fighters


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
            snapshot_fighters()
            return redirect(url_for('event_awards', event_id=event_id))

    except Exception as e:
        import traceback
        traceback.print_exc(e)
        return str(e), 500

    return redirect(url_for('event_fights', event_id=event_id))