from app import db
from sqlalchemy import Column, Integer, String, Text, Table, ForeignKey


Posts_Categories = Table('Posts_Categories', db.metadata,
    Column('post_id', Integer, ForeignKey('Posts.id', ondelete='cascade')),
    Column('category_id',  Integer, ForeignKey('Categories.id', ondelete='cascade'))
)

class Category(db.Model):
    __tablename__ = "Categories"
    id = Column(Integer, primary_key=True) 
    name = Column(String(128), nullable=False, unique=True) 
    description = Column(String(256), nullable=True) 
    slug = Column(String(128), nullable=False, unique=True) 

    # define a relationship (dont need to flask db migrate , that use in python side)
    # relationship ('related_class_name', secondary=middle_tbl_name, back_populates='this_tbl_name')
    posts = db.relationship('Post', secondary=Posts_Categories, back_populates='categories')

class Post(db.Model):
    __tablename__ = "Posts"
    id = Column(Integer, primary_key=True) 
    title = Column(String(128), nullable=False, unique=True) 
    summary = Column(String(256), nullable=True) 
    content = Column(Text, nullable=False) 
    slug = Column(String(128), nullable=False, unique=True) 

    # define a relationship (dont need to flask db migrate , that use in python side)
    # relationship ('related_class_name', secondary=middle_tbl_name, back_populates='this_tbl_name')
    categories = db.relationship('Category', secondary=Posts_Categories, back_populates='posts')