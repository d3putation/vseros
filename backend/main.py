from core.functions import *
from fastapi import FastAPI



# app = FastAPI()

# app.include_router(user.router, prefix="/users", tags=["users"])
# app.include_router(tasks.router, prefix="/tasks", tags=["tasks"])

# @app.post("/create-tables/")
# def api_create_tables():
#     create_tables()
#     return {"message": "Таблицы созданы"}

# @app.post("/drop-tables/")
# def api_drop_tables():
#     drop_tables()
#     return {"message": "Таблицы удалены"}


create_tables()

# добавление юзера
# tasks = ['12', '21', '42']
# new_user_data = User(tg_id='123', fullname="penis", tasks_id=tasks,password='123', vs='test')


# asyncio.run(new_user(new_user_data))







#создание таска
# new_task_data = Task(owner_tg_id='asd', owner_fullname='sadas', task_text='купить подарок начальнику', date_create='2024-09-19', diedline='2024-09-25')
# new_task(new_task_data)

# data = UserOrm(tg_id='23', fullname='penis' )
# asyncio.run(new_userOrm(data=data))
# создание пользователя по уёбск(но мы так и будем делать )






