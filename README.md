"Veezy"

Для запуска склонируйте репозиторий в каталог, не имеющий в своем названии русских букв
```
git clone https://github.com/blackUser-hub/hackOmsk.git
```
В директорию ```/vseros/webapp``` добавьте модель скачанную по [ссылке](https://dropmefiles.com/yBSHF) и [файлы из тренировочного датасета](https://lodmedia.hb.bizmrg.com/case_files/1128664/train_dataset_cold_start_train.zip)

# На компьютерах с ОС Windows:
Скачайте приложение [Docker Desktop](https://www.docker.com/products/docker-desktop/) и проведите его первоначальную настройку

В каталоге программы выполните команду:
```
docker compose up -d
```

выберите консоль контейнера webapp и дождитесь сообщения от фласка об успешном запуске веб-приложения
P.S. При возникновении ошибки пропишите в директории проекта команду:

```
docker compose up -d --build webapp
```




# На компьютерах с Linux:
Перейдите на [сайт документации docker](https://docs.docker.com/engine/install/), выберите свою систему и следуйте инструкциям

В каталоге программы выполните команду:
```
docker compose up -d
```
Выполните команду ```docker logs --follow webapp``` дождитесь сообщения от фласка об успешном запуске веб-приложения
P.S. При возникновении ошибки пропишите в директории проекта команду:

```
docker compose up -d --build webapp
```

# Взаимодействие с СУБД

Перейдите в админ панель базы данных по [ссылке](localhost:15432) и войдите по данным из файла .env (PGADMIN_EMAIL, PGADMIN_PASSWORD)

  1. На главном экране нажмите "Add new server"
  2. Во вкладке General введите postgres в поле "name"
  3. Во вкладке Connection введите db в поле "Host name", username и password из .env (DB_USER, DB_PASSWORD)
  4. Нажмите "connect"

для работы с веб-приложением перейдите по [ссылке](http://localhost:8000)
