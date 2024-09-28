from pydantic import BaseModel
import datetime


class User(BaseModel):
    id: str
    birth_date: datetime.datetime
    fullname: str
    tematics: list
    region: str
    password:str
    liked_videos: list
    disled_videos: list