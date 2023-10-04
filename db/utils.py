import datetime
import json

from sqlalchemy import Column, DateTime, delete as sqlalchemy_delete, update as sqlalchemy_update, Float, func
from sqlalchemy.future import select
from db import Base, db

db.init()


class AbstractClass:
    @staticmethod
    async def commit():
        try:
            await db.commit()
        except Exception:
            await db.rollback()
            raise

    @classmethod
    async def create(cls, **kwargs):
        object_ = cls(**kwargs)
        db.add(object_)
        await cls.commit()
        return object_

    @classmethod
    async def delete_all(cls):
        query = sqlalchemy_delete(cls)
        await db.execute(query)
        await cls.commit()
        return True

    @classmethod
    async def get_count(cls):
        query = select(func.count()).select_from(cls)
        count = await db.scalar(query)
        return count

    @classmethod
    async def get_all_chat_ids(cls):
        query = select(cls.chat_id)
        result = await db.execute(query)
        chat_ids = [row[0] for row in result]
        return chat_ids

    @classmethod
    async def update(cls, id_, **kwargs):
        query = (
            sqlalchemy_update(cls)
            .where(cls.id == id_)
            .values(**kwargs)
            .execution_options(synchronize_session="fetch")
        )
        await db.execute(query)
        await cls.commit()

    @classmethod
    async def update_by_user_id(cls, user_id, **kwargs):
        query = (
            sqlalchemy_update(cls)
            .where(cls.user_id == user_id)
            .values(**kwargs)
            .execution_options(synchronize_session="fetch")
        )
        await db.execute(query)
        await cls.commit()

    @classmethod
    async def update2(cls, chat_id, **kwargs):
        query = (
            sqlalchemy_update(cls)
            .where(cls.chat_id == chat_id)
            .values(**kwargs)
            .execution_options(synchronize_session="fetch")
        )
        await db.execute(query)
        await cls.commit()

    @classmethod
    async def get_by_chat_id(cls, chat_id):
        chat_id_str = str(chat_id)
        query = select(cls).where(cls.chat_id == chat_id_str)
        objects = await db.execute(query)
        object_ = objects.first()
        return object_

    @classmethod
    async def get_by_id(cls, id):
        chat_id_str = str(id)
        query = select(cls).where(cls.id == chat_id_str)
        objects = await db.execute(query)
        object_ = objects.first()
        return object_

    @classmethod
    async def get_by_pubg_id(cls, pubg_id):
        pubg_id_str = str(pubg_id)
        query = select(cls).where(cls.pubg_id == pubg_id_str)
        objects = await db.execute(query)
        object_ = objects.first()
        return object_

    @classmethod
    async def get_by_chat_id_str(cls, chat_id):
        query = select(cls).where(cls.chat_id == str(chat_id))
        objects = await db.execute(query)
        player = objects.first()
        return player

    @classmethod
    async def delete(cls):
        query = sqlalchemy_delete(cls)
        await db.execute(query)
        await cls.commit()
        return True

    @classmethod
    async def get_all(cls):
        query = select(cls)
        objects = await db.execute(query)
        return objects.all()


class CreatedModel(Base, AbstractClass):
    __abstract__ = True
    created_at = Column(DateTime(), default=datetime.datetime.utcnow)
    updated_at = Column(DateTime(), default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
