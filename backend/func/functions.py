from sqlalchemy import text, insert, select, update
from engines import async_engine, async_session_factory, Base,engine
from models.models import  metadata_obj, users_table
from models.shemas import  User
from models.orm import UserOrm


# def create_tables():
    
#     metadata_obj.create_all(engine)


def create_tables():
    Base.metadata.create_all(engine)


def drop_tables():
    Base.metadata.drop_all(engine)


        
async def new_user(data:str):  
    async with async_session_factory() as session:
        user = UserOrm(id=data, tematics=[], liked_videos=[],disled_videos=[], watched_videos=[])
        session.add(user)
        await session.commit()
    return 'пользователь создан'
    





async def get_user(id:str) -> dict:
    async with async_session_factory() as session:
        result = await session.execute(select(UserOrm).filter_by(id=id))
        user = result.scalar_one_or_none()
        return user
        



async def update_password(id:str, new_pass:str):
    async with async_session_factory() as session:
        result = await session.execute(select(UserOrm).filter_by(id=id))
        user = result.scalar_one_or_none()
        if user:
            user.password = new_pass
            await session.commit()
    return 'Пароль изменён'

async def update_likeds(id:str, video_id: str):
       
       async with async_session_factory() as session:
        result = await session.execute(select(UserOrm).filter_by(id=id))
        user = result.scalar_one_or_none()
        if user:
            lister = list(user.liked_videos) if user.liked_videos is not None else []
            print('++++++++++++++++++++++++++++++++++')
            if video_id not in lister:
                lister.append(video_id)
                print(lister)
                user.liked_videos = lister
                
                print(user.liked_videos) 
                print('пользователь добавлен')
                await session.commit()
                print('видео добавлено')

        else:
            print('пользователь не найден')



async def get_liked_video(id:str):
    async with async_session_factory() as session:
        result = await session.execute(select(UserOrm).filter_by(id=id))
        user = result.scalar_one_or_none()
        if user:
            videos = user.liked_videos
            return videos
        else: 
            return 'нету пользователя'


async def update_dislikeds(id:str, video_id: str):
    async with async_session_factory() as session:
        result = await session.execute(select(UserOrm).filter_by(id=id))
        user = result.scalar_one_or_none()
        if user:
            
            print('++++++++++++++++++++++++++++++++++')
            dis = list(user.disled_videos) if user.disled_videos is not None else []
            if video_id not in dis:
                dis.append(video_id)
                print(dis)
                user.disled_videos = dis
                
                print(user.disled_videos) 
                print('пользователь добавлен')
                await session.commit()
                print('видео добавлено')
        else:
            print('пользователь не найден')



async def add_tematics(id:str, tematic:str):
    async with async_session_factory() as session:
        result = await  session.execute(select(UserOrm).filter_by(id=id))
        user = result.scalar_one_or_none()
        if user:
            tem = list(user.watched_videos) if user.watched_videos is not None else []
            tem.append(tematic)
            user.watched_videos = tem
            await session.commit()


async def get_disliked_video(id:str):
    async with async_session_factory() as session:
        result = await session.execute(select(UserOrm).filter_by(id=id))
        user = result.scalar_one_or_none()
        if user:
            videos = user.liked_videos
            return videos
        else: 
            return 'нету пользователя'
        

