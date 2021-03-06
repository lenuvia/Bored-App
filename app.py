"""Bored Application"""

import os
from flask import Flask
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db
from routes import bp_routes

app = Flask(__name__)
app.register_blueprint(bp_routes)

app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgres:///bored_db')).replace("://", "ql://", 1)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'shh')

# debug = DebugToolbarExtension(app)

connect_db(app)
# db.drop_all()
db.create_all()