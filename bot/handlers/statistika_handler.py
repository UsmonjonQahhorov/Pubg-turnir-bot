import os

from aiogram import types
from aiogram.dispatcher import FSMContext

from aiogram.dispatcher.filters import CommandStart, Text
from aiogram.utils import callback_data
from bot.buttons.inline_buttons import payment_button, payment_method, fill_balance, agree_or_disagree, \
    with_balance
from bot.buttons.reply_buttons import main_menu_buttons, balance_panel
from bot.buttons.text import info, statistics, turnir, balance, fill, back_menu, uzcard, humo, hamyon, tether, payeer, \
    withdraw, agree, cancel, turnir_stat
from bot.dispatcher import dp, bot
from db.model import Players, Exchange_rate
import json
import pandas as pd


@dp.message_handler(Text(turnir_stat), state="admin_menu")
async def stat_handler(msg: types.Message, state: FSMContext):
    await msg.answer("Iltimos Exel fileni yuboring!!")
    await state.set_state("doc")


@dp.message_handler(state="doc", content_types=types.ContentType.DOCUMENT)
async def handle_document(message: types.Message, state: FSMContext):
    document = message.document
    if document.mime_type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
        await message.answer("Excel fayli qabul qilindi. Ushlab olinmoqda...")
        file_path = f"{document.file_id}.xlsx"  # Change the file path as needed
        await message.document.download(destination=file_path)
        df = pd.read_excel(file_path)
        user_ids = df["chat_id"].tolist()
        kills = df["Kill"].tolist()
        summas = df["summa"].tolist()
        for chat_id, kill, summa in zip(user_ids, kills, summas):
            print(f"User ID: {chat_id}, Kills: {kill}, Summa: {summa}")
            user_id_str = str(chat_id)
            print(user_id_str)
            try:
                player = await Players.get_by_chat_id(chat_id=user_id_str)
                if player[0].chat_id == user_id_str:
                    new_balance = player[0].balance + float(summa)
                    await Players.update2(user_id_str, balance=new_balance)
            except TypeError:
                print(f"Bunday chat_id li user topilmadi: {user_id_str}")
                text = (f"Balance toldirishda muammo bo'ldi❎\n"
                        f"Bunday chat_id li user topilmadi: {user_id_str}\n"
                        f"Kills: {kill}\n"
                        f"Summa: {summa}")
                await bot.send_message(chat_id=-1001834462254, text=text)

        os.remove(file_path)
        await message.answer("Ma'lumotlar muvaffaqiyatli o'qib olinib chiqarildi.")
        await message.answer(f"Balans muvaffaqiyatli yangilandi✅\n")
        await bot.send_file()
    else:
        await message.answer("Iltimos, Excel formatidagi faylni yuboring.")
    await state.finish()  # Holatni tugatish
