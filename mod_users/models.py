from sqlalchemy import Column, Integer, String
from app import db

from werkzeug.security import generate_password_hash ### for create password hash
from werkzeug.security import check_password_hash ### for check hash


# Role = 0 --> User
# Role = 1 --> Admin

class User(db.Model):
    __tablename__ = "users"
    id = Column(Integer, primary_key = True)
    email = Column(String(128), nullable=False, unique=True)
    password = Column(String(128), nullable=False)
    role = Column(Integer, nullable=False, default=0)
    full_name = Column(String(128), nullable=True)

    def set_pass(self, password):
        self.password = generate_password_hash(password)

    def check_pass(self, password):
        return check_password_hash(self.password, password) ### return a boolean 
    
    def is_admin(self):
        return self.role == 1