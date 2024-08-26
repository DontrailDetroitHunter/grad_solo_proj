from flask_app import app
from flask import (
    redirect,
    session,
    request,
    flash,
    render_template,
    url_for,
    jsonify,
    json,
    Request,
)
import numpy
from flask_app.models.post import Post
from flask_app.models.user import User
import os
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv

nfl_teams_info = [
    {
        "team_id": 1,
        "team_name": "Cardinals",
        "team_location": "Arizona",
        "team_abbreviation": "ARI",
        "team_stadium": "State Farm Stadium",
    },
    {
        "team_id": 2,
        "team_name": "Falcons",
        "team_location": "Atlanta",
        "team_abbreviation": "ATL",
        "team_stadium": "Mercedes-Benz Stadium",
    },
    {
        "team_id": 3,
        "team_name": "Ravens",
        "team_location": "Baltimore",
        "team_abbreviation": "BAL",
        "team_stadium": "M&T Bank Stadium",
    },
    {
        "team_id": 4,
        "team_name": "Bills",
        "team_location": "Buffalo",
        "team_abbreviation": "BUF",
        "team_stadium": "Highmark Stadium",
    },
    {
        "team_id": 5,
        "team_name": "Panthers",
        "team_location": "Carolina",
        "team_abbreviation": "CAR",
        "team_stadium": "Bank of America Stadium",
    },
    {
        "team_id": 6,
        "team_name": "Bears",
        "team_location": "Chicago",
        "team_abbreviation": "CHI",
        "team_stadium": "Soldier Field",
    },
    {
        "team_id": 7,
        "team_name": "Bengals",
        "team_location": "Cincinnati",
        "team_abbreviation": "CIN",
        "team_stadium": "Paul Brown Stadium",
    },
    {
        "team_id": 8,
        "team_name": "Browns",
        "team_location": "Cleveland",
        "team_abbreviation": "CLE",
        "team_stadium": "FirstEnergy Stadium",
    },
    {
        "team_id": 9,
        "team_name": "Cowboys",
        "team_location": "Dallas",
        "team_abbreviation": "DAL",
        "team_stadium": "AT&T Stadium",
    },
    {
        "team_id": 10,
        "team_name": "Broncos",
        "team_location": "Denver",
        "team_abbreviation": "DEN",
        "team_stadium": "Empower Field at Mile High",
    },
    {
        "team_id": 11,
        "team_name": "Lions",
        "team_location": "Detroit",
        "team_abbreviation": "DET",
        "team_stadium": "Ford Field",
    },
    {
        "team_id": 12,
        "team_name": "Packers",
        "team_location": "Green Bay",
        "team_abbreviation": "GB",
        "team_stadium": "Lambeau Field",
    },
    {
        "team_id": 13,
        "team_name": "Texans",
        "team_location": "Houston",
        "team_abbreviation": "HOU",
        "team_stadium": "NRG Stadium",
    },
    {
        "team_id": 14,
        "team_name": "Colts",
        "team_location": "Indianapolis",
        "team_abbreviation": "IND",
        "team_stadium": "Lucas Oil Stadium",
    },
    {
        "team_id": 15,
        "team_name": "Jaguars",
        "team_location": "Jacksonville",
        "team_abbreviation": "JAX",
        "team_stadium": "TIAA Bank Field",
    },
    {
        "team_id": 16,
        "team_name": "Chiefs",
        "team_location": "Kansas City",
        "team_abbreviation": "KC",
        "team_stadium": "GEHA Field at Arrowhead Stadium",
    },
    {
        "team_id": 17,
        "team_name": "Raiders",
        "team_location": "Las Vegas",
        "team_abbreviation": "LV",
        "team_stadium": "Allegiant Stadium",
    },
    {
        "team_id": 18,
        "team_name": "Chargers",
        "team_location": "Los Angeles",
        "team_abbreviation": "LAC",
        "team_stadium": "SoFi Stadium",
    },
    {
        "team_id": 19,
        "team_name": "Rams",
        "team_location": "Los Angeles",
        "team_abbreviation": "LA",
        "team_stadium": "SoFi Stadium",
    },
    {
        "team_id": 20,
        "team_name": "Dolphins",
        "team_location": "Miami",
        "team_abbreviation": "MIA",
        "team_stadium": "Hard Rock Stadium",
    },
    {
        "team_id": 21,
        "team_name": "Vikings",
        "team_location": "Minnesota",
        "team_abbreviation": "MIN",
        "team_stadium": "U.S. Bank Stadium",
    },
    {
        "team_id": 22,
        "team_name": "Patriots",
        "team_location": "New England",
        "team_abbreviation": "NE",
        "team_stadium": "Gillette Stadium",
    },
    {
        "team_id": 23,
        "team_name": "Saints",
        "team_location": "New Orleans",
        "team_abbreviation": "NO",
        "team_stadium": "Caesars Superdome",
    },
    {
        "team_id": 24,
        "team_name": "Giants",
        "team_location": "New York",
        "team_abbreviation": "NYG",
        "team_stadium": "MetLife Stadium",
    },
    {
        "team_id": 25,
        "team_name": "Jets",
        "team_location": "New York",
        "team_abbreviation": "NYJ",
        "team_stadium": "MetLife Stadium",
    },
    {
        "team_id": 26,
        "team_name": "Eagles",
        "team_location": "Philadelphia",
        "team_abbreviation": "PHI",
        "team_stadium": "Lincoln Financial Field",
    },
    {
        "team_id": 27,
        "team_name": "Steelers",
        "team_location": "Pittsburgh",
        "team_abbreviation": "PIT",
        "team_stadium": "Heinz Field",
    },
    {
        "team_id": 28,
        "team_name": "49ers",
        "team_location": "San Francisco",
        "team_abbreviation": "SF",
        "team_stadium": "Levi's Stadium",
    },
    {
        "team_id": 29,
        "team_name": "Seahawks",
        "team_location": "Seattle",
        "team_abbreviation": "SEA",
        "team_stadium": "Lumen Field",
    },
    {
        "team_id": 30,
        "team_name": "Buccaneers",
        "team_location": "Tampa Bay",
        "team_abbreviation": "TB",
        "team_stadium": "Raymond James Stadium",
    },
    {
        "team_id": 31,
        "team_name": "Titans",
        "team_location": "Tennessee",
        "team_abbreviation": "TEN",
        "team_stadium": "Nissan Stadium",
    },
    {
        "team_id": 32,
        "team_name": "Commanders",
        "team_location": "Washington",
        "team_abbreviation": "WAS",
        "team_stadium": "FedExField",
    },
]


#
# def all_sports():
#     url = f"{base_url}/homepage/"{name}
#     response = request.get_data(url)
#     if response.status_code == 200:
#         sports_data = response.json()
#         print(sports_data)
#     else:
#         print(f"failed to retrieve data {response.status_code}")

#     sport_name = "49ers"
#     sports_info = all_sports(sport_name)

#     if sports_info:
#         print(f"{sports_info}")


@app.route("/homepage")
def homepage():
    # get_all method
    if "user_id" not in session:
        return redirect("/")
    query_results = Post.get_all()
    # url = f"{base_url}/homepage/{name}"
    # response = request.get(url)
    # print(nfl_teams_info[2:5])
    print(os.getenv("Do152709"))
    return render_template("homepage.html", all_post=query_results)


@app.route("/create")
def create():
    if "user_id" not in session:
        return redirect("/")
    query_results = Post.get_all()
    return render_template("sport_take.html", all_post=query_results)


@app.route("/wks_lounge")
def wks():
    # get_all method
    if "user_id" not in session:
        return redirect("/")
    query_results = Post.get_all()
    nfl_teams_info
    return render_template("sports_lounge.html", all_post=query_results)


@app.route("/update/<int:post_id>")
def update(post_id):
    if not "user_id" in session:
        flash("try again")
        return redirect("/")

    return render_template("edit.html", post=Post.get_by_id(post_id))


@app.route("/sport_take", methods=["POST"])
def sport_take():
    print("HOT TAKE!!")
    print(request.form)
    if not "user_id" in session:
        flash("try again")
        return redirect("/")
    if not Post.is_valid(request.form):
        print("WE ARE DEFINITELY HERE!")

        return redirect("/create")
    data = {
        "post": request.form["post"],
        "user_id": session["user_id"],
    }
    Post.create(data)
    print(request.form)
    return redirect("/homepage")


@app.route("/homepage/sport_take/<int:post_id>")
def wks_view_page(post_id):
    if not "user_id" in session:
        flash("Go register first")
        return redirect("/")

    # create variable to use to call on this html page in Jinja
    post = Post.join_tables_for_one_id(post_id)

    return render_template("wks_view_page.html", post=post)


@app.route("/homepage/view/<int:post_id>")
def view(post_id):
    if not "user_id" in session:
        flash("Go register first")
        return redirect("/")
    #    # get_all method

    # user = User.get_by_id("user_id")
    query_results = Post.get_by_id(post_id)
    # call the post class view = post.join_tables_for_one_id()
    return render_template("wks_view_page.html", all_post=query_results)


@app.route("/homepage/edit/<int:post_id>", methods=["POST"])
def edit(post_id):
    print(request.form)
    if not "user_id" in session:
        flash("Go register first")
        return redirect("/")
    if Post.is_valid(request.form):
        flash("Updated!")
        data = {
            "post": request.form["post"],
            "post_id": post_id,
            "user_id": session["user_id"],
        }
        Post.update(data)
        return redirect("/homepage")
    return redirect(f"/update/{post_id}")


@app.route("/homepage/update/<int:post_id>", methods=["POST"])
def update_edit(post_id):
    if not "user_id" in session:
        flash("try again")
        return redirect("/")
    if Post.is_valid(request.form):
        flash("Updated!")
    data = {
        "post": request.form["post"],
        "id": post_id,
        "user_id": session["user_id"],
    }
    Post.update(data)
    print(request.form)
    return redirect("/homepage")


@app.route("/homepage/delete/<int:post_id>")
def delete(post_id):
    if "user_id" not in session:
        return redirect("/")
    Post.delete(post_id)

    return redirect("/homepage")


@app.route("/sports_lounge/", methods=["POST"])
def sports_lounge():
    print("HOT TAKE!!")
    print(request.form)
    if not "user_id" in session:
        flash("try again")
        return redirect("/")
    if not Post.is_valid(request.form):
        print("WE ARE DEFINITELY HERE!")

        return redirect("/create")
    data = {
        "post": request.form["post"],
        "user_id": session["user_id"],
    }
    nfl_teams_info
    Post.create(data)
    print(request.form)
    return redirect("/wks_lounge")


@app.route("/search")
def search():
    favorite_team = nfl_teams_info
    return render_template("sports_lounge.html", favorite_team)
