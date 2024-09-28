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

# Основной цикл взаимодействия с пользователями
while True:
    user_id = input("Введите ваш user_id (или 'exit' для выхода): ")
    if user_id == 'exit':
        break

    user_data = load_user_data(user_id)

    while True:
        if not user_data["liked_videos"]:
            random_video_id = random.choice(video_data['video_id'].tolist())  # Используйте оригинальные ID видео
        else:
            random_video_id = recommend_video(user_data["liked_videos"])
        
        # Получение информации о видео
        video_info = video_data[video_data['video_id'] == random_video_id].iloc[0]  # Поиск по оригинальному ID
        video_category = video_info['category_id']  # Получите категорию видео

        # Проверка на нежелательные категории
        if video_category in user_data["disliked_categories"]:
            print(f"Рекомендуемое видео ID {random_video_id} относится к нежелательной категории.")
            
            # Попытка найти видео из другой категории
            alternative_videos = video_data[~video_data['category_id'].isin(user_data["disliked_categories"])]
            
            if not alternative_videos.empty:
                random_video_id = random.choice(alternative_videos['video_id'].tolist())
                video_info = alternative_videos[alternative_videos['video_id'] == random_video_id].iloc[0]
                print(f"Рекомендуемое видео ID: {video_info['video_id']}, Заголовок: {video_info['title']}, Описание: {video_info['description']}")
            else:
                print("Нет доступных видео из других категорий. Рекомендуем из непривлекательных категорий.")

                available_disliked_videos = video_data[video_data['category_id'].isin(user_data["disliked_categories"])]
                if not available_disliked_videos.empty:
                    random_video_id = random.choice(available_disliked_videos['video_id'].tolist())
                    video_info = available_disliked_videos[available_disliked_videos['video_id'] == random_video_id].iloc[0]
                    print(f"Рекомендуемое видео ID: {video_info['video_id']}, Заголовок: {video_info['title']}, Описание: {video_info['description']}")
                else:
                    print("Нет доступных видео из непривлекательных категорий. Попробуйте снова.")
                    continue  # Если нет доступных видео, продолжаем цикл
        else:
            print(f"Рекомендуемое видео ID: {video_info['video_id']}, Заголовок: {video_info['title']}, Описание: {video_info['description']}")
        
        # Запрос реакции пользователя
        user_input = input("Введите 'like' для лайка, 'dislike' для дизлайка (или 'exit' для выхода): ")
        if user_input == "like":
            user_data["liked_videos"].append(video_info['video_id'])
            user_data["favorite_category"] = video_info['category_id']
        elif user_input == "dislike":
            user_data["disliked_categories"].add(video_category)
            print(f"Категория '{video_category}' добавлена в список непривлекательных.")
            continue
        elif user_input == "exit":
            break

        save_user_data(user_id, user_data)
