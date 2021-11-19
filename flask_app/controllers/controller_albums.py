from flask_app import app, render_template, request, redirect, session, flash
from flask_app.models.model_album import Album
from flask_app.models.model_user import User


@app.route("/new_album")
def new_album():
    data = {
        "id": session['id']
    }
    user=User.get_one(data)
    return render_template("new_album.html", user=user)

@app.route('/process_album', methods=['POST'])
def create_album():
    
    data = {
        "name" : request.form['name'],
        "description" : request.form['description'],
        "user_id" : session['id']
    }

    if not Album.validate_albums(request.form):
        return redirect('/new_album')
        
    Album.save(data)
    return redirect("/dashboard")
    

@app.route("/album/<int:id>")
def show_album(id):
    print("Showing the User Photos from the Album")
    data = {
        "id":id
        }
    data2 = {
        "id": session['id']
    }
    album=Album.get_one(data)
    user=User.get_one(data2)
    all_photos=Album.get_album_with_photos(data)
    print(all_photos.photos[0].album_id)
    return render_template("album.html", album=album, user=user, all_photos=all_photos )

@app.route("/edit/<int:id>")
def edit(id):
    data = {"id":id}
    data2 = {
        "id": session['id']
    }
    session['album_id'] = id
    user=User.get_one(data2)
    album=Album.get_one(data)
    return render_template("edit.html", album=album, user=user)

@app.route('/update',methods=['POST'])
def update():
    album_id = session['album_id']
    if not Album.validate_album(request.form):
        return redirect(f"/edit/{album_id}")
    Album.update(request.form)
    return redirect("/dashboard")

@app.route("/destroy/<int:id>")
def destroy(id):
    data ={'id': id}
    Album.destroy(data)
    id = session['id']
    return redirect("/dashboard")

