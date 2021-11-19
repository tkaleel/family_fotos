from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

from flask_app.models import model_album

class Photo:
    def __init__(self, data):
        self.id = data['id']
        self.photo = data['photo']
        self.name = data['name']
        self.location = data['location']
        self.description = data['description']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.album_id = data['album_id']
    @property
    def creator(self):
        return model_album.Album.get_one({'id': self.album_id})


    @classmethod
    def save(cls, data ):
        query = "INSERT INTO photos ( photo, name, location, description, album_id, created_at, updated_at ) VALUES ( %(photo)s, %(name)s, %(location)s, %(description)s, %(album_id)s, NOW() , NOW() );"
        return connectToMySQL('family_fotos_schema').query_db( query, data )
    
    @classmethod
    def get_one(cls,data):
        query  = "SELECT * FROM photos WHERE id = %(id)s;"
        result = connectToMySQL('family_fotos_schema').query_db(query,data)
        return cls(result[0])

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM photos;"
        results = connectToMySQL('family_fotos_schema').query_db(query)
        photos = []
        for photo in results:
            photos.append( cls(photo) )
        return photos
    

    @classmethod
    def update(cls,data):
        query = "UPDATE photos SET name=%(name)s, location=%(location)s, description=%(description)s, updated_at=NOW() WHERE id = %(id)s;"
        return connectToMySQL('family_fotos_schema').query_db(query,data)

    @classmethod
    def destroy(cls,data):
        query  = "DELETE FROM photos WHERE id = %(id)s;"
        return connectToMySQL('family_fotos_schema').query_db(query,data)

    @staticmethod
    def validate_photo(data):
        is_valid = True
        if not data['photo']:
            flash("You must choose a foto.", "err_photo")
            is_valid = False
        if len(data['name']) < 3:
            flash("Name must be at least 3 character.", "err_photo")
            is_valid = False
        if len(data['location']) < 3:
            flash("Location must be at least 3 characters.", "err_photo")
            is_valid = False
        if len(data['description']) < 3:
            flash("Description must be at least 3 characters.", "err_photo")
            is_valid = False
        return is_valid