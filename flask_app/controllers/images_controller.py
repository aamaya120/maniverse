from flask_app import app
from flask import render_template, redirect, session, request, flash, send_from_directory
from flask_app.models.image import Image
from flask_app.models.user import User
from flask_app.models.comment import Comment
from datetime import datetime
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge
import os

UPLOAD_DIRECTORY = os.path.join('flask_app', 'static', 'uploads')
if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)
app.config['UPLOAD_DIRECTORY'] = UPLOAD_DIRECTORY
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['ALLOWED_EXTENSIONS'] = ['.jpg', '.jpeg', '.png']

# CREATE NEW IMAGE FORM
@app.route('/images/create')
def images_create():
    if session['user_id']:
        current_user = User.get_one(session['user_id'])
    return render_template('image_create.html', 
                        current_user = current_user, 
                        form_data = {})

# CREATE NEW IMAGE (POST)
@app.route('/images/create', methods=['POST'])
def image_create_save():
    form_data = request.form.to_dict() 
    if Image.validate(form_data):
        form_data['user_id'] = session['user_id']
        Image.create_one(form_data)
        if session['user_id']:
            user_id = form_data['user_id']
            # current_user = User.get_one(session['user_id'])
            return redirect(f'/user/home/{user_id}') 


#EDIT IMAGE FORM
@app.route('/images/edit/<int:image_id>')
def image_edit(image_id):
    if session['user_id']:
        one_image = Image.get_one(image_id)
        formatted_date = one_image.created_at.strftime("%Y-%m-%d")
        if one_image.creator.id == session['user_id']:
            return render_template('image_edit.html', 
                    image_to_edit = one_image, 
                    current_user = User.get_one(session['user_id']),
                    formatted_date = formatted_date)
        return redirect ('/home')
    return redirect('/home')

# EDIT IMAGE (POST)
@app.route('/images/update/<int:image_id>', methods=['POST'])
def show_edit_save(image_id):
    form_data = request.form.to_dict()
    # print(form_data, "*******i made it to line 78 ******")
    if Image.validate(form_data):
        # print("*******it's valid** i made it to line 80 ****")   
        form_data['image_id'] = image_id
        # print("****  made it to line 82 ****", form_data['image_id'] )
        Image.update_one(form_data)
        # print(Image.update_one(form_data), "!!!!! made it to line 84 !!!")
        return redirect(f'/images/show_one/{image_id}')
    return redirect('/home')

# @app.route('/upload', methods=['POST'])
# def upload():
#     try:
#         file = request.files['file']
#         extension = os.path.splitext(file.filename)[1]
#         print(extension)
#         if file.filename.strip():
#             flash("Please select a file")
#         if file:

#             if extension not in app.config['ALLOWED_EXTENSIONS']:
#                 flash( 'File is not an image' )

#             file.save(os.path.join(
#                 app.config['UPLOAD_DIRECTORY'],
#                 secure_filename(file.filename)))
#     except RequestEntityTooLarge:
#         return 'File is larger than the 16MB limit.'
#     return redirect('/home')

# @app.route('/serve-image/<filename>', methods=['GET'])
# def serve_image(filename):
#     return send_from_directory(app.config['UPLOAD_DIRECTORY'], filename)


@app.route('/upload', methods=['POST'])
def upload():
    try:
        file = request.files['file']
        extension = os.path.splitext(file.filename)[1]
        print(extension)
        if file.filename.strip():
            flash("Please select a file")
        if file:
            
            if extension not in app.config['ALLOWED_EXTENSIONS']:
                flash( 'File is not an image' )

            file.save(os.path.join(
                app.config['UPLOAD_DIRECTORY'],
                secure_filename(file.filename)))
        Image.add_image(secure_filename(file.filename), 
                            request.form['user_id'], request.form['image_id'])    
    except RequestEntityTooLarge:
        return 'File is larger than the 16MB limit.'
    return redirect('/home')

@app.route('/serve-image/<filename>', methods=['GET'])
def serve_image(filename):
    return send_from_directory(app.config['UPLOAD_DIRECTORY'], filename)






# DELETE IMAGE W VALIDATIONS
@app.route('/images/delete/<int:image_id>')
def image_delete(image_id):
    if session['user_id']:
        data = {'image_id': image_id}
        if session['user_id'] == Image.get_one(image_id).creator.id:
            Image.delete_image(data)
        return redirect('/home')
    return redirect('/')

#SHOW ONE IMAGE
@app.route('/images/show_one/<int:image_id>')
def show_one(image_id):
    one_image = Image.get_one(image_id)
    one_comment = Comment.get_one_comment_by_creator_id({'image_id':image_id})
    this_image_comments = Comment.get_all_comments_by_image_id({"image_id": image_id})
    # for one_date in one_comment:
    #     formatted_date = one_date.created_at.strftime("%b %d, %Y")
    print(this_image_comments,'%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
    print(one_image)
    if session['user_id']:
        current_user = User.get_one(session['user_id'])
    return render_template('image_show_one.html', one_image = one_image, 
                    current_user = current_user,
                    one_comment = one_comment,
                    this_image_comments = this_image_comments)
                    # formatted_date = formatted_date)
                    
