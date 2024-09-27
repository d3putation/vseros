from sqlalchemy.orm import Mapped, mapped_column
from engines import Base
from sqlalchemy import Table, Column, Integer, MetaData, String, ARRAY, func
import enum
import datetime



class UserOrm(Base):
    __tablename__ = 'Users'

    id: Mapped[int] = mapped_column(primary_key=True)
    birth_date: Mapped[str] = mapped_column(String, unique=True)
    fullname: Mapped[str] = mapped_column(String)
    tematics: Mapped[list] = mapped_column(ARRAY(String), nullable=True)  # Используем ARRAY для хранения списка строк
    region: Mapped[str] = mapped_column(String, nullable=True)
    password: Mapped[str] = mapped_column(String, nullable=True)

class VideosORM(Base):
    
    __tablename__ = 'Videos'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    author_id: Mapped[int] 
    category: Mapped[str]
    created_date: Mapped[datetime.datetime]


