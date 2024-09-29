from flask import Flask, session, render_template, redirect
from flask_session import Session
import time
import requests
from functions import get_recommendation

app = Flask(__name__)
app.secret_key = 'bebra'
app.debug = True

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app=app)

def get_latest_id():
    return str(time.time())

def add_user(id):
    requests.post("http://backend:8000/users/new_user", params={"data": id})

@app.route("/")
def startpage():
    if "id" not in session:
        id = get_latest_id()
        print("got")
        add_user(id)
        session["id"] = id
    data = get_recommendation(session["id"])
    names = [res["title"] for res in data]

    descriptions = [res["description"] for res in data]
    categories = [res["category_id"] for res in data]
    return render_template("recomendation.html", names = names, descriptions = descriptions, categories = categories)
    

@app.route("/video/{id}")
def video(id):
    name = ""
    description = ""
    category = ""
    return render_template("single_video.html", name = name, description = description, category = category)

if __name__ == "__main__":
    app.run(host="webapp", port=5555)