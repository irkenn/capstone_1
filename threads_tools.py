from flask import Flask, render_template, request
from forms import AddThreadForm
from spotify_cache_tools import SpotifyCacheTools
from database_comments_tools import DatabaseCommentsTools


class ThreadTools():
    """Aids app.py in the handling of adding threads to the database. Works closely with SpotifyCacheTools. """


    @classmethod
    def add_thread(cls, request, spotify_id, user_id):
        """"Sends a form to start a comment about the selected spotify item 
        'search_cached_items_get_them_from_API_and_cached_them()' is the central hub 
        for the whole caching process """
        
        form = AddThreadForm()
        item_type = request.args['item_type'] # !!!!!! THIS LINE NEEDS TO BE CORRECTED, THE VARIABLE IS STORED IN THE SERVER add a form with the same argument so it can be requested again in the POST method.
        json_spotify_item = SpotifyCacheTools.search_cached_items_get_them_from_API_and_cached_them(spotify_id, item_type)
        
        if request.method == 'POST' and form.validate_on_submit():
            """The item is searched again using the funciton, because the app is stateless and there might be several requests at the same time.
            Afterward the item is cached accordingly and the thread field are attached to it"""
            
            item_type = request.args['item_type']
            """The third argument of the function is optional, if is true will cache the provided item in the database """
            json_spotify_item = SpotifyCacheTools.search_cached_items_get_them_from_API_and_cached_them(spotify_id, item_type, True)
            
            thread_item = DatabaseCommentsTools.cache_thread(form, spotify_id, user_id)
            

            return render_template('threads/detail.html', spotify_item=json_spotify_item, item_type=f"{item_type}s", thread_item=thread_item)
            #while querying is better to use filter_by and .first() than get, in order to avoid an error. Not really, you can use get_or_404()
            
            

        return render_template('threads/add.html', form=form, spotify_item=json_spotify_item, item_type=f"{item_type}s")
    

    @classmethod
    def show_thread(cls, request, spotify_id, user_id):

        return None