import uuid

from sqlalchemy import Column, Boolean, JSON, Date, ForeignKey
from sqlalchemy.types import String
from sqlalchemy.orm import relationship

from fileshare.db import Base


class File(Base):
    __tablename__ = "files"
    id = Column(String(100), primary_key=True, unique=True)
    filename = Column(String(100), nullable = False)
    code = Column(String(100), nullable = False, index=True)
    created_on = Column(Date, nullable = False, index=True)
    expiry_date = Column(Date, nullable = False, index=True)
    is_deleted = Column(Boolean, index=True, default = False)
    is_auto_deleted = Column(Boolean, index=True, default = False)

    user_id = Column(ForeignKey("users.id"), index=True)