"""Models test"""

import os
from unittest import TestCase

from models import db, User, Thread, Comment, SpotifyContent, Artist, Album, Track
from flask import Flask, session

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
        
        
        db.session.commit()


    def tearDown(self):
        """Clean fouled transactions. """

        db.session.rollback()
    
    def test_create_spotify_content_and_thread(self):
        """ As user search for Spotify Content and start a thread about it. """


        with self.client as c:
            with c.session_transaction() as sess:
                sess["SPOTIFY_COMMENTS_USER_KEY"] = self.testuser.id


        """Search for Spotify Content. """        
        resp = c.post("/search/API", data={"keywords": "Dua Lipa",
                                           "form_item_type": "artist",
                                            "limit": 1 })

        # html = resp.get_data(as_text=True)
        # self.assertIn("Dua Lipa", html)
        self.assertEqual(resp.status_code, 200)






