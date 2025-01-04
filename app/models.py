from app import db
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey, Integer, Boolean, DateTime
from datetime import datetime

class Fighter(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    age: Mapped[int] = mapped_column(nullable=False)
    country: Mapped[str] = mapped_column(nullable=False)
    record: Mapped[str] = mapped_column(nullable=False)
    victories: Mapped[int] = mapped_column(nullable=True, default=0)
    defeats: Mapped[int] = mapped_column(nullable=True, default=0)
    draws: Mapped[int] = mapped_column(nullable=True, default=0)
    no_contests: Mapped[int] = mapped_column(nullable=True, default=0)
    image: Mapped[str] = mapped_column(nullable=True)

class Category(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    description: Mapped[str] = mapped_column(unique=True)
    champion_id: Mapped[int] = mapped_column(Integer, ForeignKey('fighter.id'), nullable=False)
    
    fighter: Mapped[Fighter] = db.relationship("Fighter", backref="categories")
    
class CategoryFighter(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    fighter_id: Mapped[int] = mapped_column(Integer, ForeignKey('fighter.id'), nullable=False)
    category_id: Mapped[int] = mapped_column(Integer, ForeignKey('category.id'), nullable=False)
    ranking: Mapped[int] = mapped_column(Integer)
    
    fighter: Mapped[Fighter] = db.relationship("Fighter", backref="categoryfighters")
    category: Mapped[Category] = db.relationship("Category", backref="categoryfighters")
    
class Event(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    description: Mapped[str] = mapped_column(unique=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now)
    event_completed_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    
class Fight(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    number: Mapped[int] = mapped_column(nullable=True)
    event_id: Mapped[int] = mapped_column(Integer, ForeignKey('event.id'), nullable=False)
    category_id: Mapped[int] = mapped_column(Integer, ForeignKey('category.id'), nullable=False)
    red_corner_id: Mapped[int] = mapped_column(Integer, ForeignKey('fighter.id'))
    blue_corner_id: Mapped[int] = mapped_column(Integer, ForeignKey('fighter.id'))
    control: Mapped[int] = mapped_column(Integer, nullable=True)
    belt_dispute: Mapped[bool] = mapped_column(Boolean, default=False)
    winner_id: Mapped[int] = mapped_column(Integer, ForeignKey('fighter.id'), nullable=True)
    loser_id: Mapped[int] = mapped_column(Integer, ForeignKey('fighter.id'), nullable=True)
    method: Mapped[str] = mapped_column(nullable=True)
    round: Mapped[int] = mapped_column(nullable=True)
    time: Mapped[str] = mapped_column(nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.now)
    save_fight_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    
    red_corner: Mapped[Fighter] = db.relationship("Fighter", foreign_keys=[red_corner_id], backref="fights_as_red")
    blue_corner: Mapped[Fighter] = db.relationship("Fighter", foreign_keys=[blue_corner_id], backref="fights_as_blue")
    winner: Mapped[Fighter] = db.relationship("Fighter", foreign_keys=[winner_id], backref="fights_as_winner")
    loser: Mapped[Fighter] = db.relationship("Fighter", foreign_keys=[loser_id], backref="fights_as_loser")
    category: Mapped[Category] = db.relationship("Category", backref="fights")
    event: Mapped[Event] = db.relationship("Event", backref="fights")
