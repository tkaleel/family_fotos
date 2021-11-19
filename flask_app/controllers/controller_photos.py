from flask_app import app, render_template, request, redirect, session, flash
from flask_app.models.model_photo import Photo
from flask_app.models.model_user import User
from flask_app.models.model_album import Album
import os.path

@app.route("/upload")
def new_photo():
    data = {
        "id": session['id']
    }
    all_albums=User.get_user_with_albums(data)
    return render_template("upload.html", all_albums=all_albums)

@app.route('/process_photo', methods=['POST'])
def create_photo():
    # if not Photo.validate_photo(request.form):
    #     return redirect('/upload')
    
    album = request.form['album_id']
    filename = request.form['name']

    data = {
        "photo" : f"{album}_{request.form['name']}",
        "name" : request.form['name'],
        "location" : request.form['location'],
        "description" : request.form['description'],
        "album_id" : request.form['album_id']
    }
    
    photo = request.files.get('photo')
    print(photo)
    if photo:
        photo.save(os.path.join(app.static_folder, f"img/{album}_{filename}.jpg"))

    Photo.save(data)
    return redirect("/dashboard")
    # should I return to album instead??

@app.route("/show_photo/<int:id>")
def show_photo(id):
    print("Showing the User the Photo")
    data = {
        "id":id
        }
    photo=Photo.get_one(data)
    return render_template("show.html", photo=photo)

@app.route("/edit_photo/<int:id>")
def edit_photo(id):
    data = {"id":id}
    session['photo_id'] = id 
    photo=Photo.get_one(data)
    return render_template("edit.html", photo=photo)

@app.route('/update_photo',methods=['POST'])
def update_photo():
    photo_id = session['photo_id']
    if not Photo.validate_photo(request.form):
        return redirect(f"/edit/{photo_id}")
    Photo.update(request.form)
    return redirect("/dashboard")

@app.route("/destroy_photo/<int:id>")
def destroy_photo(id):
    data ={'id': id}
    Photo.destroy(data)
    id = session['id']
    return redirect("/dashboard")
