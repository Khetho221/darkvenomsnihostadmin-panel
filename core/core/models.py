from sqlalchemy import Column, String, Integer, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Admin(Base):
    __tablename__ = "admins"
    username = Column(String, primary_key=True)
    password_hash = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

class User(Base):
    __tablename__ = "users"
    username = Column(String, primary_key=True)
    daily_limit = Column(Integer, default=20)
    expires_at = Column(DateTime)
    status = Column(String, default="active")

class PassKey(Base):
    __tablename__ = "passkeys"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String)
    passkey_hash = Column(String)
    expires_at = Column(DateTime)
    used = Column(Boolean, default=False)
    used_at = Column(DateTime)
