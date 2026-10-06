from sqlalchemy import Column, Integer, String, Text

from database import base


class Blog(base):
    __tablename__ = "blogs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column("tittle", String, nullable=False)
    content = Column(Text, nullable=False)


class User(base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
