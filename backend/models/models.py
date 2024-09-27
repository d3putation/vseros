from pydantic import BaseModel
from sqlalchemy import Table, Column, Integer, String, MetaData, ARRAY, DATE, Text
from sqlalchemy.orm import Mapped, mapped_column
from engines import Base
import datetime


metadata_obj = MetaData(schema='ai')





users_table  = Table(
     'Users',
     metadata_obj,
    Column('id', Integer, primary_key=True),
    Column('birth_date', String),
    Column('fullname', String),
    Column('tematics', ARRAY(String)),
    Column('region', String),
    Column('password', String),
    
)


videos_table = Table(
    'Videos',
    metadata_obj,
    Column('id', Integer, primary_key=True),
    Column('name', String),
    Column('author_id', Integer),
    Column('category', String),
    Column('created_date', String),
    Column('likes_count', Integer),
    Column('dislike_count', Integer),
)




