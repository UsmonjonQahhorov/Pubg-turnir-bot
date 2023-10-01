import json
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart, Text
from bot.buttons.inline_buttons import payment_method, with_balance
from bot.buttons.reply_buttons import main_menu_buttons, turnir_panel
from bot.buttons.text import info, statistics, turnir, balance, basic, pro, free, save, cancel, withdraw
from bot.dispatcher import dp, bot
from aiogram import types
from bot.handlers.admin_menu import main
from db.model import User, Players

JSON_FILE = 'dollar_currency'


def load_json_data():
    try:
        with open(JSON_FILE, 'r') as json_file:
            return json.load(json_file)
    except FileNotFoundError:
        return {"dollar_cur": 12000}


def save_json_data(data):
    with open(JSON_FILE, 'w') as json_file:
        json.dump(data, json_file, indent=4)


@dp.message_handler(commands=['update_dollar'], state="*")
async def update_dollar_cur(message: types.Message):
    try:
        new_dollar_cur = float(message.get_args())
        json_data = load_json_data()
        json_data["dollar_cur"] = new_dollar_cur
        save_json_data(json_data)
        await message.reply(f"Dollar kursi yangilandi: {new_dollar_cur}")
    except ValueError:
        await message.reply("Noto'g'ri qiymat. Yangi dollar kursini son bilan yuboring.")


@dp.message_handler(commands=['update_withdraw'], state="*")
async def update_dollar_cur(message: types.Message):
    try:
        new_dollar_cur = float(message.get_args())
        json_data = load_json_data()
        json_data["dollar_withdraw"] = new_dollar_cur
        save_json_data(json_data)
        await message.reply(f"Dollar kursi yangilandi: {new_dollar_cur}")
    except ValueError:
        await message.reply("Noto'g'ri qiymat. Yangi dollar kursini son bilan yuboring.")
