from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "<h1>Virtual Closet</h1><p>It works!</p>"

if __name__ == "__main__":
    app.run(debug=True)