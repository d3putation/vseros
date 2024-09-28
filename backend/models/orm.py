from sqlalchemy.orm import Mapped, mapped_column
from engines import Base
from sqlalchemy import Table, Column, Integer, MetaData, String, ARRAY, func
import enum
import datetime



class UserOrm(Base):
    __tablename__ = 'Users'

    id: Mapped[str] = mapped_column(primary_key=True)
    tematics: Mapped[list] = mapped_column(ARRAY(String), nullable=True)  # Используем ARRAY для хранения списка строк
    liked_videos: Mapped[list] = mapped_column(ARRAY(String), nullable=True)
    disled_videos: Mapped[list] = mapped_column(ARRAY(String), nullable=True)
    watched_videos: Mapped[list] = mapped_column(ARRAY(String), nullable=True)

