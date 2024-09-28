from fastapi import APIRouter
from func.functions import *
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter()

class UserData(BaseModel):
    id: str
    tematics: Optional[List[str]] = []
    liked_videos: Optional[List[str]] = []
    disled_videos: Optional[List[str]] = []
    watched_videos: Optional[List[str]] = []

@router.post("/create_tables")
def create_tables_endpoint():
    create_tables()
    return {"message": "Tables created"}

@router.post("/drop_tables")
def drop_tables_endpoint():
    drop_tables()
    return {"message": "Tables dropped"}

@router.post("/new_user")
async def new_user_endpoint(data: str):
    result = await new_user(data)
    return {"message": result}

@router.get("/get_user/{id}")
async def get_user_endpoint(id: str):
    result = await get_user(id)
    return result

@router.put("/update_password")
async def update_password_endpoint(id: str, new_pass: str):
    result = await update_password(id, new_pass)
    return {"message": result}

@router.put("/update_likeds")
async def update_likeds_endpoint(id: str, video_id: str):
    await update_likeds(id, video_id)
    return {"message": "Liked videos updated"}

@router.get("/get_liked_video/{id}")
async def get_liked_video_endpoint(id: str):
    result = await get_liked_video(id)
    return result

@router.put("/update_dislikeds")
async def update_dislikeds_endpoint(id: str, video_id: str):
    await update_dislikeds(id, video_id)
    return {"message": "Disliked videos updated"}

@router.put("/add_tematics")
async def add_tematics_endpoint(id: str, tematic: str):
    await add_tematics(id, tematic)
    return {"message": "Tematics added"}

@router.get("/get_disliked_video/{id}")
async def get_disliked_video_endpoint(id: str):
    result = await get_disliked_video(id)
    return result
