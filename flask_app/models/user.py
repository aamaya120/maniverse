from flask_app.config.mysqlconnection import connect
from flask_app.models import image
from flask import flash
import datetime
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9.+_-]+\.[a-zA-Z]+$')


class User:
    db = "maniverse"
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.username = data['username']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

        self.all_images = []

    # VALIDATIONS FOR USER REG
    @staticmethod
    def validate(request):
        is_valid = True
        
        if not request['first_name'].strip():
            is_valid = False
            flash("First Name Required", "reg")
        elif len(request['first_name']) < 2:
            is_valid = False
            flash("First Name Must Be Longer", "reg")

        if not request['last_name'].strip():
            is_valid = False
            flash("Last Name Required", "reg")
        elif len(request['first_name']) < 2:
            is_valid = False
            flash("Last Name Must Be Longer", "reg")
        
        if not request['username'].strip():
            is_valid = False
            flash("Username Required", "reg")
        elif len(request['username']) < 4:
            flash('Username needs to be min 3 characters', "reg")

        if User.get_by_username({'username': request['username']}):
            is_valid = False
            flash("Username taken.  Choose a different Username.", "reg")

        if not request['email'].strip():
            is_valid = False
            flash("Email Required", "reg")   
        elif not EMAIL_REGEX.match(request['email']):
            is_valid = False
            flash("Email is not valid!", "reg")
        
        if User.get_by_email({'user_email': request['email']}):
            is_valid = False
            flash("Email Address is Already In Use", "reg")

        if not request['password'].strip():
            is_valid = False
            flash("Password Required", "reg")
        elif len(request['password']) < 8:
            is_valid = False
            flash("Password Must Be 8 Characters", "reg")
        elif not re.search(r'\d', request['password']) or not re.search(r'[A-Z]', request['password']):
            is_valid = False
            flash('Password must contain at least one number and one uppercase letter', 'reg')
        elif request['password'] != request['password_confirm']:
            is_valid = False
            flash("Passwords Must Match", "reg")
        return is_valid

    # GET BY EMAIL
    @classmethod
    def get_by_email(cls, data):
        query = """
        SELECT * FROM users 
        WHERE email = %(user_email)s;
        """
        result = connect(cls.db).query_db(query,data)
        # print(result, len(result))
        if len(result) < 1:
            return False
        return cls(result[0])
    
    # GET BY USERNAME
    @classmethod
    def get_by_username(cls, data):
        query = """
        SELECT * FROM users
        WHERE username = %(username)s;
        """
        result = connect(cls.db).query_db(query, data)
        print(result)
        if len(result) < 1:
            return False
        return cls(result[0])


    #CREATE USER 
    @classmethod
    def create_one(cls, data):
        query = """
        INSERT INTO users 
        (first_name, last_name, username, email, password) 
        VALUES (%(first_name)s, %(last_name)s, %(username)s, %(email)s, %(password)s);
        """
        user_id = connect(cls.db).query_db(query, data)
        return user_id


    # SHOW ONE USER
    @classmethod
    def get_one(cls, user_id):
        query = """
            SELECT * FROM users
            WHERE id = %(user_id)s
            """
        data = {'user_id' : user_id}
        results = connect(cls.db).query_db(query, data) 
        print(results)
        if results:
            return cls(results[0])
        return None

    #SHOW ALL USERS
    @classmethod
    def get_all(cls):
        query = """
            SELECT * 
            FROM users
            """
        results = connect(cls.db).query_db(query)
        all_users = []
        for one_user in results:
            all_users.append(cls(one_user))
        return all_users
    

    #SHOW ONE JOIN IMAGE
    @classmethod
    def get_one_join_images(cls, data):
        query = """
            SELECT *
            FROM users
            JOIN images
            ON users.id = images.user_id
            WHERE users.id = %(user_id)s
            """
        results = connect(cls.db).query_db(query, data)
        print(results)
        this_user = cls(results[0])
        print(this_user)
        for image in results:
            image_data = {
            "id": image['images.id'],
            "image": image['image'],
            "caption": image['caption'],
            "user_id": image['user_id'],
            "brand": image['brand'],
            "brand2": image['brand2'],
            "color": image['color'],
            "color2": image['color2'],
            "created_at": image['images.created_at'],
            "updated_at": image['images.updated_at'],
            }
            this_image = image.Image(image_data)
            print(this_image, "----*************---------this_image----------")
            this_user.all_images.append(this_image)
        return this_user

    # #SHOW ALL IMAGES JOIN USER
    # @classmethod
    # def get_all_images_join_user(cls, data):
    #     query = """
    #         SELECT *
    #         FROM images
    #         JOIN users
    #         ON users.id = images.user_id
    #         WHERE users.id = %(user_id)s
    #         """
    #     results = connect(cls.db).query_db(query, data)
    #     this_image = image.Image(results[0])
    #     print(this_image)
    #     for user_dict in results:
    #         user_data = {
    #             self.id = data['id']
    #         self.first_name = data['first_name']
    #         self.last_name = data['last_name']
    #         self.username = data['username']
    #         self.email = data['email']
    #         self.password = data['password']
    #         self.created_at = data['created_at']
    #         self.updated_at = data['updated_at']
    #         "id": image_dict['images.id'],
    #         "image": image_dict['image'],
    #         "caption": image_dict['caption'],
    #         "user_id": image_dict['user_id'],
    #         "created_at": image_dict['images.created_at'],
    #         "updated_at": image_dict['images.updated_at'],
    #         }
    #         this_image = image.Image(image_data)
    #         print(this_image)
    #         this_user.all_images.append(this_image)
    #     return this_user
