"""Virtual Closet web app."""

from flask import Flask, render_template
from db import db

app = Flask(__name__)


@app.route("/")
@app.route("/")
def home():
    # """Render the home page with the newest posts first."""
    posts = list(db.posts.find().sort("created_at", -1))
    return render_template("index.html", posts=posts)


@app.route("/authentication")
def authenticate():
    # """Render the user authentication page."""
    return render_template("authentication.html")


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


if __name__ == "__main__":
    app.run(debug=True)
