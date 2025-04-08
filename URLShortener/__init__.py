from flask import Flask
from flask_cors import CORS
from .db import db
from .main import main_bp
from .redirect import redirect_bp
from log.debug_print import dprint
import os
from dotenv import load_dotenv

load_dotenv('../.env')  # Load environment variables from .env file

def create_app():
    """
    Create and configure the Flask application.
    """
    app = Flask(__name__)
    
    CORS(app)
    environ = os.environ.get('FLASK_ENV')
    
    if environ == 'production':
        app.config.from_object('conf.config.ProductionConfig')
    elif environ == 'testing':
        app.config.from_object('conf.config.TestingConfig')
    elif environ == 'development':   # Default to development
        app.config.from_object('conf.config.DevelopmentConfig')

    return app

def add_db_to_app(app):
    """
    Initialize the database with the Flask app.
    """
    db.init_app(app)
    return db




app = create_app()
cfg = app.config.copy()

dprint(cfg)

db = add_db_to_app(app)
app.register_blueprint(main_bp)
app.register_blueprint(redirect_bp)

from . import models

with app.app_context():
    db.create_all()  # Creates tables automatically based on models