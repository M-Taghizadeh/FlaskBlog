from app import db
from sqlalchemy import Column, Integer, String, Text

class Category(db.Model):
    __tablename__ = "Categories"
    id = Column(Integer, primary_key=True) 
    name = Column(String(128), nullable=False, unique=True) 
    description = Column(String(256), nullable=True) 
    slug = Column(String(128), nullable=False, unique=True) 

class Post(db.Model):
    __tablename__ = "Posts"
    id = Column(Integer, primary_key=True) 
    title = Column(String(128), nullable=False, unique=True) 
    summary = Column(String(256), nullable=True) 
    content = Column(Text, nullable=False) 
    slug = Column(String(128), nullable=False, unique=True) 