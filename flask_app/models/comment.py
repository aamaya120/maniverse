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


    # VALIDATIONS FOR ADDING POST
    @staticmethod
    def validate(request):
        is_valid = True
        if not request['content'].strip():
            is_valid = False
            flash("Please type a comment", "post")
        return is_valid

    #CREATE IMAGE/COMMENT
    @classmethod
    def create_one(cls, data):
        query = """
        INSERT INTO comments 
        (content, image_id, user_id) 
        VALUES (%(content)s, %(image_id)s, %(user_id)s)
        """
        comment_content = connect(cls.db).query_db(query, data)
        print(f"""returned CONTENT from query: {comment_content}""")
        return comment_content


    #GET ALL POSTS BY IMAGE_ID
    @classmethod
    def get_all_posts_by_image_id(cls, data):
        query = """
            SELECT * FROM comments
            JOIN users ON comments.creator_id = users.id
            WHERE comments.image_id = %(image_id)s;
            """
        results = connect(cls.db).query_db(query, data)
        print(results)
        all_comments = []
        for dict in results: #Makes a dictionary out of the query results
            this_comment = cls(dict)  #Creates a post object
            print(this_comment)
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
            print(this_comment.user.first_name, this_comment.content)
            all_comments.append(this_comment)  #Put the post object into the all_posts list
        return all_comments
    




