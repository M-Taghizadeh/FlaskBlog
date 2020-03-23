from sqlalchemy import Column, Integer, String
from app import db

from werkzeug.security import generate_password_hash ### for create password hash

class User(db.Model):
    __tablename__ = "users"
    id = Column(Integer, primary_key = True)
    email = Column(String(128), nullable=False, unique=True)
    password = Column(String(128), nullable=False)
    role = Column(Integer(), nullable=False, default=0)
    full_name = Column(String(128), nullable=True)

    def set_pass(self, password):
        self.password = generate_password_hash(password)
