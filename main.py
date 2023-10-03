import asyncio
from aiogram.utils import executor
from aiofiles.threadpool.utils import cond_delegate_to_executor
from sqlalchemy.testing.plugin.plugin_base import logging
from bot.dispatcher import dp
from db import db, Base
# from sqlalchemy.util import asyncio
from bot.handlers import *
from db.model import User, Players, Admins, Basic, Pro, Free, Total
from middlewares import BigBrother


async def create_all():
    await db.create_all()


if __name__ == "__main__":
    dp.middleware.setup(BigBrother())
    db.init()
    # Players().create()
    # Basic().create()
    # Pro().create()
    # Free().create()
    # Exchange_rate().create()
    # Total().create()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(create_all())
    executor.start_polling(dp, skip_updates=True)
    logging.basicConfig(level=logging.INFO)
