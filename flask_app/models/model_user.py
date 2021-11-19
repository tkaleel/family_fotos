from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import model_album, model_photo
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class User:
    def __init__(self, data):
        self.id = data['id']
        self.username = data['username']
        self.email_address = data['email_address']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.albums = []
# *****************CREATE****************
    @classmethod
    def save(cls, data ):
        query = "INSERT INTO users ( username, email_address, password, created_at, updated_at ) VALUES ( %(username)s, %(email_address)s, %(password)s , NOW() , NOW() );"
        # data is a dictionary that will be passed into the save method from server.py
        return connectToMySQL('family_fotos_schema').query_db( query, data )
# ****************RETRIEVE*****************
    @classmethod
    def get_one(cls,data):
        query  = "SELECT * FROM users WHERE id = %(id)s;"
        result = connectToMySQL('family_fotos_schema').query_db(query,data)
        return cls(result[0])
    
    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email_address = %(email_address)s;"
        result = connectToMySQL('family_fotos_schema').query_db(query,data)
        if len(result) <1:
            return False
        return cls(result[0])

    @classmethod
    def get_user_with_albums(cls, data):
        query = "SELECT * FROM users LEFT JOIN albums ON albums.user_id = users.id WHERE users.id = %(id)s;"
        results = connectToMySQL('family_fotos_schema').query_db(query, data)
        user_albums = cls(results[0])
        for row_from_db in results:
            album_data = {
                "id" : row_from_db["albums.id"],
                "name" : row_from_db["name"],
                "description" : row_from_db["description"],
                "created_at" : row_from_db["albums.created_at"],
                "updated_at" : row_from_db["albums.updated_at"]
            }
            user_albums.albums.append( model_album.Album( album_data ))
        return user_albums


#*************VALIDATE************** 
    @staticmethod
    def validate_user(data):
        is_valid = True
        if len(data['username']) < 3:
            flash("Please select a username that is at least 3 characters.", "err_register")
            is_valid = False
        if len(data['password']) < 8:
            flash("Password must be at least 8 characters.", "err_register")
            is_valid = False
        if data['password'] != data['confirm_password']:
            flash("Passwords must match.", "err_register")
            is_valid = False
        if not EMAIL_REGEX.match(data['email_address']):
            flash("Invalid email address!", "err_register")
            is_valid = False
        return is_valid
    
    @staticmethod
    def validate_login(data):
        is_valid = True
        if not EMAIL_REGEX.match(data['email_address']):
            flash("Invalid email address!", "err_login")
            is_valid = False
        if len(data['password']) < 8:
            flash("Password must be at least 8 characters.", "err_login")
            is_valid = False
        return is_valid
    