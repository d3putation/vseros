from pydantic import BaseModel
import datetime


class User(BaseModel):
    birth_date: datetime.datetime
    fullname: str
    tematics: list
    region: str
    password:str


class Video(BaseModel):
    name: str 
    author_id: int
    category: str
    date_create: datetime.datetime



