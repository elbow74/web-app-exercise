"""Virtual Closet web app."""

import os
from datetime import datetime, timezone
import re
from bson.errors import InvalidId
from bson.objectid import ObjectId
from flask import Flask, flash, redirect, render_template, request, url_for, abort
from flask_login import (
    LoginManager,
    UserMixin,
    current_user,
    login_required,
    login_user,
    logout_user,
)
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
@login_required
def account():
    """Render the logged-in user's posts."""
    posts = list(
        db.posts.find({"username": current_user.username}).sort("created_at", -1)
    )
    return render_template("account.html", posts=posts)


@app.route("/create", methods=["GET", "POST"])
@login_required
def create():
    """Show the new post form, add or remove hashtags and links, and save the post."""
    hashtags = []
    buy_links = []

    if request.method == "POST":
        caption = request.form.get("caption", "").strip()
        hashtags = request.form.getlist("hashtags")
        buy_links = request.form.getlist("buy_links")
        new_hashtag = request.form.get("new_hashtag", "").strip()
        new_link = request.form.get("new_link", "").strip()
        action = request.form.get("action", "post")

        if action in ("add", "post"):
            if new_hashtag:
                hashtags.append(new_hashtag)
            if new_link:
                buy_links.append(new_link)

        if action.startswith("remove_hashtag:"):
            removed = action.removeprefix("remove_hashtag:")
            hashtags = [tag for tag in hashtags if tag != removed]
        elif action.startswith("remove_link:"):
            removed = action.removeprefix("remove_link:")
            buy_links = [link for link in buy_links if link != removed]
        elif action == "post":
            if not caption:
                flash("Caption is required.")
            else:
                db.posts.insert_one(
                    {
                        "username": current_user.username,
                        "image_path": None,  # set by the image upload feature
                        "caption": caption,
                        "hashtags": hashtags,
                        "buy_links": buy_links,
                        "liked_by": [],
                        "created_at": datetime.now(timezone.utc),
                    }
                )
                return redirect(url_for("home"))

    return render_template(
        "create.html", form=request.form, hashtags=hashtags, buy_links=buy_links
    )


@app.route("/edit")
def edit():
    # """Render the edit post page."""
    return render_template("edit.html")


@app.route("/search")
@login_required
def search():
    """render the search results page."""

    query = request.args.get("search", "").strip()

    posts = []

    if query:
        posts = list(
            db.posts.find(
                {
                    "$or": [
                        {"caption": {"$regex": re.escape(query), "$options": "i"}},
                        {"hashtags": {"$regex": re.escape(query), "$options": "i"}},
                    ]
                }
            ).sort("created_at", -1)
        )
    return render_template("search.html", posts=posts, query=query)


@app.route("/like/<post_id>", methods=["POST"])
@login_required
def like_post(post_id):
    """Like a post, or unlike it if the user already liked it."""
    try:
        post = db.posts.find_one({"_id": ObjectId(post_id)})
    except InvalidId:
        post = None
    if post is None:
        abort(404)

    if current_user.id in post.get("liked_by", []):
        db.posts.update_one(
            {"_id": post["_id"]}, {"$pull": {"liked_by": current_user.id}}
        )
    else:
        db.posts.update_one(
            {"_id": post["_id"]}, {"$addToSet": {"liked_by": current_user.id}}
        )

    # go back to the page the like came from, scrolled to this post
    next_url = request.form.get("next", "")
    if not next_url.startswith("/") or next_url.startswith(("//", "/\\")):
        next_url = url_for("home")
    return redirect(f"{next_url}#post-{post_id}")


if __name__ == "__main__":
    app.run(debug=True)
