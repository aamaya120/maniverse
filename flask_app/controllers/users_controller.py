from flask_app import app
from flask import render_template, redirect, session, request, flash
from flask_app.models.user import User
from flask_app.models.image import Image
from flask_bcrypt import Bcrypt
import os
bcrypt = Bcrypt(app)


# DASHBOARD
# @app.route('/home')
# def dashboard():
#     if session['user_id']:
#         all_images= Image.get_all_images_by_user()
#         current_user = User.get_one(session['user_id'])
#         return render_template('dashboard.html', 
#                 all_images = all_images,
#                 current_user = current_user)
#     return redirect('/')


#DASHBOARD / HOME PAGE
@app.route('/home')
def dashboard():
    if session['user_id']:
        current_user = User.get_one(session['user_id'])
        all_images= Image.get_all_images_by_all_users()
        files = os.listdir(app.config['UPLOAD_DIRECTORY'])
        images = []
        for file in files:
            extension = os.path.splitext(file)[1].lower()
            if extension in app.config['ALLOWED_EXTENSIONS']:
                images.append(file)
                print(images)
    
        return render_template('dashboard.html', 
                all_images = all_images,
                current_user = current_user,
                images = images)
    else:
        flash("You need to be signed in to view page")           
        return redirect('/')
    # return redirect('/')

#CREATE USER FORM
@app.route('/create')
def create_user():
    return render_template('create.html')

#CREATE USER 
@app.route('/create', methods=['POST'])
def create():
    id = User.save_create(request.form)
    print(id)
    return redirect(f'/read_one/{id}')


#SHOW ALL IMAGES OF USER
@app.route('/users/show_all_images/<int:user_id>')
def show_all_images(user_id):
    if session['user_id']:
        current_user = User.get_one(session['user_id'])
        all_images= Image.get_all_images_by_user({'user_id':user_id})
        # image_creator = User.get_all_images_join_user(user_id)
        return render_template('user_show_all_images.html', 
                all_images = all_images, 
                current_user = current_user)
                # image_creator = image_creator)


#SHOW ALL IMAGES OF CURRENT USER / USER HOME
@app.route('/user/home/<int:user_id>')
def user_home(user_id):
    if session['user_id']:
        current_user = User.get_one(session['user_id'])
        this_user = Image.get_all_images_by_user({'user_id':user_id})
    return render_template('user_mypage.html', 
                        current_user = current_user,
                        this_user = this_user)




#EDIT USER FORM
@app.route('/users/edit/<int:user_id>')
def user_edit(user_id):
    one_user = User.get_one(user_id)
    return render_template('edit.html', one_user = one_user)

# EDIT USER 
@app.route('/users/edit/<int:user_id>', methods=['POST'])
def update_user(user_id):
    one_user = {
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "username": request.form['username'],
        "email": request.form["email"],
        "id": user_id
    }
    User.update(one_user)
    return redirect(f'/read_one/{user_id}')


#SHOW ONE USER
@app.route('/user/show_one/<int:user_id>')
def read_one(user_id):
    one_user = User.get_one(user_id)
    current_user = User.get_one(session['user_id'])
    return render_template('user_show_one.html', one_user = one_user, current_user = current_user)


# #SHOW ONE USER
# @app.route('/user/show_one/<int:user_id>')
# def read_one(user_id):
#     one_user = User.get_one(user_id)
#     current_user = User.get_one(session['user_id'])
#     return render_template('user_show_one.html', one_user = one_user, current_user = current_user)

#SHOW ALL USERS
@app.route("/user/show_all")
def read_all():
    all_users = User.get_all()
    print(all_users)
    return render_template("user_show_all.html", all_users = all_users) 



# DELETE USER (without verifiction)
@app.route('/users_delete/<int:user_id>')
def delete_user(user_id):
    User.delete(user_id)
    return redirect('/read_all')
