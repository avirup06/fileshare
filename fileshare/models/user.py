import uuid

from sqlalchemy import Column, Boolean, JSON
from sqlalchemy.types import String
from sqlalchemy.orm import relationship

from fileshare.db import Base


class User(Base):
    __tablename__ = "users"
    id = Column(String(100), primary_key=True, unique=True)
    first_name = Column(String(100), nullable = False)
    last_name = Column(String(100), nullable = False)
    username = Column(String(100), unique=True, nullable = False)
    salt = Column(String(100), nullable = False)
    password_hash = Column(String(100), nullable = False)

    files = relationship("File", backref="users", lazy='joined')