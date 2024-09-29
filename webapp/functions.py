import pandas as pd
import torch
import torch.nn as nn
import torch.optim as optim
import random
import json
import os
from sklearn.preprocessing import LabelEncoder
import requests

# Параметры устройства
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Определение модели
class LSTMModel(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(LSTMModel, self).__init__()
        self.embedding = nn.Embedding(input_size, 50)
        self.lstm = nn.LSTM(50, hidden_size, batch_first=True)
        self.fc = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        x = self.embedding(x)
        x, _ = self.lstm(x)
        x = self.fc(x[:, -1, :])  # берем последний временной шаг
        return x

# Загрузка данных
video_data = pd.read_parquet('video_stat.parquet')  # Загружаем весь датасет
log_data = pd.read_parquet('logs_df_2024-08-05.parquet').sample(n=1000)  # Загрузка небольшой выборки

# Создание экземпляров LabelEncoder
video_encoder = LabelEncoder()
user_encoder = LabelEncoder()

# Кодирование идентификаторов видео
all_video_ids = pd.concat([video_data['video_id'], log_data['video_id']]).unique()
video_encoder.fit(all_video_ids)
video_data['video_id_encoded'] = video_encoder.transform(video_data['video_id'])
log_data['video_id_encoded'] = video_encoder.transform(log_data['video_id'])

# Кодирование идентификаторов пользователей
log_data['user_id_encoded'] = user_encoder.fit_transform(log_data['user_id'])

X, y, categories = [], [], []
for user_id in log_data['user_id'].unique():
    user_logs = log_data[log_data['user_id'] == user_id]
    seq = user_logs['video_id_encoded'].tolist()
    for i in range(1, len(seq)):
        X.append(seq[:i])  # Все до текущего
        y.append(seq[i])   # Текущее видео
        category_id = video_data.loc[video_data['video_id_encoded'] == seq[i], 'category_id']
        categories.append(category_id.values[0] if not category_id.empty else 0)  # Добавление категории

# Проверка на пустой список
if not X:
    print("Нет последовательностей для обучения. Проверьте данные в log_data.")
else:
    # Приведение последовательностей к одинаковой длине
    max_len = max(len(x) for x in X)
    X_padded = [x + [0] * (max_len - len(x)) for x in X]  # Добавление нулей для выравнивания
    X = torch.tensor(X_padded).to(device)
    y = torch.tensor(y).to(device)

# Параметры модели
input_size = len(video_encoder.classes_)  # Количество уникальных видео
hidden_size = 100
output_size = input_size

# Создание модели
model = LSTMModel(input_size, hidden_size, output_size).to(device)
optimizer = optim.Adam(model.parameters())
criterion = nn.CrossEntropyLoss()



# Загрузка сохраненной модели
model_save_path = 'video_recommendation_model.pth'
checkpoint = torch.load(model_save_path, map_location=device)
model.load_state_dict(checkpoint['model_state_dict'])

model.eval()

def recommend_video(user_preferences):
    model.eval()
    with torch.no_grad():
        # Кодирование пользовательских предпочтений
        encoded_preferences = video_encoder.transform(user_preferences)
        user_sequence = torch.tensor(encoded_preferences).unsqueeze(0).to(device)
        recommended_video = model(user_sequence)
        recommended_video_id = video_encoder.inverse_transform(recommended_video.argmax(dim=1).cpu().numpy())
        return recommended_video_id[0]






# URL базы данных
BASE_URL = "http://backend:5051/users"


def load_user_data(user_id):
    """Загружает данные пользователя через запрос к роутеру /get_user."""
    try:
        response = requests.get(f"{BASE_URL}/get_user/{user_id}")
        response.raise_for_status()
        data = response.json()
        return {
            "liked_videos": data.get("liked_videos", []),
            "favorite_category": data.get("favorite_category"),
            "disliked_categories": data.get("disliked_categories", []),  # Изменено для списка
            "liked_categories": data.get("liked_categories", []),  # Новый параметр для списка
        }
    except requests.RequestException as e:
        print(f"Ошибка при загрузке данных пользователя: {e}")
        return {
            "liked_videos": [],
            "favorite_category": None,
            "disliked_categories": [],
            "liked_categories": [],
        }


def save_user_data(user_id, user_data):
    """Сохраняет данные пользователя, обновляя понравившиеся и нелюбимые категории через роутеры."""
    try:
        # Обновление списка понравившихся видео
        for video_id in user_data["liked_videos"]:
            requests.put(f"{BASE_URL}/update_likeds", params={"id": user_id, "video_id": video_id})

        # Обновление любимой категории
        if user_data["favorite_category"]:
            requests.put(f"{BASE_URL}/add_tematics", params={"id": user_id, "tematic": user_data["favorite_category"]})

        # Обновление нелюбимых категорий
        for category in user_data["disliked_categories"]:
            requests.put(f"{BASE_URL}/update_dislikeds", params={"id": user_id, "video_id": category})

        # Обновление понравившихся категорий
        for category in user_data["liked_categories"]:
            requests.put(f"{BASE_URL}/add_tematics", params={"id": user_id, "tematic": category})

        print("Данные пользователя успешно сохранены.")
    except requests.RequestException as e:
        print(f"Ошибка при сохранении данных пользователя: {e}")


def update_user_preferences(user_id, current_video_id=None, reaction=None):
    """
    Обновляет предпочтения пользователя на основе его реакции на текущее видео.

    Параметры:
    - user_id (str): Идентификатор пользователя.
    - current_video_id (str, optional): Идентификатор текущего видео.
    - reaction (str, optional): Реакция пользователя на текущее видео ('like', 'dislike').
    """
    # Загрузка данных пользователя или инициализация новых данных, если их нет
    user_data = load_user_data(user_id)

    # Обновление данных пользователя на основе реакции на текущее видео
    if reaction == "like" and current_video_id:
        user_data["liked_videos"].append(current_video_id)
        video_info = video_data[video_data['video_id'] == current_video_id].iloc[0]
        category = video_info['category_id']
        if category not in user_data["liked_categories"]:
            user_data["liked_categories"].append(category)
    elif reaction == "dislike" and current_video_id:
        video_info = video_data[video_data['video_id'] == current_video_id].iloc[0]
        category = video_info['category_id']
        if category not in user_data["disliked_categories"]:
            user_data["disliked_categories"].append(category)

    # Сохранение обновленных данных пользователя
    save_user_data(user_id, user_data)



def recommend_video(user_preferences):
    """Recommend a video based on user preferences using the trained model."""
    model.eval()
    with torch.no_grad():
        encoded_preferences = video_encoder.transform(user_preferences)
        user_sequence = torch.tensor(encoded_preferences).unsqueeze(0).to(device)
        recommended_video = model(user_sequence)
        recommended_video_id = video_encoder.inverse_transform(recommended_video.argmax(dim=1).cpu().numpy())
        return recommended_video_id[0]




def get_top_recommendations(user_id, current_video_id=None, reaction=None, num_recommendations=10):
    """
    Получение списка рекомендуемых видеословарей, основанных на отзывах пользователей.

    Параметры:
    - user_id (str): Идентификатор пользователя.
    - current_video_id (str, необязательно): Идентификатор текущего видео.
    - reaction (str, необязательно): Реакция пользователя на текущее видео («нравится», «не нравится»).
    - num_recommendations (int, необязательно): Количество необходимых уникальных рекомендаций.

    Возвращает:
    - список: Список словарей с информацией о рекомендованных видео.

    """
    # Load the user data or initialize it if not found
    print("func ready")
    user_data = load_user_data(user_id)

    # Initialize disliked and liked categories if not present
    if "disliked_categories" not in user_data:
        user_data["disliked_categories"] = []
    if "liked_categories" not in user_data:
        user_data["liked_categories"] = []

    print("func 1")

    recommended_videos = set()  # Using a set to ensure uniqueness
    video_details = []  # List to store details of recommended videos

    # Filter video data to exclude disliked categories
    filtered_videos = video_data[~video_data['category_id'].isin(user_data["disliked_categories"])]

    # If the user has liked videos, use the recommendation model
    if user_data["liked_videos"]:
        print("Рекомендую...")

        # Use a for loop to limit to num_recommendations
        for _ in range(num_recommendations):
            recommended_video_id = recommend_video(user_data["liked_videos"])
            
            # Check if the recommended video is in filtered list
            if recommended_video_id in filtered_videos['video_id'].values and recommended_video_id not in recommended_videos:
                video_info = filtered_videos[filtered_videos['video_id'] == recommended_video_id].iloc[0]
                recommended_videos.add(recommended_video_id)
                video_details.append({
                    'video_id': video_info['video_id'],
                    'title': video_info['title'],
                    'description': video_info['description'],
                    'category_id': video_info['category_id']
                })

    # Fill with random videos if not enough recommendations or for new users
    while len(recommended_videos) < num_recommendations:
        random_video_id = random.choice(filtered_videos['video_id'].tolist())
        if random_video_id not in recommended_videos:
            video_info = filtered_videos[filtered_videos['video_id'] == random_video_id].iloc[0]
            recommended_videos.add(random_video_id)
            video_details.append({
                'video_id': video_info['video_id'],
                'title': video_info['title'],
                'description': video_info['description'],
                'category_id': video_info['category_id']
            })

    # Limit the result to the required number of recommendations
    return video_details[:num_recommendations]




def get_video_info(video_id):
    """
    Получает данные о видео по его ID.

    Параметры:
    - video_id (str): ID видео.

    Возвращает:
    - dict: Словарь с информацией о видео (название, описание, категория).
    """
    # Найти видео по ID
    video_info = video_data[video_data['video_id'] == video_id]
    
    if not video_info.empty:
        video_info = video_info.iloc[0]
        name = video_info.get('title', "")
        description = video_info.get('description', "")
        category = video_info.get('category_id', "")
    else:
        name = ""
        description = ""
        category = ""
    
    return {
        "video_id": video_id,
        "name": name,
        "description": description,
        "category": category
    }
