from flask_app import app
from flask import render_template, redirect, session, request, flash
from flask_app.models.image import Image
from flask_app.models.user import User
from flask_app.models.comment import Comment
from datetime import datetime



# @app.route('/image/comment/create/<int:image_id>', methods=['POST'])        
# def comment_create(image_id):
#     print(request.form)
#     if session['user_id']:
#         current_user = User.get_one(session['user_id'])
#         if Comment.validate(request.form):
#             data = request.form.to_dict()
#             data['creator_id'] = session['user_id']
#             data['image_id'] = image_id
#             Comment.create_one(data)
#     return redirect(f"""/images/show_one/{image_id}""", 
#                         current_user = current_user)


@app.route('/image/comment/create/<int:image_id>', methods=['POST'])        
def comment_create(image_id):
    print(request.form)
    if session['user_id']:
        current_user = User.get_one(session['user_id'])
        if Comment.validate(request.form):
            data = request.form.to_dict()
            data['creator_id'] = session['user_id']
            data['image_id'] = image_id
            Comment.create_one(data)
    return redirect(f"""/images/show_one/{image_id}""")
