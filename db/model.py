from datetime import datetime

from sqlalchemy import Column, String, Sequence, Boolean, Integer, Float, DateTime
from db import db
from db.utils import CreatedModel

db.init()


class User(CreatedModel):
    __tablename__ = 'users'
    id = Column(Integer, Sequence("user_id_seq"), primary_key=True)
    chat_id = Column(String(30))
    fullname = Column(String(255))
    username = Column(String(255))


class Players(CreatedModel):
    __tablename__ = "players"
    id = Column(Integer, Sequence("user_id_seq"), primary_key=True)
    chat_id = Column(String(30))
    pubg_id = Column(String(100))
    phone_number = Column(String(50))
    email = Column(String(50))
    username = Column(String(255))
    tg_username = Column(String(80))
    name = Column(String(100))
    balance = Column(Float, default=0)


class Basic(CreatedModel):
    __tablename__ = "basic"
    id = Column(Integer, Sequence("user_id_seq"), primary_key=True)
    chat_id = Column(String(30))
    username = Column(String(255))
    tg_username = Column(String(80))
    name = Column(String(100))


class Pro(CreatedModel):
    __tablename__ = "pro"
    id = Column(Integer, Sequence("user_id_seq"), primary_key=True)
    chat_id = Column(String(30))
    username = Column(String(255))
    tg_username = Column(String(80))
    name = Column(String(100))


class Free(CreatedModel):
    __tablename__ = "free"
    id = Column(Integer, Sequence("user_id_seq"), primary_key=True)
    chat_id = Column(String(30))
    username = Column(String(255))
    tg_username = Column(String(80))
    name = Column(String(100))


class Total(CreatedModel):
    __tablename__ = "total"
    id = Column(Integer, Sequence("user_id_seq"), primary_key=True)
    chat_id = Column(String(30))
    username = Column(String(255))
    tg_username = Column(String(80))
    priority = Column(String(50))
    name = Column(String(100))


class Admins(CreatedModel):
    __tablename__ = "admins"
    id = Column(Integer, Sequence('admin_id_seq'), primary_key=True)
    chat_id = Column(String(40))
    username = Column(String(50))


class Exchange_rate(CreatedModel):
    __tablename__ = "exchange_rate"
    id = Column(Integer, Sequence('admin_id_seq'), primary_key=True)
    currency = Column(Float())
