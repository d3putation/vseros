from sqlalchemy import text, insert, select, update
from engines import async_engine, async_session_factory, Base,engine
from models.models import  metadata_obj, videos_table, users_table
from models.shemas import Video, User
from models.orm import UserOrm, VideosORM


# def create_tables():
    
#     metadata_obj.create_all(engine)


def create_tables():
    Base.metadata.create_all(engine)


def drop_tables():
    Base.metadata.drop_all(engine)


        
async def new_user(data:UserOrm):
    
    async with async_session_factory() as session:
    
        session.add(data)
        await session.commit()
    return 'пользователь создан'
    


# создание таска
async def new_video(video_data:VideosORM):
    async with async_session_factory() as session:
        session.add(video_data)
        await session.commit()
    return 'Задача создана'



async def get_user(id:int) -> dict:
    async with async_session_factory() as session:
        result = await session.execute(select(UserOrm).filter_by(id=id))
        user = result.scalar_one_or_none()
        res = {'birth_date': user.birth_datem, 'fullname': user.fullname, "tematics":user.tematics, 'region': user.region, 'password': user.password}
    
        return res
        



async def update_password(id:str, new_pass:str):
    async with async_session_factory() as session:
        result = await session.execute(select(UserOrm).filter_by(id=id))
        user = result.scalar_one_or_none()
        if user:
            user.password = new_pass
            await session.commit()
    return 'Пароль изменён'


async def update_dislike(id:int, dis:int):
    async with async_session_factory() as session:
        result = await session.execute(select(VideosORM).filter_by(id=id))
        video = result.scalar_one_or_none()
        if video:
            video.dislike_count += dis
            await session.commit()
    return 'колличество дизлайков изменено'


async def update_like(id:int, lik:int):
    async with async_session_factory() as session:
        result = await session.execute(select(VideosORM).filter_by(id=id))
        video = result.scalar_one_or_none()
        if video:
            video.likes_count += lik
            await session.commit()
    return 'колличество дизлайков изменено'