import asyncio

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart, Text

from bot.buttons.inline_buttons import payment_method
from bot.buttons.reply_buttons import main_menu_buttons, turnir_panel
from bot.buttons.text import info, statistics, turnir, balance, basic, pro, free, save, cancel, withdraw, magazine
from bot.dispatcher import dp, bot
from aiogram import types

from bot.handlers.admin_menu import main
from db.model import User, Players


@dp.message_handler(Text(magazine), state="menu")
async def magazine_handler(msg: types.Message, state: FSMContext):
    await msg.answer("Barcha akkauntlar shu kanalda 👉 https://t.me/ptb_savdo", )

