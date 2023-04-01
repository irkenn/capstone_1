from flask import Flask, jsonify
from models import db, connect_db, Thread, Comment
import json



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
    
    @classmethod
    def cache_comment(cls, json_data):
        """Will store the comment in the database, add/commit 
        and convert it into a dictionary with .to_dict() """

        user_id = json_data["user_id"]
        thread_id = json_data["thread_id"]
        comment = json_data["comment"]

        cached_item = Comment( user_id=int(user_id), 
                              thread_id=int(thread_id), 
                              content=comment)

        db.session.add(cached_item)
        db.session.commit()
        
        json_cached_item = cached_item.to_dict()
        
        return json_cached_item
    
    
