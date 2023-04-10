from flask import Flask, render_template, request
from forms import AddThreadForm
from spotify_cache_tools import SpotifyCacheTools
from models import SpotifyContent, Artist, Album, Track, Thread
from database_comments_tools import DatabaseCommentsTools


class ThreadTools():
    """Aids app.py in the handling of adding threads to the database. Works closely with SpotifyCacheTools. """


    @classmethod
    def add_thread(cls, request, spotify_id, user_id):
        """"Sends a form to start a thread about the selected spotify item. It uses 
        'search_cached_items_get_them_from_API_and_cached_them()' which is the central hub 
        of the whole caching process """
        
        form = AddThreadForm()

        """The html page 'threads.html' has a form incorporated in the request, this is to recover the kind of 
        spotify item that's being called (artist, album, track). """
        item_type = request.args['item_type']
        json_spotify_item = SpotifyCacheTools.search_cached_items_get_them_from_API_and_cached_them(spotify_id, item_type)
        
        if request.method == 'POST' and form.validate_on_submit():
            """The item is searched again using the function, because the app is stateless and there might be several requests at the same time.
            Afterward the item is cached accordingly and the thread field are attached to it"""
            item_type = request.args['item_type']
            """The third argument of the function is optional, if is true will cache the provided item in the database """
            json_spotify_item = SpotifyCacheTools.search_cached_items_get_them_from_API_and_cached_them(spotify_id, item_type, is_caching=True)
            
            thread_item = DatabaseCommentsTools.cache_thread(form, spotify_id, user_id)
            
            """This should be like a landing page of your thread about the item, then it should be moved to the usual threads/<id> route. 
            Probably display a section of other threads. It should have a button like, see who else has posted about them. """
            return render_template('threads/single-thread.html', item=json_spotify_item, item_type=f"{item_type}s", thread_item=thread_item)
            
        return render_template('threads/add.html', form=form, item=json_spotify_item, item_type=f"{item_type}s")
    

    @classmethod
    def show_thread(cls, request, spotify_id, user_id):
        """The page displays all the threads and comments for each spotify item"""
        
        current_thread = SpotifyContent.query.get(spotify_id)

        """Only spotify items with threads will have a page."""
        if not current_thread:
            return render_template('threads/not-found.html')

        item_type = current_thread.content_type_name
        
        if item_type == 'artist':
            current_item = Artist.query.get(spotify_id)
                        
        elif item_type == 'album':
            current_item = Album.query.get(spotify_id)
            
        elif item_type == 'track':
            current_item = Track.query.get(spotify_id)
        
        current_item = current_item.to_dict()

        thread_item = Thread.query.filter_by(spotify_content_id=spotify_id).all()

        return render_template('threads/detail.html', 
                                   item=current_item, 
                                   item_type=f"{item_type}s", 
                                   thread_item_list=thread_item )
            
    @classmethod
    def user_thread(cls, thread_id):
        """This will show only a single thread and its comments about the Spotify item that is about. """

        current_thread = Thread.query.get(thread_id)
        if current_thread:

            return render_template('threads/user-thread.html', thread_item=current_thread)

        return render_template('threads/not-found.html')     
    