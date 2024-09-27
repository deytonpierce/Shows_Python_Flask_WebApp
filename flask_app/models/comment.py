from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

from flask_app.models import user

class Comment:
    def __init__( self , data ):
        self.id = data['id']
        self.comment = data['comment']
        self.date = data['date']
        self.show_id = data['show_id']
        self.user_id = data['user_id']

        self.show = None
        self.user = None

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM comments"
        results = connectToMySQL('shows_schema').query_db(query)

        table = []

        for element in results:
            table.append(cls(element))
        return table
    
    @classmethod
    def save(cls,data):
        query = "INSERT INTO comments (comment, show_id, user_id) VALUES (%(comment)s, %(show_id)s, %(user_id)s);"
        return connectToMySQL("shows_schema").query_db(query, data)
    
    @classmethod
    def get_all_comments_with_user(cls, show_id):

        query = "SELECT * FROM comments JOIN users ON comments.user_id = users.id WHERE show_id = %s ORDER BY date DESC;"
        results = connectToMySQL('shows_schema').query_db(query, show_id)
        all_comments = []
        for row in results:

            one_comment = cls(row)

            one_comments_user_info = {
                
                "id": row['users.id'], 
                "first_name": row['first_name'],
                "last_name": row['last_name'],
                "email": row['email'],
                "password": row['password'],
            }

            author = user.User(one_comments_user_info)

            one_comment.user = author

            all_comments.append(one_comment)
            print(one_comment.user.first_name)
        return all_comments
    
    
    @classmethod
    def delete(cls, id):
        query = 'DELETE FROM comments WHERE id = %s'
        return connectToMySQL('shows_schema').query_db(query, id)
    
    @classmethod
    def get_comment_by_id(cls, data):
        query = "SELECT * FROM comments WHERE id = %s;"
        return connectToMySQL("shows_schema").query_db(query, data)