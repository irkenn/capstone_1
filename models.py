"""SQLAlchemy models for Warbler."""

from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from sqlalchemy.exc import IntegrityError
from flask import flash
from sqlalchemy import Enum
import enum

db = SQLAlchemy()
bcrypt = Bcrypt()

##############################################################################
# tools

class Enum1(enum.Enum):
    album = 'album'
    artist = 'artist'
    track = 'track'
    genre = 'genre'


##############################################################################
# section for models

class SpotifyContent(db.Model):
    """Table with the id's to which the database content will be created """

    __tablename__ = 'spotify_content'

    id = db.Column(db.integer, primary_key=True)

    content_type = db.Column(Enum(Enum1))







##############################################################################

def connect_db(app):
    """Connect this database to Flask app.
    """

    db.app = app
    db.init_app(app)