"""Virtual Closet web app."""

from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def home():
    # """Render the home page."""
    return render_template("index.html")


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
