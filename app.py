import os

from flask import Flask, render_template, request, flash, redirect, session, g, jsonify, Response
from flask_debugtoolbar import DebugToolbarExtension

from database.models import db, SpotifyContent, connect_db, User, SpotifyContent, Artist, ArtistTrack, ArtistAlbum, Track, Album, Thread, Comment
from spotify_API.SpotifyAPI import SpotifyAPI, SpotifyAPI_InstanceClass
from utilities.app_tools import AppTools
from database.user_tools import UserTools
from database.threads_tools import ThreadTools
from utilities.search_tools import SearchTools
from database.comment_tools import CommentTools


app = Flask(__name__)

# Get DB_URI from environ variable (useful for production/testing) or,
# if not set there, use development local db.
app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgresql:///spotify_comments'))

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "it's a secret")
app.config['API_CLIENT_ID'] = os.environ.get('API_CLIENT_ID', 'not found')
app.config['API_SECRET'] = os.environ.get('API_SECRET', 'not found')

toolbar = DebugToolbarExtension(app)

connect_db(app)


##############################################################################
# User signup/login/logout

@app.before_first_request
def spotify_API_credentials():
    """Communicate with Spotify's API to get a valid token. """

    SpotifyAPI.credentials_in_session()

@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if "SPOTIFY_COMMENTS_USER_KEY" in session:
        g.user = User.query.get(session["SPOTIFY_COMMENTS_USER_KEY"])
    else:
        g.user = None

##############################################################################
#Homepage-sign up page or user page

@app.route('/')
def homepage():
    """Redirects to the user page if it's active or renders the sign up page"""
    
    if not g.user:
        return render_template('home-logout.html')
    
    
    return redirect(f'/users/{g.user.id}')
    
##############################################################################
#Sign up, login and logout

@app.route('/signup', methods=['GET', 'POST'])
def signup_page():
    """Checks if any user is already logged in, otherwise sends a form to create a new user 
    and adds the user to the database""" 
    
    if not g.user:
        return UserTools.signup_handler(request)

    return AppTools.already_login(g.user)


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    """Checks if the user is already logged in, otherwise sends a login form to the user 
    and redirects to users homepage"""

    if not g.user:
        return AppTools.login_handler(request)
    
    return AppTools.already_login(g.user)
    
    
@app.route('/logout', methods=['GET', 'POST'])
def logout_page():
    """If user is not logged redirects to home, otherwise deletes current user credentials 
    and redirects the user to login page """
    
    return AppTools.do_logout()

##############################################################################
#User pages

@app.route('/users/<int:user_id>')
def userpage(user_id):
    """Redirects if currect user does not match user_id un the URL"""
    
    if not g.user:
        return redirect('/login')
    
    elif g.user.id == user_id:
        return UserTools.user_homepage_data(user_id)

    return UserTools.other_user_homepage(user_id)
    


@app.route('/users/<int:user_id>/edit', methods=['GET', 'POST'])
def edit_userpage(user_id):
    """Evaluates the state of the sessiona and renders the user a form to edit its info"""
    
    if not g.user:
        return redirect('/login')

    elif g.user.id == user_id:
        return UserTools.edit_user_handler(request, user_id)

    return AppTools.already_login(g.user)
    

@app.route('/users/<int:user_id>/delete', methods=['POST', 'GET'])
def delete_userpage(user_id):
    """Confirms the user keys are correct, sends a form and eliminates the user from the database
    if the option YES is selected, otherwise returns the user to its userpage"""
    
    if not g.user:
        return redirect('/login')
    
    elif g.user.id == user_id:
            return UserTools.delete_user_handler(request, user_id)
    
    return AppTools.already_login(g.user)
    

##############################################################################
#Search pages

@app.route('/nav-search', methods=['POST'])
def nav_search_items():
    """This will receive only POST methods that come from the nav-bar searchbox
    it will search in the database for the Spotify Content that matches the criteria
    that matched the search keywords. """

    if not g.user:
        return redirect('/login')    
    
    return SearchTools.search_thread(request.form["keyword"])


@app.route('/search/API', methods=['GET', 'POST'])
def search_items_in_API():
    """Searches in the Spotify API """
    if not g.user:
        return redirect('/login')
    
    return SearchTools.search_spotify_API(request)


@app.route('/search', methods=['GET', 'POST'])
def form_search_items():
    """ """
    if not g.user:
            return redirect('/login')  
    
    return SearchTools.form_search_thread(request)

##############################################################################
#Threads pages

@app.route('/threads/<spotify_id>/add', methods=['GET', 'POST'])
def start_new_thread(spotify_id):
    """The selected thread is displayed in its own page, a form is sent
    to start the thread on the selected item, the item is then cached and the 
    thread is stored in the databse """

    if not g.user:
        return redirect('/login')
    
    return ThreadTools.add_thread(request, spotify_id, session["SPOTIFY_COMMENTS_USER_KEY"] )



@app.route('/threads/<spotify_id>', methods=['GET', 'POST'])
def show_thread_details(spotify_id):
    """ This will show a thread and will receive upvotes or downvotes """

    if not g.user:
        return redirect('/login')

    return ThreadTools.show_thread(request, spotify_id, session["SPOTIFY_COMMENTS_USER_KEY"])   


@app.route('/user-thread/<thread_id>/', methods=['GET', 'POST'])
def show_user_thread(thread_id):
    """This will show a page with a single thread """
    
    if not g.user:
        return redirect('/login')

    return ThreadTools.user_thread(thread_id)

##############################################################################
#Threads pages

@app.route('/comments/', methods=['POST'])
def receive_comment():
    """This won't render a page, will just receive comment posts
    and incorporate them into the database"""

    if not g.user:
        return redirect('/login')
    
    return CommentTools.new_comment(request, g.user.id)
    







#This is an example of how maybe it could work
# @app.route('/threads/new', methods=['GET', 'POST'])
# def new_thread():
    
#     thread = None

#     return redirect(f"/threads/{thread.id}") 

##############################################################################
#Search pages

# @app.route('/search/threads', methods=['GET', 'POST'])
# def search_threads():
#     """Searches for existing threads in the database"""
    
#     if not g.user:
#         return redirect('/login')
    
#     ## what happens when a looged in users enters other user's route
#     elif g.user :
#         return UserTools.delete_user_handler(request)

    



