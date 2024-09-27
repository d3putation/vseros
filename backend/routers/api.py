from fastapi import APIRouter, Depends
from func.functions import (
    create_tables, drop_tables, new_user, new_video, get_user,
    update_password, update_dislike, update_like
)
from models.orm import UserOrm, VideosORM

router = APIRouter()

@router.post("/create_tables")
async def create_db_tables():
    create_tables()
    return {"message": "Tables created"}

@router.post("/drop_tables")
async def drop_db_tables():
    drop_tables()
    return {"message": "Tables dropped"}

@router.post("/new_user")
async def create_user(user: UserOrm):
    return await new_user(user)

@router.post("/new_video")
async def create_video(video: VideosORM):
    return await new_video(video)

@router.get("/get_user/{id}")
async def read_user(id: int):
    return await get_user(id)

@router.put("/update_password/{id}")
async def change_password(id: int, new_pass: str):
    return await update_password(id, new_pass)

@router.put("/update_dislike/{id}")
async def change_dislike(id: int, dis: int):
    return await update_dislike(id, dis)

@router.put("/update_like/{id}")
async def change_like(id: int, lik: int):
    return await update_like(id, lik)
