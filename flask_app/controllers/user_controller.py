from flask_app import app
from flask import (
    redirect,
    session,
    request,
    flash,
    render_template,
)
from flask_app.models.post import Post
from flask_app.models.user import User
from flask_bcrypt import Bcrypt


bcrypt = Bcrypt(app)


@app.route("/")
def index():

    return render_template("index.html")


@app.route("/users/login", methods=["POST"])
def login():
    # session id
    #  validate login form.
    if not User.login_validator(request.form):
        flash("register email account first")
        return redirect("/")
    # see if the username provided exists in the database
    data = {"email": request.form["email"]}
    user_in_db = User.get_by_email(data)
    # user is not registered in the db
    if not user_in_db:
        flash("Invalid Email/Password")
        return redirect("/")

    if not bcrypt.check_password_hash(user_in_db.password, request.form["password"]):
        # if we get False after checking the password
        flash("Invalid Email/Password")
        return redirect("/")
    # if the passwords matched, we set the user_id into session

    #  store users id in session.
    session["users_id"] = user_in_db.id
    session["first_name"] = user_in_db.first_name
    session["full_name"] = f"{user_in_db.first_name} {user_in_db.last_name}"
    print(session)
    return redirect("/homepage")


@app.route("/logout")
def logout():

    return redirect("/")


@app.route("/users/register", methods=["post"])
def register_user():
    # session id
    #  validate register form.
    if not User.register_validator(request.form):
        return redirect("/")

    # check if user already exist.
    user = User.get_by_email(request.form)
    if user:
        flash("email already exist", "registration")
        return redirect("/")
    #  user exist hash password.
    hash = bcrypt.generate_password_hash(request.form["password"])
    user_data = {
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email": request.form["email"],
        "password": hash,
    }
    # database function
    user_id = User.save(user_data)
    #  store users id in session.
    session["user_id"] = user_id
    session["full_name"] = f"{request.form['first_name']} {request.form['last_name']}"

    print(session)
    print(request.form)
    return redirect("/homepage")
