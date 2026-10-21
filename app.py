"""Virtual Closet web app."""

import os

from bson.errors import InvalidId
from bson.objectid import ObjectId
from flask import Flask, flash, redirect, render_template, request, url_for
from flask_login import (
    LoginManager,
    UserMixin,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from markupsafe import escape
from werkzeug.security import check_password_hash, generate_password_hash

from db import db

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "dev")

login_manager = LoginManager(app)
login_manager.login_view = "authenticate"


class User(UserMixin):
    """Logged-in user, built from a document in the users collection."""

    def __init__(self, doc):
        self.id = str(doc["_id"])
        self.username = doc["username"]


@login_manager.user_loader
def load_user(user_id):
    """Load a user from the session's stored id."""
    try:
        doc = db.users.find_one({"_id": ObjectId(user_id)})
    except InvalidId:
        return None
    return User(doc) if doc else None


@app.route("/authentication", methods=["GET", "POST"])
def authenticate():
    """Log in, or create an account if the username is new."""
    if current_user.is_authenticated:
        return redirect(url_for("home"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        doc = db.users.find_one({"username": username})

        if not username or not password:
            flash("Username and password are required.")
        elif doc is None:
            result = db.users.insert_one(
                {
                    "username": username,
                    "password_hash": generate_password_hash(password),
                }
            )
            login_user(User({"_id": result.inserted_id, "username": username}))
            return redirect(url_for("home"))
        elif check_password_hash(doc["password_hash"], password):
            login_user(User(doc))
            return redirect(url_for("home"))
        else:
            flash("Incorrect password for that username.")

    return render_template("authentication.html")


@app.route("/")
@login_required
def home():
    """Render the home page."""
    posts = list(db.posts.find().sort("created_at", -1))
    return render_template("index.html", posts=posts)


@app.route("/logout")
@login_required
def logout():
    """Log out and return to the login page."""
    logout_user()
    return redirect(url_for("authenticate"))


@app.route("/account")
def account():
    # """Render the account page."""
    return render_template("account.html")


@app.route("/create")
def create():
    # """Render the create / new post page."""
    return render_template("create.html")


@app.route("/edit")
def edit():
    # """Render the edit post page."""
    return render_template("edit.html")

@app.route("/search")
def search():
    # """Render the search page."""
    return render_template("search.html")

if __name__ == "__main__":
    app.run(debug=True)
