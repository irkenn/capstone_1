from flask import Flask, jsonify
from models import db, connect_db, Thread



class DatabaseCommentsTools():
    """"Works in conjunction with ThreadTools. Caches threads comments, subcoments and votes """
    

    #threads should be cached
    #threads should be queried and displayed
    

    @classmethod
    def cache_thread(cls, form, spotify_id, user_id):
        """Will store the thread in the database """

        title = form.title.data
        description = form.description.data
        cached_item = Thread(user_id= user_id,
                                spotify_content_id=spotify_id, 
                                title=title, 
                                description=description)

        db.session.add(cached_item)
        db.session.commit()
            
        return cached_item
    
