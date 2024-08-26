from flask_app import app
from flask import Flask, request, jsonify

from flask_app.controllers import post_controller

from flask_app.controllers import user_controller

from flask_app.models import post
from flask_app.models import user
import os


print(os.getenv("Do152709"))


if __name__ == "__main__":
    app.run(debug=True, host="localhost", port=5001)
