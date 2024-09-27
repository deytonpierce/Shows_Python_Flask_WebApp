from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

class User:
    def __init__( self , data ):
        self.id = data['id']

        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']

        self.shows = []


    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users"
        results = connectToMySQL('shows_schema').query_db(query)

        table = []

        for element in results:
            table.append(cls(element))
        return table
    
    @classmethod
    def save(cls,data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        return connectToMySQL("shows_schema").query_db(query, data)
    
    @classmethod
    def get_password(cls, email):
        query = 'SELECT password FROM users WHERE email = %s'
        return connectToMySQL('shows_schema').query_db(query, email)
    
    @classmethod
    def get_user(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL("shows_schema").query_db(query, data)

        if len(result) < 1:
            return False
        return cls(result[0])
    
    @classmethod
    def get_user_by_id(cls, data):
        query = "SELECT * FROM users WHERE id = %s;"
        return connectToMySQL("shows_schema").query_db(query, data)

    @staticmethod
    def validate_user(user):
        print(user)
        is_valid = True
        if len(user['first_name']) < 2:
            flash("First name must be at least 2 characters.", 'register')
            is_valid = False
        if len(user['last_name']) < 2:
            flash("Last name must be at least 2 characters", 'register')
            is_valid = False
        existing_user = User.get_user({'email': user['email']})
        if existing_user:
            flash("Email already exists in the database.", 'register')
            is_valid = False
        # Email format validation
        if not re.match(r'^\S+@\S+\.\S+$', user['email']):
            flash("Email is not in a valid format", 'register')
            is_valid = False
        if user['register_password_1'] != user['register_password_2']:
            flash("Passwords do not match", 'register')
            is_valid = False
        if len(user['register_password_1']) < 8:
            flash("Password must be at least 8 characters", 'register')
            is_valid = False
        return is_valid
