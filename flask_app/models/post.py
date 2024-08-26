from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
from flask_bcrypt import Bcrypt
from flask_app.models.user import User

EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$")

# import the function that will return an instance of a connection


# model the class after the posts table from our database
class Post:

    # model the class after the posts table from our database

    my_db = "sports_lounge_schema.posts"

    def __init__(self, data):
        self.id = data["id"]
        self.post = data["post"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.users_id = data["users_id"]
        self.tv_critic = []

    @classmethod
    def create(cls, data):
        query = """
        INSERT INTO posts
        (post,users_id)
        VALUES (%(post)s,%(user_id)s);

        """
        # data = data.copy()
        # data["user_id"] = session["user_id"]

        # this line returns the id of the new user.
        return connectToMySQL("sports_lounge_schema").query_db(query, data)

    @classmethod
    def get_all(cls):
        query = """
        SELECT *
        FROM posts
        JOIN users
        ON users.id = posts.users_id;

        """

        # (post,network,release_date,,user_id);
        # VALUES (%(post)s,%(network)s,%(release_date)s,%(user_id)s);
        results = connectToMySQL(Post.my_db).query_db(query)
        all_post = []
        for dict in results:
            posts = cls(dict)
            user_data = {
                "id": dict["users_id"],
                "first_name": dict["first_name"],
                "last_name": dict["last_name"],
                "email": dict["email"],
                "password": dict["password"],
                "created_at": dict["created_at"],
                "updated_at": dict["updated_at"],
            }

            user_obj = User(user_data)
            posts.users = user_obj
            all_post.append(posts)
            # debugging print query
            # print("query results:", results)
        return all_post

    @classmethod
    def join_tables_for_one_id(cls, post_id):
        query = """
        SELECT *
        FROM posts
        JOIN users
        ON users.id = posts.users_id
        WHERE posts.id=%(id)s;
        """
        data = {"id": post_id}
        results = connectToMySQL(Post.my_db).query_db(query, data)
        single_post = cls(results[0])
        for dict in results:
            user_data = {
                "id": dict["users.id"],
                "first_name": dict["first_name"],
                "last_name": dict["last_name"],
                "email": dict["email"],
                "password": None,
                "created_at": dict["users.created_at"],
                "updated_at": dict["users.updated_at"],
            }
            publisher = User(user_data)
            single_post.chef = publisher
        return single_post

    @classmethod
    def get_by_id(cls, data_id):
        query = """
        SELECT *
        FROM posts
        WHERE id = %(post_id)s;
        """
        data = {"post_id": data_id}
        results = connectToMySQL(Post.my_db).query_db(query, data)
        print(results)
        # if results is empty return none
        if len(results) == 0:
            return None
        return cls(results[0])

    @classmethod
    def update(cls, post_data):
        query = """
        UPDATE posts
        SET 
        post=%(post)s
        WHERE id =%(post_id)s;
        """

        posts = connectToMySQL(Post.my_db).query_db(query, post_data)
        print(posts)
        return posts

    @classmethod
    def delete(cls, post_id):
        query = """
        DELETE FROM posts
        WHERE id = %(id)s;
        """
        data = {"id": post_id}
        connectToMySQL(Post.my_db).query_db(query, data)

    @staticmethod
    def is_valid(form_data):
        is_valid = True
        # presence validation aka. make sure they type something.
        if len(form_data["post"].strip()) == 0:
            is_valid = False
            flash("post Required", "post")
        elif len(form_data["post"]) < 2:
            is_valid = False
            flash("2 Character min", "post")
            # network validation
        # if len(form_data["network"].strip()) == 0:
        #     is_valid = False
        #     flash("network name Required", "network")
        # elif len(form_data["network"]) < 2:
        #     is_valid = False
        #     flash("2 Character min for Network name", "network")
        #     # release_date validation
        # if len(form_data["release_date"].strip()) == 0:
        #     is_valid = False
        #     flash("release_date Required", "release_date")
        # elif len(form_data["release_date"]) < 2:
        #     is_valid = False
        #     flash("Need Date 2 char min!", "release_date")
        #     # date validation

        # if form_data.get("network") is None:
        #     is_valid = False
        #     flash("comments! Required", "comments")

        print(is_valid)
        return is_valid
