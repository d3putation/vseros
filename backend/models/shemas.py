from pydantic import BaseModel
import datetime


class User(BaseModel):
    birth_date: datetime.datetime
    fullname: str
    tematics: list
    region: str
    password:str
    liked_videos: list


