from flask_app.config.mysqlconnection import connect
from flask_app.models import user
from flask import flash, request
import datetime


class Image:
    db = "maniverse"
    def __init__( self , data ):
        self.id = data['id']
        self.image = data['image']
        self.caption = data['caption']
        self.user_id = data['user_id']
        self.brand = data['brand']
        self.brand2 = data['brand2']
        self.color = data['color']
        self.color2 = data['color2']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

        self.creator = None


    # VALIDATIONS FOR ADDING IMAGE
    @staticmethod
    def validate(request):
        is_valid = True
        if not request['image'].strip():
            is_valid = False
            flash("Image Required", "image")
        elif len(request['image']) < 3:
            is_valid = False
            flash("Title Must Be Longer", "image")

        if not request['caption'].strip():
            is_valid = False
            flash("Caption Field Cannot Be Blank", "image")
        elif len(request['caption']) < 3:
            is_valid = False
            flash("Caption Must Be Longer", "image")

        return is_valid


    # GET ALL IMAGES BY USER
    @classmethod
    def get_all_images_by_user(cls, data):
        query = """
            SELECT * 
            FROM images
            JOIN users 
            ON images.user_id = users.id
            WHERE users.id = %(user_id)s
            ORDER BY images.created_at DESC
            """
        results = connect(cls.db).query_db(query, data)
        all_images = []
        for dict in results: #Makes a dictionary out of the query results
            this_image = cls(dict)  #Creates an image object
            user_data = {
                "id": dict['users.id'],
                "first_name": dict['first_name'],
                "last_name": dict['last_name'],
                "username": dict['username'],
                "email": dict['email'],
                "password": dict['password'],
                "created_at": dict['users.created_at'],
                "updated_at": dict['users.updated_at']
                }
            this_creator = user.User(user_data)  #Create a User object
            this_image.creator = this_creator #set creator attribute to this_creator User object
            all_images.append(this_image)  #Put the recipe object into the all_recipes list
        print("all_images---------------------*****", all_images)
        return all_images
    
    # GET ALL IMAGES BY USER
    @classmethod
    def get_all_images_by_all_users(cls):
        query = """
            SELECT * 
            FROM images
            JOIN users 
            ON images.user_id = users.id
            ORDER BY images.created_at DESC
            """
        results = connect(cls.db).query_db(query)
        all_images = []
        for dict in results: #Makes a dictionary out of the query results
            this_image = cls(dict)  #Creates an image object
            user_data = {
                "id": dict['users.id'],
                "first_name": dict['first_name'],
                "last_name": dict['last_name'],
                "username": dict['username'],
                "email": dict['email'],
                "password": dict['password'],
                "created_at": dict['users.created_at'],
                "updated_at": dict['users.updated_at']
                }
            this_creator = user.User(user_data)  #Create a User object
            this_image.creator = this_creator #set creator attribute to this_creator User object
            all_images.append(this_image)  #Put the recipe object into the all_recipes list
        print("all_images---------------------*****", all_images)
        return all_images



    
    #CREATE IMAGE
    @classmethod
    def create_one(cls, data):
        query = """
        INSERT INTO images 
        (image, caption, brand, brand2, color, color2, user_id) 
        VALUES (%(image)s, %(caption)s, %(brand)s, %(brand2)s, %(color)s, %(color2)s, %(user_id)s);
        """
        image_id = connect(cls.db).query_db(query, data)
        print(f"""returned IMAGE ID from query: {image_id}""")
        return image_id
    
        # DELETE IMAGE
    @classmethod
    def delete_image(cls, data):
        query = """
            DELETE FROM images 
            WHERE id = %(image_id)s;
            """
        connect(cls.db).query_db(query, data)






    # EDIT IMAGE 
    @classmethod
    def update_one(cls, data):
        query = """
            UPDATE images
            SET image = %(image)s, caption = %(caption)s, brand = %(brand)s, brand2 = %(brand2)s, color = %(color)s, color2 = %(color2)s
            WHERE id = %(image_id)s;
            """
        connect(cls.db).query_db(query, data)


    # SHOW ONE IMAGE JOIN USER
    @classmethod
    def get_one(cls, image_id):
        query = """
            SELECT * FROM images
            JOIN users
            ON images.user_id = users.id
            WHERE images.id = %(image_id)s
            """
        data = {"image_id": image_id}
        result = connect(cls.db).query_db(query, data)
        this_image = cls(result[0])
        user_data = {
            "id": result[0]['users.id'],
            "first_name": result[0]['first_name'],
            "last_name": result[0]['last_name'],
            "username": result[0]['username'],
            "email": result[0]['email'],
            "password": None,
            "created_at": result[0]['users.created_at'],
            "updated_at": result[0]['users.updated_at']
            }
        this_image.creator = user.User(user_data)
        return this_image
    

    # CREATE AN IMAGE / INSERT TO DB
    @classmethod
    def add_image(cls, data):
        image_data = {
            "id": id,
            "user_id": user_id,
            "content": content
        }
        query = """
        INSERT INTO images(id, user_id, content)
        VALUES (%(id)s, %(user_id)s, %(content)s)
        """
        print(query)
        results = connect(cls.db).query_db(query, image_data)
        print(results)
        return results


