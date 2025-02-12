from flask import Flask
from extensions import db
from datetime import datetime
import pytz
from app.routes import register_routes
from app.logging_config import setup_logging
import os

def create_app(config_name=None):
    app = Flask(__name__)
    
    app.secret_key = os.getenv('SECRET_KEY', 'asdas*d(nasd*(nD8asD8Nasdu(ansdasduN89U987')
    
    if config_name == 'testing':
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///:memory:"
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
            'SQLALCHEMY_DATABASE_URI',
            'sqlite:///db.sqlite'
        )
        app.config['ENV'] = os.getenv('FLASK_ENV', 'production')
        app.config['DEBUG'] = os.getenv('FLASK_DEBUG', '0') == '1'

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    def format_datetime(value, format="%d/%m/%Y %H:%M:%S"):
        return value

    app.jinja_env.filters['datetime'] = format_datetime
    
    db.init_app(app)
    setup_logging(app)
    register_routes(app)

    return app
