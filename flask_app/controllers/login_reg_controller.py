from flask_app import app
from flask import render_template, redirect, session, request, flash
from flask_app.models.user import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


# INDEX/HOME PAGE -- REGISTER AND LOGIN PAGE
@app.route('/')
def index():
    return render_template('index.html')

# REGISTER USER (POST)
@app.route('/user/create', methods=['POST'])
def create_validate():
    if User.validate(request.form):
        pw_hash = bcrypt.generate_password_hash(request.form['password'])
        data = {
            "first_name" : request.form['first_name'],
            "last_name" : request.form['last_name'],
            "username" : request.form['username'],
            "email" : request.form['email'],
            "password" : pw_hash
            }
        user_id = User.create_one(data)
        session['user_id'] = user_id
        return redirect('/home')
    return redirect('/')



# LOGIN (POST)
@app.route('/users/login', methods=['POST'])
def login_user():
    user_in_db = User.get_by_email({'user_email' : request.form['email']})
    if user_in_db:
        if bcrypt.check_password_hash(user_in_db.password, request.form['password']):
            session['user_id'] = user_in_db.id
            return redirect('/home')
    flash("Invalid Credentials", "log")
    return redirect('/')


# LOGOUT
@app.route('/user/logout')
def logout():
    session.clear()
    return redirect('/')
