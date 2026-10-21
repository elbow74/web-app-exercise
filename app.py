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
login_manager.login_view = "login"


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


@app.route("/")
@login_required
def home():
    """Render the home page."""
    return (
        f"<h1>Virtual Closet</h1>"
        f"<p>Logged in as {escape(current_user.username)}.</p>"
        f'<p><a href="{url_for("logout")}">Log out</a></p>'
    )


@app.route("/register", methods=["GET", "POST"])
def register():
    """Create an account and log the new user in."""
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        if not username or not password:
            flash("Username and password are required.")
        elif db.users.find_one({"username": username}):
            flash("That username is taken.")
        else:
            result = db.users.insert_one(
                {"username": username, "password_hash": generate_password_hash(password)}
            )
            login_user(User({"_id": result.inserted_id, "username": username}))
            return redirect(url_for("home"))
    return render_template("auth.html", title="Register", other="login")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log in with a username and password."""
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        doc = db.users.find_one({"username": username})
        if doc and check_password_hash(doc["password_hash"], password):
            login_user(User(doc))
            return redirect(url_for("home"))
        flash("Invalid username or password.")
    return render_template("auth.html", title="Log in", other="register")


@app.route("/logout")
@login_required
def logout():
    """Log out and return to the login page."""
    logout_user()
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)