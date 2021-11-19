from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import model_user, model_photo

class Album:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.photos = []
        # self.user_id = data['user_id']
    @property
    def creator(self):
        return model_user.User.get_one({'id': self.user_id})


    @classmethod
    def save(cls, data ):
        query = "INSERT INTO albums ( name, description, user_id, created_at, updated_at ) VALUES ( %(name)s, %(description)s, %(user_id)s, NOW() , NOW() );"
        return connectToMySQL('family_fotos_schema').query_db( query, data )
    
    @classmethod
    def get_one(cls,data):
        query  = "SELECT * FROM albums WHERE id = %(id)s;"
        result = connectToMySQL('family_fotos_schema').query_db(query,data)
        return cls(result[0])

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM albums;"
        results = connectToMySQL('family_fotos_schema').query_db(query)
        albums = []
        for sighting in results:
            albums.append( cls(sighting) )
        return albums
    
    @classmethod
    def get_album_with_photos(cls, data):
        query = "SELECT * FROM albums LEFT JOIN photos ON photos.album_id = albums.id WHERE albums.id = %(id)s;"
        results = connectToMySQL('family_fotos_schema').query_db(query, data)
        album_photos = cls(results[0])
        for row_from_db in results:
            photo_data = {
                "id" : row_from_db["photos.id"],
                "photo" : row_from_db["photo"],
                "name" : row_from_db["photos.name"],
                "location" : row_from_db["location"],
                "description" : row_from_db["photos.description"],
                "created_at" : row_from_db["photos.created_at"],
                "updated_at" : row_from_db["photos.updated_at"],
                "album_id" : album_photos.id
            }
            album_photos.photos.append( model_photo.Photo( photo_data ))
        return album_photos

    @classmethod
    def update(cls,data):
        query = "UPDATE albums SET name=%(name)s, description=%(description)s, updated_at=NOW() WHERE id = %(id)s;"
        return connectToMySQL('family_fotos_schema').query_db(query,data)

    @classmethod
    def destroy(cls,data):
        query  = "DELETE FROM albums WHERE id = %(id)s;"
        return connectToMySQL('family_fotos_schema').query_db(query,data)

    @staticmethod
    def validate_albums(data):
        is_valid = True
        if len(data['name']) < 3:
            flash("Please choose a name with at least 3 characters.", "err_album")
            is_valid = False
        if len(data['description']) < 3:
            flash("Description must be at least 3 characters.", "err_album")
            is_valid = False
        return is_valid