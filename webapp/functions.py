import pandas as pd
import torch
import torch.nn as nn
import torch.optim as optim
import random
import json
import os
from sklearn.preprocessing import LabelEncoder


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

# Обучение модели
epochs = 10
for epoch in range(epochs):
    model.train()
    optimizer.zero_grad()
    outputs = model(X)
    loss = criterion(outputs, y)
    loss.backward()
    optimizer.step()
    print(f'Epoch [{epoch + 1}/{epochs}], Loss: {loss.item():.4f}')

# Сохранение модели
model_save_path = 'video_recommendation_model.pth'
torch.save({
    'model_state_dict': model.state_dict(),
    'optimizer_state_dict': optimizer.state_dict(),
}, model_save_path)

# Логика для взаимодействия с пользователями
def load_user_data(user_id):
    # Загрузка данных пользователя из файла
    user_file = f'user_data_{user_id}.json'
    if os.path.exists(user_file):
        with open(user_file, 'r') as f:
            return json.load(f)
    else:
        # Если файла нет, создаем структуру данных для нового пользователя
        return {
            "liked_videos": [],
            "favorite_category": None,
            "disliked_categories": set(),
        }

def save_user_data(user_id, user_data):
    # Сохранение данных пользователя в файл
    user_file = f'user_data_{user_id}.json'
    user_data["liked_videos"] = [str(video) for video in user_data["liked_videos"]]
    user_data["disliked_categories"] = list(user_data["disliked_categories"])
    with open(user_file, 'w') as f:
        json.dump(user_data, f)
    print("Данные пользователя сохранены.")

def recommend_video(user_preferences):
    model.eval()
    with torch.no_grad():
        # Кодирование пользовательских предпочтений
        encoded_preferences = video_encoder.transform(user_preferences)
        user_sequence = torch.tensor(encoded_preferences).unsqueeze(0).to(device)
        recommended_video = model(user_sequence)
        recommended_video_id = video_encoder.inverse_transform(recommended_video.argmax(dim=1).cpu().numpy())
        return recommended_video_id[0]




# Assuming video_data and the trained model are already loaded and available in your environment

def load_user_data(user_id):
    """Load user data from JSON or initialize a new structure if not found."""
    try:
        with open('user_data.json', 'r') as f:
            all_user_data = json.load(f)
        return all_user_data.get(user_id, {"liked_videos": [], "favorite_category": None, "disliked_categories": set()})
    except (FileNotFoundError, json.JSONDecodeError):
        # Return default if no data is available
        return {"liked_videos": [], "favorite_category": None, "disliked_categories": set()}

def save_user_data(user_id, user_data):
    """Save user data to JSON, adding it to the existing data."""
    try:
        with open('user_data.json', 'r') as f:
            all_user_data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        all_user_data = {}
    
    all_user_data[user_id] = user_data

    with open('user_data.json', 'w') as f:
        # Convert sets to lists for JSON serialization
        all_user_data_serializable = {uid: {
            "liked_videos": [str(vid) for vid in data["liked_videos"]],
            "favorite_category": str(data["favorite_category"]) if data["favorite_category"] else None,
            "disliked_categories": list(data["disliked_categories"])
        } for uid, data in all_user_data.items()}
        json.dump(all_user_data_serializable, f)

def recommend_video(user_preferences):
    """Recommend a video based on user preferences using the trained model."""
    model.eval()
    with torch.no_grad():
        encoded_preferences = video_encoder.transform(user_preferences)
        user_sequence = torch.tensor(encoded_preferences).unsqueeze(0).to(device)
        recommended_video = model(user_sequence)
        recommended_video_id = video_encoder.inverse_transform(recommended_video.argmax(dim=1).cpu().numpy())
        return recommended_video_id[0]

def get_recommendation(user_id, current_video_id=None, reaction=None):
    """
    Get a recommendation based on user feedback.
    
    Parameters:
    - user_id (str): The ID of the user.
    - current_video_id (str, optional): The ID of the current video.
    - reaction (str, optional): The user's reaction to the current video ('like', 'dislike').

    Returns:
    - str: The recommended video ID.
    """
    # Load the user data or initialize it if not found
    user_data = load_user_data(user_id)

    # Update user data based on the reaction to the current video
    if reaction == "like" and current_video_id:
        user_data["liked_videos"].append(current_video_id)
        video_info = video_data[video_data['video_id'] == current_video_id].iloc[0]
        user_data["favorite_category"] = video_info['category_id']
    elif reaction == "dislike" and current_video_id:
        video_info = video_data[video_data['video_id'] == current_video_id].iloc[0]
        user_data["disliked_categories"].add(video_info['category_id'])
    
    # Save updated user data
    save_user_data(user_id, user_data)
    
    # Recommend a video
    if not user_data["liked_videos"]:
        random_video_id = random.choice(video_data['video_id'].tolist())
    else:
        random_video_id = recommend_video(user_data["liked_videos"])

    video_info = video_data[video_data['video_id'] == random_video_id].iloc[0]
    video_category = video_info['category_id']

    # Handle disliked categories
    if video_category in user_data["disliked_categories"]:
        alternative_videos = video_data[~video_data['category_id'].isin(user_data["disliked_categories"])]
        if not alternative_videos.empty:
            random_video_id = random.choice(alternative_videos['video_id'].tolist())
        else:
            available_disliked_videos = video_data[video_data['category_id'].isin(user_data["disliked_categories"])]
            if not available_disliked_videos.empty:
                random_video_id = random.choice(available_disliked_videos['video_id'].tolist())
            else:
                return None  # No available videos

    return random_video_id
