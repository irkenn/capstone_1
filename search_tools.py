from flask import Flask, render_template, request, flash, g
from forms import SearchSpotifyForm
from SpotifyAPI import SpotifyAPI

        
class SearchTools():
    """Aids app.py in the search of items with Spotify's API. Integrates with SpotifyAPI.py class, managing the 
     interaction between those API methods and Flask. """

    @classmethod
    def sort_responses(cls, resp, item_type, search_or_get):
        """ Takes the response, transforms it into JSON and returns only the relevant info
         or error description."""

        if resp.status_code == 200:
            response = resp.json()
            if search_or_get == "search": 
                """Spotify's API returns the item type on plural, the line bellow saves a couple of lines in the Jinja template.""" 
                return response[f"{item_type}s"]['items']    
            """The response of a 'GET' method doesn't require further treatment, the returned object is less complex."""
            return response

        elif resp.status_code in [204, 400, 403, 404, 429, 503]:
            """The list is a collection of the typical status codes that Spotify's API might return if the request is not made properly. 
            It doesn't cover all the cases"""
            response = resp.json()
            flash(f"Couldn't complete your search due to this error: {response['error']['message']}, please try again", "danger")
            return None
        return None

    @classmethod
    def search_spotify_API(cls, request):
        """Retrieves values from the session """

        form = SearchSpotifyForm()
        if request.method == 'POST' and form.validate_on_submit():
            keywords = form.keywords.data
            form_item_type = form.item_type.data
            limit = form.limit.data or 5

            offset = 1 #This does not appear in the form, it's added later for pagination
            
            response = SpotifyAPI.search_item(query_string=keywords, 
                                               item_type= form_item_type, 
                                               limit=limit)
            json_response = cls.sort_responses(response, form_item_type, "search")
            
            return render_template('threads/search.html', form=form, response=json_response, item_type=form_item_type)
  
        return render_template('threads/search.html', form=form)
