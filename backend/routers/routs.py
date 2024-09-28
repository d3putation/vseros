from fastapi import APIRouter
from func.functions import *
from pydantic import BaseModel
from typing import List, Optional

# Create a new router instance to define API routes
router = APIRouter()

# Define a Pydantic model for user data that can be used for validation in request bodies
class UserData(BaseModel):
    id: str
    tematics: Optional[List[str]] = []       # Optional list of tematics (topics or categories)
    liked_videos: Optional[List[str]] = []   # Optional list of liked video IDs
    disled_videos: Optional[List[str]] = []  # Optional list of disliked video IDs (typo in "disled" should be "disliked")
    watched_videos: Optional[List[str]] = [] # Optional list of watched video IDs

# Endpoint to create database tables by calling the `create_tables` function
@router.post("/create_tables")
def create_tables_endpoint():
    create_tables()  # Calls the function to create database tables
    return {"message": "Tables created"}  # Returns a success message

# Endpoint to drop database tables by calling the `drop_tables` function
@router.post("/drop_tables")
def drop_tables_endpoint():
    drop_tables()  # Calls the function to drop database tables
    return {"message": "Tables dropped"}  # Returns a success message

# Endpoint to add a new user by passing a string data to `new_user`
@router.post("/new_user")
async def new_user_endpoint(data: str):
    result = await new_user(data)  # Calls the asynchronous function to add a new user
    return {"message": result}     # Returns the result message

# Endpoint to get user data by their ID
@router.get("/get_user/{id}")
async def get_user_endpoint(id: str):
    result = await get_user(id)  # Calls the asynchronous function to retrieve user data by ID
    return result                # Returns the user data

# Endpoint to update a user's password
@router.put("/update_password")
async def update_password_endpoint(id: str, new_pass: str):
    result = await update_password(id, new_pass)  # Calls the async function to update the user's password
    return {"message": result}                    # Returns the result message

# Endpoint to update a user's liked videos list by adding a new video ID
@router.put("/update_likeds")
async def update_likeds_endpoint(id: str, video_id: str):
    await update_likeds(id, video_id)  # Calls the async function to add a video to the liked videos list
    return {"message": "Liked videos updated"}  # Returns a success message

# Endpoint to get the list of liked videos for a specific user by their ID
@router.get("/get_liked_video/{id}")
async def get_liked_video_endpoint(id: str):
    result = await get_liked_video(id)  # Calls the async function to retrieve the user's liked videos
    return result                       # Returns the list of liked videos

# Endpoint to update a user's disliked videos list by adding a new video ID
@router.put("/update_dislikeds")
async def update_dislikeds_endpoint(id: str, video_id: str):
    await update_dislikeds(id, video_id)  # Calls the async function to add a video to the disliked videos list
    return {"message": "Disliked videos updated"}  # Returns a success message

# Endpoint to add a new tematic (topic or category) to a user's tematic list
@router.put("/add_tematics")
async def add_tematics_endpoint(id: str, tematic: str):
    await add_tematics(id, tematic)  # Calls the async function to add a tematic to the user's profile
    return {"message": "Tematics added"}  # Returns a success message

# Endpoint to get the list of disliked videos for a specific user by their ID
@router.get("/get_disliked_video/{id}")
async def get_disliked_video_endpoint(id: str):
    result = await get_disliked_video(id)  # Calls the async function to retrieve the user's disliked videos
    return result                          # Returns the list of disliked videos