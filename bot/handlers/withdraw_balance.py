import json

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart, Text

from bot.buttons.inline_buttons import payment_method, with_balance
from bot.buttons.reply_buttons import main_menu_buttons, turnir_panel
from bot.buttons.text import info, statistics, turnir, balance, basic, pro, free, save, cancel, withdraw
from bot.dispatcher import dp, bot
from aiogram import types


def load_json_data():
    with open('dollar_currency', 'r') as json_file:
        json_data = json.load(json_file)
    return json_data


# def load_json_data_with():
#     with open('dollar_currency_with', 'r') as json_file:
#         json_data = json.load(json_file)
#     return json_data


@dp.message_handler(Text([withdraw]), state="balance")
async def withdraw_handler(msg: types.Message, state: FSMContext):
    await msg.answer(
        text="<b>Balansingizdan minimal pull yechib olish miqdori 30$, Pull yechib olish usulini tanlang👇 </b>",
        parse_mode='HTML', reply_markup=await payment_method())
    await state.set_state("summa_request")
