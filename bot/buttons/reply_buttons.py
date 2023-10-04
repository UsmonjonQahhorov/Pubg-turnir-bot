from bot.buttons.text import info, back_menu, turnir, balance, statistics, fill, withdraw, basic, pro, back, free, \
    admin, statistika, add_admin, message, turnir_stat, manage_t, msg_basic, msg_free, msg_pro, habar, delete, msg_all, \
    admin_back, magazine, subscribe, donat, profil
from aiogram.types import ReplyKeyboardMarkup


async def main_menu_buttons():
    design = [
        [balance, donat],
        [turnir, magazine],
        [profil, admin],
    ]
    return ReplyKeyboardMarkup(keyboard=design, resize_keyboard=True)



async def balance_panel():
    design = [
        [fill, withdraw],
        [back_menu]
    ]
    return ReplyKeyboardMarkup(keyboard=design, resize_keyboard=True)


async def turnir_panel():
    design = [
        [basic, free, pro],
        [back_menu]
    ]
    return ReplyKeyboardMarkup(keyboard=design, resize_keyboard=True)


async def back_panel():
    design = [
        [back]
    ]
    return ReplyKeyboardMarkup(keyboard=design, resize_keyboard=True)

async def admin_panel():
    design = [
        [statistika, add_admin],
        [message, turnir_stat],
        [manage_t]
    ]
    return ReplyKeyboardMarkup(keyboard=design, resize_keyboard=True)


async def message_turnir():
    design = [
        [habar, delete]
    ]
    return ReplyKeyboardMarkup(keyboard=design, resize_keyboard=True)


async def manage_turnir():
    design = [
        [msg_basic, msg_pro],
        [msg_free, msg_all],
        [admin_back]
    ]
    return ReplyKeyboardMarkup(keyboard=design, resize_keyboard=True)
