from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session
import re

from flask_app.models import user

class Show:
    def __init__( self , data ):
        self.id = data['id']
        self.title = data['title']
        self.network = data['network']
        self.release_date = data['release_date']
        self.comments = data['comments']
        self.user_id = data ['user_id']

        self.user = None
        self.user_comments = []

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM shows"
        results = connectToMySQL('shows_schema').query_db(query)

        table = []

        for element in results:
            table.append(cls(element))
        return table
    
    @classmethod
    def save(cls,data):
        query = "INSERT INTO shows (title, network, release_date, comments, user_id) VALUES (%(title)s, %(network)s, %(release_date)s, %(comments)s, %(user_id)s);"
        return connectToMySQL("shows_schema").query_db(query, data)
    
    @classmethod
    def update(cls,data):
        query = "UPDATE shows SET title = %(title)s, network = %(network)s, release_date = %(release_date)s, comments = %(comments)s WHERE id = %(id)s;"
        return connectToMySQL("shows_schema").query_db(query, data)

    @classmethod
    def get_show_by_id(cls, data):
        query = "SELECT * FROM shows WHERE id = %s;"
        return connectToMySQL("shows_schema").query_db(query, data)
    
    @classmethod
    def get_all_shows_with_user(cls):

        query = "SELECT * FROM shows JOIN users ON shows.user_id = users.id ORDER BY comments;"
        results = connectToMySQL('shows_schema').query_db(query)
        all_shows = []
        for row in results:

            one_show = cls(row)

            one_shows_user_info = {
                
                "id": row['users.id'], 
                "first_name": row['first_name'],
                "last_name": row['last_name'],
                "email": row['email'],
                "password": row['password'],
            }

            author = user.User(one_shows_user_info)

            one_show.user = author

            all_shows.append(one_show)
            print(one_show.user.first_name)
        return all_shows
    
    @staticmethod
    def validate_show(show):
        is_valid = True

        if len(show['title']) < 3:
            flash("Title must be at least 3 characters.")
            is_valid = False

        if len(show['network']) < 3:
            flash("Network must be at least 3 characters")
            is_valid = False

        if len(show['comments']) < 3:
            flash("Comments must be at least 3 characters")
            is_valid = False

        query = "SELECT * FROM shows WHERE title = %s;"
        results = connectToMySQL("shows_schema").query_db(query, show['title'])

        show_title = ''
        if 'show_id' in session:
            show_title = Show.get_show_by_id(session['show_id'])[0]['title']


        print(results)
        print(show_title)

        if results:
            if results[0]['title'] != show_title:
                flash('Title has already been used')
                is_valid = False

        data = {
            "title":  show['title'],
            "network":  show['network'],
            "release_date":  show['release_date'],
            "comments":  show['comments']
        }

        session['description'] = data
        return is_valid
    
    @classmethod
    def delete_show(cls, id):
        query = 'DELETE FROM shows WHERE id = %s'
        return connectToMySQL('shows_schema').query_db(query, id)


