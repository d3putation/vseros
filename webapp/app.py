from flask import Flask, session, render_template, redirect
from flask_session import Session
import time
import requests
from functions import get_top_recommendations

app = Flask(__name__)
app.secret_key = 'bebra'
app.debug = True

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app=app)

def get_latest_id():
    return str(time.time())

def add_user(id):
    requests.post("http://backend:5051/users/new_user", params={"data": id})

@app.route("/")
def startpage():
    if "id" not in session:
        id = get_latest_id()
        print("got")
        add_user(id)
        session["id"] = id
    data = get_top_recommendations(session["id"])
    names = []

    descriptions = []
    categories = []
    for video in data:
        names.append(video["title"])
        descriptions.append(video["description"])
        categories.append(video["category_id"])
    return render_template("recomendation.html", names = names, descriptions = descriptions, categories = categories)
    

@app.route("/video/{id}")
def video(id):
    name = ""
    description = ""
    category = ""
    return render_template("single_video.html", name = name, description = description, category = category)

if __name__ == "__main__":
    app.run(host="webapp", port=8000)
