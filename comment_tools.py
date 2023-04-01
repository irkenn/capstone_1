from flask import jsonify
from database_comments_tools import DatabaseCommentsTools


class CommentTools():
    """Aids app.py in the handling of the comment routes"""

    @classmethod
    def new_comment(cls, request, user_id):
        """ Handles the axios request converts it to JSON and caches the comment"""
        new_comment_json = request.get_json()

        if user_id == int(new_comment_json["user_id"]):
            response = DatabaseCommentsTools.cache_comment(new_comment_json)
            return jsonify(response), 201
        
        data = {"message": "user trying to make the comment does not match the user logged in"}
        return jsonify(data), 400

    

