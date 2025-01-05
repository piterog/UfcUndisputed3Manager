from flask import render_template, request, redirect, url_for, flash, jsonify
from app.services.fighters_service import get_all_fighters, get_by_category, format_record, get_fighter_details


def index():
    return render_template('fighters.html', fighters=get_all_fighters())

def fighters_by_category(category_id: int):
    fighters = get_by_category(category_id)

    obj = []

    for fighter in fighters:
        fighter = {
            'id': fighter.id,
            'name': fighter.name,
            'record': format_record(fighter)
        }

        obj.append(fighter)

    return jsonify(obj)

def details(fighter_id: int):
    return jsonify(get_fighter_details(fighter_id))
