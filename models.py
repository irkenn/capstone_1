"""SQLAlchemy models for Warbler."""

from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql import func
from flask import flash
from sqlalchemy import Enum, ForeignKey
import enum
from forms import UserAddForm

db = SQLAlchemy()
bcrypt = Bcrypt()

def connect_db(app):
    """Connect this database to Flask app."""

    db.app = app
    db.init_app(app)


##############################################################################
# tools

class Enum1(enum.Enum):
    album = 'album'
    artist = 'artist'
    track = 'track'


################################################################################
###################### MODELS RELATED TO SPOTIFY'S CONTENT #####################

class SpotifyContent(db.Model):
    """Caches the values retrieves from Spotify's API"""

    __tablename__ = 'spotify_content'

    id = db.Column(db.Text, primary_key=True)
    
    content_type = db.Column(Enum(Enum1))
    
    timestamp = db.Column(db.DateTime, 
                          nullable=False, 
                          default=datetime.utcnow())
    
    def __repr__(self):
        return f"<SpotifyContent id: {self.id} content_type: {self.content_type} timestamp: {self.timestamp}>"

    @property
    def content_type_name(self):
        return self.content_type.name


class Artist(db.Model):
    """Caches the artist"""

    __tablename__ = 'artists'

    spotify_id = db.Column(db.Text,
                           primary_key=True)
    
    name = db.Column(db.Text)
    
    external_url = db.Column(db.Text)
    
    preview_url = db.Column(db.Text)
    
    followers = db.Column(db.Integer)

    def __repr__(self):
        return f"<Artist Spotify_id: {self.spotify_id} name: {self.name}>"

    def to_dict(self):
        """Returns a dictionary just as Spotify's API does,
        so Jinja could handle when responses come from the API or from the 
        own database without any distinction."""

        return {
            'id': self.spotify_id,
            'name': self.name,
            'images' : [
                {'url': self.preview_url},
                {'url': self.preview_url}
                ],
            'followers': {
                'total': self.followers },
            'external_urls': {
                'spotify': self.external_url
            }
        }


class ArtistTrack(db.Model):
    """ Association table for a many to many relationship artist -> track"""

    __tablename__ = 'artists_tracks'

    artist_id = db.Column(db.Text, 
                            db.ForeignKey('artists.spotify_id', ondelete='cascade'), 
                            primary_key=True)
    
    track_id = db.Column(db.Text, 
                            db.ForeignKey('tracks.spotify_id', ondelete='cascade'), 
                            primary_key=True)


class ArtistAlbum(db.Model):
    """" Association table for a many to many relationship artist -> album """

    __tablename__ = 'artists_albums'

    artist_id = db.Column(db.Text, 
                            db.ForeignKey('artists.spotify_id', ondelete='cascade'), 
                            primary_key=True)
    
    album_id = db.Column(db.Text, 
                            db.ForeignKey('albums.spotify_id', ondelete='cascade'),
                            primary_key=True)
       


class Album(db.Model):
    """ Caches the albums."""

    __tablename__ = 'albums'
    
    spotify_id = db.Column(db.Text, primary_key=True)

    name = db.Column(db.Text)
    
    external_url = db.Column(db.Text)
    
    release_date = db.Column(db.Text)

    preview_url = db.Column(db.Text)  

    total_tracks = db.Column(db.Integer)

    artists = db.relationship(
                    "Artist",
                    secondary='artists_albums',
                    primaryjoin= spotify_id == ArtistAlbum.album_id,
                    secondaryjoin= Artist.spotify_id == ArtistAlbum.artist_id)
    
    tracks = db.relationship('Track', back_populates='album')

    def __repr__(self):
        return f"<Album spofity_id: {self.spotify_id} name: {self.name} release date: {self.release_date}>"
    
    def to_dict(self):
        return {
            'id': self.spotify_id,
            'name': self.name,
            'images' : [
                {'url': self.preview_url},
                {'url': self.preview_url}
                ],
            'release_date': self.release_date,
            'external_urls': {
                'spotify': self.external_url },
            'total_tracks': self.total_tracks,
            'artists': [artist.to_dict() for artist in self.artists ],
            'tracks': [track.to_dict() for track in self.tracks]
        }

class Track(db.Model):
    """Caches the songs"""

    __tablename__ = 'tracks'
    
    spotify_id = db.Column(db.Text, primary_key=True)
    
    name = db.Column(db.Text)
    
    external_url = db.Column(db.Text)
    
    artists = db.relationship(
                    "Artist",
                    secondary='artists_tracks',
                    primaryjoin= spotify_id == ArtistTrack.track_id,
                    secondaryjoin= Artist.spotify_id == ArtistTrack.artist_id)
    
    album_id = db.Column(db.Text, 
                         db.ForeignKey('albums.spotify_id', ondelete='cascade'))

    album = db.relationship('Album', back_populates='tracks')

    def __repr__(self):
        return f"<Track spotify id: {self.spotify_id} title: {self.name}>"

    def to_dict(self):
        return {
            'id': self.spotify_id,
            'name': self.name,
            'external_urls': {
                'spotify': self.external_url },
            'artists': [artist.to_dict() for artist in self.artists ],
            'album': {
                'id': self.album.spotify_id,
                'name': self.album.name,
                'images' : [
                    {'url': self.album.preview_url},
                    {'url': self.album.preview_url}],
                'release_date': self.album.release_date
                }
            }

##############################################################################

class Thread(db.Model):
    """spotify content set's a one-to-many relationship between 'spotify_content' and 'threads' created the thread"""

    __tablename__ = 'threads'

    def __repr__(self):
        return f"<Thread id: {self.id} user: {self.user_id} title: {self.title} spotify_content: {self.spotify_content_id} >"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    user_id = db.Column(db.Integer, 
                        db.ForeignKey('users.id', ondelete='cascade'))

    spotify_content_id = db.Column(db.Text, 
                                   db.ForeignKey('spotify_content.id', ondelete='cascade'))

    title = db.Column(db.Text, nullable=False)

    description = db.Column(db.Text)

    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    
    user = db.relationship("User", back_populates='threads')

    comments = db.relationship("Comment", backref="threads")
    
    thread_votes = db.relationship("ThreadVote", backref="thread")
    
    
class Comment(db.Model):
    """Comments can only exist over a thread  """
    
    __tablename__ = 'comments'

    def __repr__(self):
        return f"<Comment id: {self.id} user: {self.user_id} content: {self.content}>"
    
    id = db.Column(db.Integer, 
                   primary_key=True, 
                   autoincrement=True)
    
    user_id = db.Column(db.Integer, 
                        db.ForeignKey('users.id', ondelete='cascade'),
                        nullable=False)
    
    thread_id = db.Column(db.Integer, 
                          db.ForeignKey('threads.id', ondelete='cascade'),
                          nullable=False)
    
    content = db.Column(db.Text)

    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())

    user = db.relationship('User', back_populates='comments')

    


class SubComment(db.Model):
    """This are comments that bind to another comment"""

    __tablename__ = "subcomments"

    def __repr__(self):
        return f"<Subcomment id: {self.id} content : {self.content} >"
    
    id = db.Column(db.Integer, 
                   primary_key=True, 
                   autoincrement=True)

    user_id = db.Column(db.Integer, 
                        db.ForeignKey('users.id', ondelete='cascade'),
                        nullable=False)

    comment_id = db.Column(db.Integer, 
                          db.ForeignKey('comments.id', ondelete='cascade'),
                          nullable=False)

    content = db.Column(db.Text)

    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())

    user = db.relationship('User', back_populates='subcomments')



class ThreadVote(db.Model):
    """This will count the votes per Thread a user can only vote once. """ 
    
    __tablename__ = 'threads_votes'

    def __repr__(self):
        return f"<ThreadVote user_id: {self.user_id} thread_id: {self.thread_id} vote{self.vote}>"
    
    
    user_id = db.Column(db.Integer, 
                        db.ForeignKey('users.id', ondelete='cascade'), 
                        primary_key=True)
    
    thread_id = db.Column(db.Integer, 
                            db.ForeignKey('threads.id', ondelete='cascade'), 
                            primary_key=True)
    
    vote = db.Column(db.Integer, 
                     info={'choices': [(1, '+1'), (-1, '-1')]}, 
                     nullable=False)

################################################################################
########## MODELS RELATED TO WEBSITE'S DATABASE USER-THREADS-COMMENTS ##########

class User(db.Model):
    """Stores all the information related to the user"""

    __tablename__ = "users"

    def __repr__(self):
        return f"<User #{self.id}: {self.username}, {self.email}>"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    username = db.Column(db.String(50), nullable=False, unique=True)
    
    email = db.Column(db.String(70), nullable=False, unique=True)
    
    password = db.Column(db.Text, nullable=False)

    image_url = db.Column(db.Text, default="/static/images/default-pic.png")

    comments = db.relationship("Comment", back_populates="user")

    subcomments = db.relationship("SubComment", back_populates="user")

    threads = db.relationship("Thread", back_populates="user")
    

    @classmethod
    def signup(cls, form):
        """Sign up user. Hashes password and adds user to system."""
        
        hashed_pwd = bcrypt.generate_password_hash(form.password.data).decode('UTF-8')

        user = User(
            username=form.username.data,
            email=form.email.data,
            password=hashed_pwd,
            image_url=form.image_url.data or cls.image_url.default.arg
            )
        db.session.add(user)
        
        return user
    
    @classmethod
    def authenticate(cls, username, password):
        """Find user with `username` and `password`.

        This is a class method (call it on the class, not an individual user.)
        It searches for a user whose password hash matches this password
        and, if it finds such a user, returns that user object.

        If can't find matching user (or if password is wrong), returns False.
        """
        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user
        return False

##############################################################################