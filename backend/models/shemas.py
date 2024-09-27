from pydantic import BaseModel
import datetime


class User(BaseModel):
    tg_id: str
    fullname: str
    tasks_id: list
    password: str
    vs:str


class Task(BaseModel):
    owner_tg_id: str
    owner_fullname: str
    task_text: str
    date_create: datetime.datetime
    diedline: datetime.datetime
