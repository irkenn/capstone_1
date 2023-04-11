"""Models test"""

import os
from unittest import TestCase

from models import db, User, Thread, Comment, SpotifyContent, Artist, Album, Track
from flask import Flask, session, request, make_response, Response
from werkzeug.datastructures import MultiDict
from search_tools import SearchTools
from threads_tools import ThreadTools

os.environ['DATABASE_URL'] = "postgresql:///spotify_comments_test"

from app import app

db.drop_all()
db.create_all()

app.config['WTF_CSRF_ENABLED'] = False


class CreateSpotifyContentAndThreads(TestCase):
    """Test for creating a user. """

    def setUp(self):
        """Create the test cliend and sample data. """

        User.query.delete()
        SpotifyContent.query.delete()
        Thread.query.delete()

        self.client = app.test_client()

        self.testuser = User(username="TestUser1",
                                    email="test@test.com",
                                    password='TestTest',
                                    image_url=None)
        
        self.testuser2 = User(username="TestUser2",
                                    email="test2@test2.com",
                                    password='Test2Test2',
                                    image_url=None)
        
        self.artist = Artist(name="Radiohead", 
                            spotify_id='4Z8W4fKeB5YxbusRsdQVPb', 
                            external_url="https://open.spotify.com/artist/4Z8W4fKeB5YxbusRsdQVPb", 
                            preview_url="https://i.scdn.co/image/ab67616100005174a03696716c9ee605006047fd", 
                            followers=7897830)

        self.spo_art = SpotifyContent(content_type='artist', id='4Z8W4fKeB5YxbusRsdQVPb')

        db.session.add(self.testuser)
        db.session.add(self.testuser2)
        db.session.add(self.artist)
        db.session.add(self.spo_art)
        db.session.commit()


    def tearDown(self):
        """Clean fouled transactions. """

        db.session.rollback()
    
    def test_search_spotify_content(self):
        """ As user search for Spotify Content and start a thread about it. """

        with self.client as c:
            with c.session_transaction() as sess:
                sess["SPOTIFY_COMMENTS_USER_KEY"] = self.testuser.id

        data = MultiDict([('keywords', 'Dua Lipa'),
                          ('form_item_type', 'artist'),
                          ('limit', 1)])

        with app.test_request_context('/search/API', data=data, method='POST'):
            response = SearchTools.search_spotify_API(request)

            resp = Response(response)
    
            self.assertEqual(200, resp.status_code)
            self.assertIn(b'Dua Lipa', resp.data)
    
    def test_add_thread(self):
        """Create a thread about a content"""

        with self.client as c:
            with c.session_transaction() as sess:
                sess["SPOTIFY_COMMENTS_USER_KEY"] = self.testuser.id

        data = MultiDict([ ('title', 'I love this band'),
                            ('description', 'This is a description')])
        spotify_id = '4Z8W4fKeB5YxbusRsdQVPb'

        with app.test_request_context(f'/threads/{spotify_id}/add?item_type=artist', data=data, method='POST'):
            response = ThreadTools.add_thread(request, spotify_id, self.testuser.id )

            resp = Response(response)
            print("############## response #############", response)
            
            self.assertEqual(200, resp.status_code)
            self.assertIn(b'Radiohead', resp.data)
        
            




        # """Search for Spotify Content. """        
        # resp = c.post("/search/API", data={"keywords": "Dua Lipa",
        #                                    "form_item_type": "artist",
        #                                     "limit": 1 })

        # # html = resp.get_data(as_text=True)
        # # self.assertIn("Dua Lipa", html)
        # self.assertEqual(resp.status_code, 200)






