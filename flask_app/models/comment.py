from flask_app.config.mysqlconnection import connect
from flask_app.models import user
from flask_app.models import image
from flask import flash, request


class Comment:
    db = "maniverse"
    def __init__( self , data ):
        self.id = data['id']
        self.content = data['content']
        self.creator_id = data['creator_id']
        self.image_id = data['image_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.image = None
        self.user = None


    # VALIDATIONS FOR ADDING POST
    @staticmethod
    def validate(request):
        is_valid = True
        if not request['content'].strip():
            is_valid = False
            flash("Please type a comment", "comment")
        return is_valid

    #CREATE COMMENT FOR IMAGE
    @classmethod
    def create_one(cls, data):
        query = """
        INSERT INTO comments 
        (content, image_id, creator_id) 
        VALUES (%(content)s, %(image_id)s, %(creator_id)s)
        """
        comment_content = connect(cls.db).query_db(query, data)
        print(f"""returned CONTENT from query: {comment_content}""")
        # print(comment_content)
        return comment_content


    
        #GET ALL COMMENTS BY IMAGE_ID
    @classmethod
    def get_all_comments_by_image_id(cls, data):
        query = """
            SELECT * 
            FROM comments
            JOIN images
            ON comments.image_id = images.id
            WHERE comments.image_id = %(image_id)s
            ORDER BY comments.created_at DESC;
            """
        results = connect(cls.db).query_db(query, data)
        print(results, 'results-----results------results-----results')
        all_comments = []
        for image_dict in results: #Makes a dictionary out of the query results
            this_comment = cls(dict)  #Creates a comment object
            print(this_comment, 'thiscomment ------ thiscomment --------this comment ----')
            image_data = {
                "id": image_dict['images.id'],
                "image": image_dict['image'],
                "caption": image_dict['caption'],
                "user_id": image_dict['user_id'],
                "brand": image_dict['brand'],
                "brand2": image_dict['brand2'],
                "color": image_dict['color'],
                "color2": image_dict['color2'],
                "created_at": image_dict['images.created_at'],
                "updated_at": image_dict['images.updated_at'],
            }
            this_image = image.Image(image_data)  #Create a Image object
            this_comment.image = this_image #set show attribute to this_image Image object
            print(this_comment.image, this_comment.content)
            all_comments.append(this_comment)  #Put the comment object into the all_comments list
        return all_comments
    




# GET ONE COMMENT BY USER_ID
    @classmethod
    def get_one_comment_by_creator_id(cls, data):
        query = """
            SELECT * 
            FROM comments
            JOIN users 
            ON comments.creator_id = users.id
            WHERE comments.image_id = %(image_id)s;
            """
        result = connect(cls.db).query_db(query, data)
        print(result, "this is the result from get one comment by creator id")
        all_comments = []
        for dict in result: #Makes a dictionary out of the query results
            this_comment = cls(dict)  #Creates a comment object
            print(this_comment, "this is this_comment from get one comment by creator id")
            user_data = {
                "id" : dict['id'],
                "first_name" : dict['first_name'],
                "last_name" :dict['last_name'],
                "email" : dict['email'],
                "username" : dict['username'],
                "password" : dict['password'],
                "created_at" : dict['users.created_at'],
                "updated_at" : dict['users.updated_at']
                }
            this_user = user.User(user_data)  #Create a User object
            this_comment.user = this_user #set show attribute to this_show Show object
            print(this_comment.user.first_name, this_comment.content,"***************")
            all_comments.append(this_comment)  #Put the comment object into the all_comments list
        return all_comments
    











    # # GET ALL COMMENTS BY USER_ID
    # @classmethod
    # def get_all_comments_by_creator_id(cls, data):
    #     query = """
    #         SELECT * FROM comments
    #         JOIN users ON comments.creator_id = users.id
    #         WHERE comments.image_id = %(image_id)s;
    #         """
    #     results = connect(cls.db).query_db(query, data)
    #     print(results)
    #     all_comments = []
    #     for dict in results: #Makes a dictionary out of the query results
    #         this_comment = cls(dict)  #Creates a comment object
    #         print(this_comment)
    #         user_data = {
    #             "id" : dict['id'],
    #             "first_name" : dict['first_name'],
    #             "last_name" :dict['last_name'],
    #             "email" : dict['email'],
    #             "username" : dict['username'],
    #             "password" : dict['password'],
    #             "created_at" : dict['users.created_at'],
    #             "updated_at" : dict['users.updated_at']
    #             }
    #         this_user = user.User(user_data)  #Create a User object
    #         this_comment.user = this_user #set show attribute to this_show Show object
    #         print(this_comment.user.first_name, this_comment.content)
    #         all_comments.append(this_comment)  #Put the comment object into the all_comments list
    #     return all_comments



