from pydantic import BaseModel
from sqlalchemy import Table, Column, Integer, String, MetaData, ARRAY, DATE, Text
from sqlalchemy.orm import Mapped, mapped_column
from engines import Base
import datetime


metadata_obj = MetaData(schema='ai')





users_table  = Table(
     'Users',
     metadata_obj,
    Column('id', String, primary_key=True),
    Column('birth_date', String),
    Column('fullname', String),
    Column('tematics', ARRAY(String)),
    Column('region', String),
    Column('password', String),
    Column('liked_videos', ARRAY(String)),
    Column('disled_videos', ARRAY(String))
)

