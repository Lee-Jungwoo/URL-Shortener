from flask import Flask
from flask_cors import CORS
from .db import db
from .main import main_bp
import json




def create_app():
    """
    Create and configure the Flask application.
    """
    app = Flask(__name__)
    CORS(app)
    return app


def add_db_to_app(app):
    
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin:0225@localhost/urlshortener'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    return db




app = create_app()
db = add_db_to_app(app)
app.register_blueprint(main_bp)

from . import models

with app.app_context():
    db.create_all()  # Creates tables automatically based on models