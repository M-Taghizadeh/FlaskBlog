from app import db
from sqlalchemy import Column, Integer, String, DateTime
import datetime as dt

class File(db.Model):
    __tablename__ = "files"
    id = Column(Integer(), primary_key=True)
    filename = Column(String(256), nullable=False, unique=True)
    upload_date = Column(DateTime(), nullable=False, default=dt.datetime.utcnow)