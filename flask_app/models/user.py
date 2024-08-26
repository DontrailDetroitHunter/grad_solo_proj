from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re

# import other class here from flask_app.model. use the lower case

EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$")


# model the class after the nextfix table from our database
class User:
    my_db = "sports_lounge_schema.users"

    def __init__(self, data):
        self.id = data["id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.email = data["email"]
        self.password = data["password"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.recipes = None

    @classmethod
    def save(cls, data):
        query = """

        INSERT INTO users
        (first_name,last_name,email,password)
        VALUES (%(first_name)s,%(last_name)s,%(email)s,%(password)s);

        """
        # this line returns the id of the new user.
        return connectToMySQL(User.my_db).query_db(query, data)

    # login in class info, not registration
    @classmethod
    def get_by_email(cls, data):
        query = """
        SELECT *
        FROM users
        WHERE email = %(email)s;
        """
        results = connectToMySQL(User.my_db).query_db(query, data)
        print(results)
        # if results is empty return none
        if len(results) == 0:
            return None

        # if results are not empty return a  user object.

        user = User(results[0])
        return user

    @classmethod
    def get_all(cls, data):
        query = """
        SELECT *
        FROM users
         (first_name,last_name,email,password)
        VALUES (%(first_name)s,%(last_name)s,%(email)s,%(password)s);

        """
        return connectToMySQL(User.my_db).query_db(query, data)

    @classmethod
    def get_by_id(cls, data):
        query = """
        SELECT *
        FROM users
        WHERE id = %(user_id)s;
        """
        results = connectToMySQL(User.my_db).query_db(query, data)
        print(results)
        # if results is empty return none
        if len(results) == 0:
            return None

        # if results are not empty return a  user object.

        user = User(results[0])
        return user

    # code Validation! write for loop in html for this validation.
    @staticmethod
    def register_validator(form_data):
        is_valid = True
        #  First name validation
        if len(form_data["first_name"].strip()) == 0:
            is_valid = False
            flash("First Name required for registration", "registration")
        elif len(form_data["first_name"]) < 2:
            is_valid = False
            flash("2 character min", "registration")

        #  Last name validation
        if len(form_data["last_name"].strip()) == 0:
            is_valid = False
            flash("Last Name required for registration", "registration")
        elif len(form_data["last_name"]) < 2:
            is_valid = False
            flash("2 character min", "registration")

        # email name validation
        if len(form_data["email"].strip()) == 0:
            is_valid = False
            flash("Email required for registration", "registration")
        elif not EMAIL_REGEX.match(form_data["email"]):
            is_valid = False
            flash("invalid email", "registration")

        # password validation
        if len(form_data["password"].strip()) == 0:
            is_valid = False
            flash("Password required for registration", "registration")
        elif len(form_data["password"]) < 8:
            is_valid = False
            flash("8 character min", "registration")
        elif form_data["password"] != form_data["confirm_pw"]:
            is_valid = False
            flash("passwords must match, to register", "registration")

        return is_valid

    @staticmethod
    def login_validator(form_data):
        is_valid = True
        # email name validation
        if len(form_data["email"].strip()) == 0:
            is_valid = False
            flash("Existing email required for login", "login")
        elif not EMAIL_REGEX.match(form_data["email"]):
            is_valid = False
            flash("invalid email", "login")

        # password validation
        if len(form_data["password"].strip()) == 0:
            is_valid = False
            flash(" Existing password required for valid login", "login")
        elif len(form_data["password"]) < 8:
            is_valid = False
            flash("8 character min", "login")
        return is_valid
