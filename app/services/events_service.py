from datetime import datetime

from app.db_base import save_to_db, update_in_db
from app.models import Event

def get_all_events():
    return Event.query.all()

def create_new_event(description):
    new_event = Event(description=description)
    save_to_db(new_event)
    return new_event

def get_event_details(event_id):
    event = Event.query.filter_by(id=event_id).first()
    if not event:
        return None
    return event

def get_last_event_id(offset: int = 0):
    return Event.query.order_by(Event.id.desc()).offset(offset).first().id

def mark_event_completed(event_id: int) -> None:
    update_in_db(Event, {'id': event_id}, {'event_completed_at': datetime.now()})