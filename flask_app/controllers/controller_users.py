from flask_app import app, render_template, request, redirect, session, flash
from flask_app.models.model_user import User
from flask_app.models.model_album import Album
# from flask_app.models.model_photo import Photo
from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app)

@app.route('/')         
def index():
    if 'id' in session:
        return redirect('/dashboard')
    return render_template("index.html")

@app.route('/register')
def register():
    return render_template("register.html")

@app.route('/process_user', methods=['POST'])
def create_user():
    if not User.validate_user(request.form):
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    
    data = {
        "username" : request.form['username'],
        "email_address" : request.form['email_address'],
        "password" : pw_hash,
        "confirm_password" : request.form['confirm_password']
    }
        
    id= User.save(data)
    session['id'] = id
    return redirect("/dashboard")


@app.route("/dashboard")
def show_user():
    print("Showing the User Info From the Form")
    if 'id' not in session:
        return redirect('/logout')
    data = {'id': session['id']}
    print(session['id'])
    all_albums = User.get_user_with_albums(data)
    return render_template("dashboard.html", all_albums=all_albums)


@app.route("/userlogin")
def login_page():
    return render_template("login.html")

@app.route("/login", methods=['POST'])
def login():
    data = {
        "email_address" : request.form["email_address"]
    }
    user_in_db = User.get_by_email(data)
    if not user_in_db:
        flash("Invalid Email/Password")
        return redirect('/')
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash("Invalid Email/Password")
        return redirect('/')
    session['id'] = user_in_db.id
    return redirect("/dashboard")

@app.route("/logout")
def logout():
    session.clear()
    return redirect('/')
