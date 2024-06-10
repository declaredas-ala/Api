# app/model/models.py
from sqlalchemy import Column, ForeignKey, Integer, String, TIMESTAMP, text
from sqlalchemy.dialects.mysql import TINYINT

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    phone = Column(String(20), nullable=False, unique=True)
    password = Column(String(200), nullable=False)
    is_admin = Column(TINYINT(1), nullable=False, server_default=text("'0'"))
    is_active = Column(TINYINT(1), nullable=False, server_default=text("'0'"))


class ApiCall(Base):
    __tablename__ = "api_calls"

    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey("users.id"), nullable=False, index=True)
    api_endpoint = Column(String(255), nullable=False)
    call_time = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    response_code = Column(Integer)
    response = Column(String(255))
    type = Column(String(10))
