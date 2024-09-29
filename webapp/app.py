from flask import Flask, session, render_template, request, redirect
from flask_session import Session
import time
import requests
from functions import get_top_recommendations, get_video_info, update_user_preferences

print(1)
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
    print("flask функция")
    data = get_top_recommendations(session["id"])
    names = []
    ids = []
    descriptions = []
    categories = []
    for video in data:
        ids.append(video['video_id'])
        names.append(video["title"])
        descriptions.append(video["description"][:100])
        categories.append(video["category_id"])
    return render_template("recomendation.html", names = names, ids= ids, descriptions = descriptions, categories = categories)
    

@app.route("/video/<string:id>")
def video(id):
    data = get_video_info(id)
    name = data['name']
    description = data['description'][:100]
    category = data['category']
    video_id = data['video_id']
    return render_template("single_video.html", name = name, description = description, category = category, video_id = video_id)

@app.route('/update_pref/<video_id>', methods=['POST'])
def update_preference(video_id):
    data = request.get_json()  # Получаем данные из запроса
    action = data.get('action')  # Получаем значение 'like' или 'dislike'
    update_user_preferences(session['id'],video_id,action)
    if action == 'like':
        print(f"Video {video_id} liked.")
    elif action == 'dislike':
        print(f"Video {video_id} disliked.")
    return redirect(f"/video/{video_id}")

if __name__ == "__main__":
    app.run(host="webapp", port=8000)