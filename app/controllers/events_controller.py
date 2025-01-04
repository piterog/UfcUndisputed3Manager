from flask import render_template, request, redirect, url_for, flash
from app.services.categories_service import get_all_categories
from app.services.events_service import (
    get_all_events,
    get_event_details,
    create_new_event,
)
from app.services.fighters_service import get_all_fighters
from app.services.fights_service import get_fights_from_event, remove_fights_by_event, create_fight, has_event_started
from app.forms.event import EventForm


def index():
    events = get_all_events()
    for item in events:
        item.started = has_event_started(item.id)

    return render_template('events.html', events=events)

def event_build(event_id: int):
    event = get_event_details(event_id)
    fighters = get_all_fighters()
    categories = get_all_categories()
    fights = get_fights_from_event(event_id)

    if not event:
        return redirect(url_for('events'))
    return render_template('event_build.html', event=event, fighters=fighters, categories=categories, fights=fights)

def event_fights(event_id: int):
    fights = get_fights_from_event(event_id)
    event = get_event_details(event_id)
    return render_template('event_fights.html', fights=fights, event=event)

def create_event():
    form = EventForm()
    if form.validate_on_submit():
        new_event = create_new_event(form.description.data)
        return redirect(url_for('event_build', event_id=new_event.id))
    return render_template('event_form.html', form=form)

def event_schedule(event_id: int):
    selected_red_fighters = request.form.getlist('red-fighters[]')
    selected_blue_fighters = request.form.getlist('blue-fighters[]')
    selected_categories = request.form.getlist('categories[]')
    belts = request.form.getlist('belt[]')
    controls = request.form.getlist('control[]')

    if not (len(selected_red_fighters) == len(selected_blue_fighters) == len(selected_categories)):
        return {
            "error": "Mismatch in the number of red fighters, blue fighters, and categories.",
            "details": {
                "red_fighters_count": len(selected_red_fighters),
                "blue_fighters_count": len(selected_blue_fighters),
                "categories_count": len(selected_categories)
            }
        }, 400

    remove_fights_by_event(event_id)

    for index, item in enumerate(selected_categories):
        create_fight({
            'number': index + 1,
            'event_id': event_id,
            'red_corner_id': selected_red_fighters[index],
            'blue_corner_id': selected_blue_fighters[index],
            'category_id': selected_categories[index],
            'control': controls[index],
            'belt_dispute': belts[index].lower() == 'true'
        })

    return redirect(url_for('events'))