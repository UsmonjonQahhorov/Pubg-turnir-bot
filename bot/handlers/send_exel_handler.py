from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart, Text
from aiogram.types import InputFile

# from bot.buttons.inline_buttons import agree_button
from bot.buttons.reply_buttons import main_menu_buttons, turnir_panel
from bot.buttons.text import info, statistics, turnir, balance, basic, pro, free, save, cancel, agree
from bot.dispatcher import dp, bot
from aiogram import types
import asyncio
from bot.buttons.inline_buttons import agree_button, agree_or_dis, agree_or_dis2, agree_or_dis3
# from .admin_menu import admins
from db.model import User, Players, Basic, Free, Pro, Total, Admins
import pandas as pd


@dp.callback_query_handler(lambda call: call.data.startswith("beg"))
async def free_handler(call: types.CallbackQuery, state: FSMContext):
    data_from_database = await Basic.get_all()
    chat_ids = [data_from_database[record][0].chat_id for record in range(len(data_from_database))]
    usernames = [data_from_database[record][0].username for record in range(len(data_from_database))]
    tg_username = [data_from_database[record][0].tg_username for record in range(len(data_from_database))]
    name = [data_from_database[record][0].name for record in range(len(data_from_database))]

    data_dict = {
        "chat_id": chat_ids,
        "Username": usernames,
        "tg_username": tg_username,
        "name": name,
        "Kill": "",
        "summa": ""
    }

    df = pd.DataFrame(data_dict)

    excel_file = "basic.xlsx"
    excel_writer = pd.ExcelWriter(excel_file, engine="openpyxl")

    df.to_excel(excel_writer, index=False, sheet_name="Sheet1")

    excel_writer._save()
    with open(excel_file, "rb") as f:
        input_file = InputFile(f)
        await bot.send_document(chat_id=-1001834462254, document=input_file, caption="Bu oyinchilar royhati"
                                                                                     " turnirdan song uni bo'sh "
                                                                                     "ustunlarini to'ldirib qayta"
                                                                                     " jonating botga")

    print(f"Data written to {excel_file}")


@dp.callback_query_handler(lambda call: call.data.startswith("probeg"))
async def free_handler(call: types.CallbackQuery, state: FSMContext):
    data_from_database = await Pro.get_all()
    chat_ids = [data_from_database[record][0].chat_id for record in range(len(data_from_database))]
    usernames = [data_from_database[record][0].username for record in range(len(data_from_database))]
    tg_username = [data_from_database[record][0].tg_username for record in range(len(data_from_database))]
    name = [data_from_database[record][0].name for record in range(len(data_from_database))]

    data_dict = {
        "chat_id": chat_ids,
        "Username": usernames,
        "tg_username": tg_username,
        "name": name,
        "Kill": "",
        "summa": ""
    }

    df = pd.DataFrame(data_dict)

    excel_file = "pro.xlsx"
    excel_writer = pd.ExcelWriter(excel_file, engine="openpyxl")

    df.to_excel(excel_writer, index=False, sheet_name="Sheet1")

    excel_writer._save()
    with open(excel_file, "rb") as f:
        input_file = InputFile(f)
        await bot.send_document(chat_id=-1001834462254, document=input_file, caption="Bu oyinchilar royhati"
                                                                                     " turnirdan song uni bo'sh "
                                                                                     "ustunlarini to'ldirib qayta"
                                                                                     " jonating botga")

    print(f"Data written to {excel_file}")


@dp.callback_query_handler(lambda call: call.data.startswith("freebegin"))
async def free_handler(call: types.CallbackQuery, state: FSMContext):
    data_from_database = await Free.get_all()
    chat_ids = [data_from_database[record][0].chat_id for record in range(len(data_from_database))]
    usernames = [data_from_database[record][0].username for record in range(len(data_from_database))]
    tg_username = [data_from_database[record][0].tg_username for record in range(len(data_from_database))]
    name = [data_from_database[record][0].name for record in range(len(data_from_database))]

    data_dict = {
        "chat_id": chat_ids,
        "Username": usernames,
        "tg_username": tg_username,
        "name": name,
        "Kill": "",
        "summa": ""
    }

    df = pd.DataFrame(data_dict)

    excel_file = "free.xlsx"
    excel_writer = pd.ExcelWriter(excel_file, engine="openpyxl")

    df.to_excel(excel_writer, index=False, sheet_name="Sheet1")

    excel_writer._save()
    with open(excel_file, "rb") as f:
        input_file = InputFile(f)
        await bot.send_document(chat_id=-1001834462254, document=input_file, caption="Bu oyinchilar royhati"
                                                                                     "turnirdan song uni botga jonatishga hojat yoq")

    print(f"Data written to {excel_file}")
