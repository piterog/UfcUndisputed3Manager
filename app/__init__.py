from flask import Flask
from extensions import db
from datetime import datetime
import pytz
from app.routes import register_routes

app = Flask(__name__)
app.secret_key = 'asdas*d(nasd*(nD8asD8Nasdu(ansdasduN89U987'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///db.sqlite"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['ENV'] = 'development'
app.config['DEBUG'] = True

def format_datetime(value, format="%d/%m/%Y %H:%M:%S"):
    if isinstance(value, datetime):
        return value.astimezone(pytz.timezone('America/Sao_Paulo')).strftime(format)
    return value

app.jinja_env.filters['datetime'] = format_datetime

db.init_app(app)

register_routes(app)
