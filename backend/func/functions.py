from sqlalchemy import text, insert, select, update
from engines import async_engine, async_session_factory, Base, engine
from models.models import metadata_obj, users_table
from models.shemas import User
from models.orm import UserOrm

# Function to create tables using SQLAlchemy Base metadata
def create_tables():
    Base.metadata.create_all(engine)  # Creates all tables defined in the metadata on the provided engine

# Function to drop tables using SQLAlchemy Base metadata
def drop_tables():
    Base.metadata.drop_all(engine)  # Drops all tables defined in the metadata from the provided engine

# Asynchronous function to add a new user to the database
async def new_user(data: str):  
    async with async_session_factory() as session:  # Opens an async session
        # Create a new user using UserOrm (the ORM model) with empty lists for fields like tematics, liked_videos, etc.
        user = UserOrm(id=data, tematics=[], liked_videos=[], disled_videos=[], watched_videos=[])
        session.add(user)  # Adds the new user to the session
        await session.commit()  # Commits the session (saves the user in the database)
    return 'пользователь создан'  # Returns a message indicating that the user was created

# Asynchronous function to get a user's data by their ID
async def get_user(id: str) -> dict:
    async with async_session_factory() as session:  # Opens an async session
        result = await session.execute(select(UserOrm).filter_by(id=id))  # Executes a query to select a user by ID
        user = result.scalar_one_or_none()  # Gets the user if it exists, otherwise returns None
        return user  # Returns the user data (or None)

# Asynchronous function to update a user's password
async def update_password(id: str, new_pass: str):
    async with async_session_factory() as session:  # Opens an async session
        result = await session.execute(select(UserOrm).filter_by(id=id))  # Finds the user by ID
        user = result.scalar_one_or_none()  # Gets the user if it exists
        if user:
            user.password = new_pass  # Updates the user's password field
            await session.commit()  # Commits the changes to the database
    return 'Пароль изменён'  # Returns a message indicating the password was updated

# Asynchronous function to update the liked videos for a user
async def update_likeds(id: str, video_id: str):
    async with async_session_factory() as session:  # Opens an async session
        result = await session.execute(select(UserOrm).filter_by(id=id))  # Finds the user by ID
        user = result.scalar_one_or_none()  # Gets the user if it exists
        if user:
            lister = list(user.liked_videos) if user.liked_videos is not None else []  # Converts liked videos to a list
            if video_id not in lister:  # Adds the video to liked videos if it's not already in the list
                lister.append(video_id)
                user.liked_videos = lister  # Updates the liked_videos field
                await session.commit()  # Commits the changes to the database
        else:
            print('пользователь не найден')  # Prints an error message if the user is not found

# Asynchronous function to retrieve a user's liked videos by ID
async def get_liked_video(id: str):
    async with async_session_factory() as session:  # Opens an async session
        result = await session.execute(select(UserOrm).filter_by(id=id))  # Finds the user by ID
        user = result.scalar_one_or_none()  # Gets the user if it exists
        if user:
            videos = user.liked_videos  # Retrieves the liked videos
            return videos  # Returns the liked videos list
        else: 
            return 'нету пользователя'  # Returns a message if the user is not found

# Asynchronous function to update the disliked videos for a user
async def update_dislikeds(id: str, video_id: str):
    async with async_session_factory() as session:  # Opens an async session
        result = await session.execute(select(UserOrm).filter_by(id=id))  # Finds the user by ID
        user = result.scalar_one_or_none()  # Gets the user if it exists
        if user:
            dis = list(user.disled_videos) if user.disled_videos is not None else []  # Converts disliked videos to a list
            if video_id not in dis:  # Adds the video to disliked videos if it's not already in the list
                dis.append(video_id)
                user.disled_videos = dis  # Updates the disliked_videos field
                await session.commit()  # Commits the changes to the database
        else:
            print('пользователь не найден')  # Prints an error message if the user is not found

# Asynchronous function to add a new tematic (category/topic) to a user's watched videos list
async def add_tematics(id: str, tematic: str):
    async with async_session_factory() as session:  # Opens an async session
        result = await session.execute(select(UserOrm).filter_by(id=id))  # Finds the user by ID
        user = result.scalar_one_or_none()  # Gets the user if it exists
        if user:
            tem = list(user.watched_videos) if user.watched_videos is not None else []  # Converts watched videos to a list
            tem.append(tematic)  # Adds the tematic (category/topic) to the list
            user.watched_videos = tem  # Updates the watched_videos field
            await session.commit()  # Commits the changes to the database

# Asynchronous function to retrieve a user's disliked videos by ID
async def get_disliked_video(id: str):
    async with async_session_factory() as session:  # Opens an async session
        result = await session.execute(select(UserOrm).filter_by(id=id))  # Finds the user by ID
        user = result.scalar_one_or_none()  # Gets the user if it exists
        if user:
            videos = user.liked_videos  # Retrieves the liked videos (seems incorrect; should return disliked videos)
            return videos  # Returns the liked videos list (possibly a bug, as it should return disliked_videos)
        else: 
            return 'нету пользователя'  # Returns a message if the user is not found