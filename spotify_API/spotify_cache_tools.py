from flask import Flask, jsonify
from database.models import db, connect_db, SpotifyContent, Artist, Album, Track, ArtistTrack, ArtistAlbum, Thread  
from spotify_API.SpotifyAPI import SpotifyAPI
from utilities.search_tools import SearchTools



class SpotifyCacheTools():
    """Aids app.py in verifying if they are present in the database 
    and caching the searched items."""

    @classmethod
    def cache_spotify_content(cls, json_spotify_item_id, item_type):
        """All the content that is retrieved from Spotify's API should be included in this table,
        otherwise the database won't be able to locate such content."""

        spotify_content = SpotifyContent(id=json_spotify_item_id, content_type=item_type )
        db.session.add(spotify_content)
        db.session.commit()


    @classmethod
    def cache_artist(cls, json_spotify_artist):
        """Caches the Spotify the artist that's being passed by """

        name = json_spotify_artist['name']
        spotify_id = json_spotify_artist['id']
        external_url = json_spotify_artist['external_urls']['spotify']
        preview_url = json_spotify_artist['images'][1]['url'] if json_spotify_artist['images'] else "/static/images/default-pic.png" #on reserve, might need to add code to prevent a KeyError
        followers = json_spotify_artist['followers']['total']
        
        cached_item = Artist(spotify_id=spotify_id, 
                             name=name, 
                             preview_url=preview_url, 
                             followers=followers, 
                             external_url=external_url)
        
        db.session.add(cached_item)
        db.session.commit()
        
    
    @classmethod
    def cache_artist_album(cls, artist_id, album_id):
        """This caches the ids of the artists_albums table for a many to many relationship table """

        cached_item = ArtistAlbum(artist_id=artist_id, album_id=album_id)
        db.session.add(cached_item)
        db.session.commit()


    @classmethod
    def cache_artist_track(cls, artist_id, track_id):
        """This caches the ids of the artists_tracks table for a many to many relationship table """ 
        
        cached_item = ArtistTrack(artist_id=artist_id, track_id=track_id)
        db.session.add(cached_item)
        db.session.commit() 


    @classmethod
    def cache_album(cls, json_spotify_album):
        """Chaces the album, searches for all the artist that collaborated in the album in the database, 
        if some of the artists are not present caches them as well """

        spotify_id = json_spotify_album['id']
        name = json_spotify_album['name']
        release_date = json_spotify_album['release_date'][0:4]
        total_tracks = json_spotify_album['total_tracks']
        external_url = json_spotify_album['external_urls']['spotify']
        preview_url = json_spotify_album['images'][1]['url'] if json_spotify_album['images'] else "/static/images/default-pic.png" #on reserve, might need to add code to prevent a KeyError
        
        cached_item = Album(spotify_id= spotify_id,
                            name= name,
                            release_date= release_date,
                            total_tracks= total_tracks,
                            external_url = external_url,
                            preview_url= preview_url)
        
        db.session.add(cached_item)
        db.session.commit()

        """Search for the artists that made the album in the database """
        for artist in json_spotify_album['artists']:
            query = Artist.query.get(artist['id'])
            if not query:
                """I case the artist is not found in the databse
                is requested to de API, and then cached in the databse """
                response = SpotifyAPI.get_item("artists", artist['id'])
                cls.cache_spotify_content(artist['id'], "artist")
                
                cls.cache_artist(response.json())
                
            """If the artist was not in the database it should be included now
            at this point, so both id's will be included in the association table
            artists_albums """    

            cls.cache_artist_album(artist['id'], json_spotify_album['id'])


    @classmethod
    def cache_track(cls, json_spotify_track):
        """Chaces the track, searches for all the artist that collaborated in the track and the album 
        to which the track belong, as well as the artist album, builds on top of cache_artist()
         cache_album() functions to cache thoss items in the database """
        
        spotify_id = json_spotify_track['id']
        name = json_spotify_track['name']
        external_url = json_spotify_track['external_urls']['spotify']
        album_id = json_spotify_track['album']['id']
        
        """The album should exist in the database before caching the track """
        album_query = Album.query.get(album_id)
        if not album_query:
            album_query = SpotifyAPI.get_item("albums", album_id)
            cls.cache_spotify_content(album_id, "album")
            """This will cache more artists than it should, but doesn't seem a bad tradeoff """
            cls.cache_album(album_query.json())


        cached_item = Track(spotify_id=spotify_id, 
                            name=name, 
                            external_url=external_url, 
                            album_id=album_id)
        
        db.session.add(cached_item)
        db.session.commit()

        """Check if the artists are already in the database, if not, fetch them from the API. """
        for artist in json_spotify_track['artists']:
            query = Artist.query.get(artist['id'])
            if not query:
                """I case the artist is not found in the databse
                is requested to de API, and then cached in the databse """
                response = SpotifyAPI.get_item("artists", artist['id'])
                cls.cache_spotify_content(artist['id'], "artist")
                cls.cache_artist(response.json())
                
            """Caches each artist in artists_tracks association table """    
            cls.cache_artist_track(artist['id'], json_spotify_track['id']) 
        
  
    @classmethod
    def cache_items(cls, json_spotify_item, item_type):
        """Adds Spotify's API json object to the database"""

        """Every item should be cached in spotify_content table before."""
        cls.cache_spotify_content(json_spotify_item['id'], item_type)

        if item_type == 'artist':
            """The most basic Spotify API json object."""
            cls.cache_artist(json_spotify_item)

        elif item_type == 'album': 
            """This will search and cache artist as well if it's the case."""
            cls.cache_album(json_spotify_item)
        
        elif item_type == 'track':
            """ Either """
            cls.cache_track(json_spotify_item)


    @classmethod
    def search_cached_items_get_them_from_API_and_cached_them(cls, spotify_id, item_type, is_caching=False):
        """Checks if the spotify item is already in the database, otherwise looks up 
        for the item in Spotify's API, returns the a json object with the arrangement in 
        any of the cases"""
    
        cached = SpotifyContent.query.get(spotify_id)
        """Looks up if the item is already in the database, and returns accordingly 
        to the type of content that is listed in spotifycontent table"""

        if cached:
            """SQLAlchemy model instances are converted to JSON"""
            if cached.content_type.name == 'artist':
                artist = Artist.query.get(cached.id)
                return artist.to_dict()
            
            elif cached.content_type.name == 'album':
                album = Album.query.get(cached.id)
                return album.to_dict()
                
            elif cached.content_type.name == 'track':
                track = Track.query.get(cached.id)
                return track.to_dict()

        elif cached is None:
            """If the content is not found in the database  """
            response = SpotifyAPI.get_item(f"{item_type}s", spotify_id) # item types are passed in plural to the API
            """This will return a json object and it will handle errors if the request is not properly done"""
            json_spotify_item = SearchTools.sort_responses(response, item_type, "get")
            
            if is_caching == True:
                cls.cache_items(json_spotify_item, item_type)

        return json_spotify_item

    



    