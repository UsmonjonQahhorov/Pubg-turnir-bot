import json

from aiogram.dispatcher import FSMContext
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.buttons.text import payment, back, uzcard, humo, \
    hamyon, tether, payeer, fill, cancel, check_sub, begin, \
    subscribe, back_donat, tashladim, oson, update, username, \
    tg_username, pubg_id, phone_number, done, agree  # Make sure to import the text values for the buttons
from bot.handlers.prices import pubg_mobile_prices


async def payment_button():
    design = [
        [InlineKeyboardButton(text=payment, callback_data=payment)]
    ]
    return InlineKeyboardMarkup(inline_keyboard=design)


async def agree_donat_button():
    design = [
        [InlineKeyboardButton(text=agree, callback_data=agree)],
        [InlineKeyboardButton(text=cancel, callback_data=cancel)]
    ]
    return InlineKeyboardMarkup(inline_keyboard=design, row_width=2)


async def done_button():
    design = [
        [InlineKeyboardButton(text=done, callback_data=done)]
    ]
    return InlineKeyboardMarkup(inline_keyboard=design)


async def agree_button():
    design = [
        [InlineKeyboardButton(text=agree, callback_data=agree)]
    ]
    return InlineKeyboardMarkup(inline_keyboard=design)


async def payment_method():
    design = [
        [InlineKeyboardButton(text=uzcard, callback_data=uzcard)],
        [InlineKeyboardButton(text=humo, callback_data=humo)],
        [InlineKeyboardButton(text=hamyon, callback_data=hamyon)],
        [InlineKeyboardButton(text=payeer, callback_data=payeer)],
        [InlineKeyboardButton(text=oson, callback_data=oson)],
    ]
    return InlineKeyboardMarkup(inline_keyboard=design)


async def fill_balance(chat_id: str):
    # async with state.proxy() as data:
    #     photo = data["photo_file_id"]
    design = [
        [InlineKeyboardButton(text="To'ldirish✅", callback_data=f"fill:{chat_id}")],
        [InlineKeyboardButton(text="Bekor qilish❎", callback_data=f"reject:{chat_id}")]
    ]

    return InlineKeyboardMarkup(inline_keyboard=design)


async def donat_button(state: FSMContext, chat_id: int):
    async with state.proxy() as data:
        username = data["username"]
        tg_username = data["tg_username"]
        amount = data["donat_amount"]
        id = data["id"]
        design = [
            [InlineKeyboardButton(text="To'ldirdim☑", callback_data=f"donat:{chat_id}: {username}:{tg_username}"
                                                                    f":{amount}:{id}")],
            [InlineKeyboardButton(text="Bekor qilish❎", callback_data=f"reject:{chat_id}")]
        ]

    return InlineKeyboardMarkup(inline_keyboard=design)


async def agree_or_dis(chat_id: str):
    design = [
        [InlineKeyboardButton(text="Ruxsat✅", callback_data=f"Ruxsat:{chat_id}")],
        [InlineKeyboardButton(text="Bekor qilish❎", callback_data=f"bekor qilish:{chat_id}")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=design)


async def agree_or_dis2(chat_id: str):
    design = [
        [InlineKeyboardButton(text="Ruxsat✅", callback_data=f"Baruxsat:{chat_id}")],
        [InlineKeyboardButton(text="Bekor qilish❎", callback_data=f"5bekor qilish:{chat_id}")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=design)


async def agree_or_dis3(chat_id: str):
    design = [
        [InlineKeyboardButton(text="Ruxsat✅", callback_data=f"3Ruxsat:{chat_id}")],
        [InlineKeyboardButton(text="Bekor qilish❎", callback_data=f"3bekor qilish:{chat_id}")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=design)


async def agree_or_dis_free(chat_id: str):
    design = [
        [InlineKeyboardButton(text="Ruxsat✅", callback_data=f"sukamisan:{chat_id}")],
        [InlineKeyboardButton(text="Bekor qilish❎", callback_data=f"pasholnax:{chat_id}")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=design)


#
# async def fill_balance(chat_id: str):
#     design = [
#         [InlineKeyboardButton(text=fill, callback_data=chat_id)],
#         [InlineKeyboardButton(text=cancel, callback_data=chat_id)]
#     ]
#     return InlineKeyboardMarkup(inline_keyboard=design)


async def agree_or_disagree():
    design = [
        [InlineKeyboardButton(text=agree, callback_data=agree)],
        [InlineKeyboardButton(text=cancel, callback_data=cancel)]
    ]
    return InlineKeyboardMarkup(inline_keyboard=design)


async def check_button():
    design = [
        [InlineKeyboardButton(text=check_sub, callback_data="check_sub")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=design)


async def turnir_basic_begin():
    design = [
        [InlineKeyboardButton(text=begin, callback_data="begin")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=design)


async def turnir_pro_begin():
    design = [
        [InlineKeyboardButton(text=begin, callback_data="probegin")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=design)


async def turnir_free_begin():
    design = [
        [InlineKeyboardButton(text=begin, callback_data="freebegin")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=design)


channel_usernames = ['pubg_turner_news', "pythondevsof"]


async def member_buttons():
    design = []
    for i in channel_usernames:
        subscribe_button = InlineKeyboardButton(
            "Obuna bolish✅", url=f"https://t.me/{i}"
        )

        design.append([subscribe_button])

    return InlineKeyboardMarkup(inline_keyboard=design)


async def pubg_prices_buttons():
    design = []
    for i in pubg_mobile_prices:
        for i in i.items():
            key = f"{i[0]} -> {i[1]}"
            value = i[0]
        design.append([InlineKeyboardButton(text=key, callback_data=value)])
    return InlineKeyboardMarkup(inline_keyboard=design, resize_keyboard=True)


async def messangers():
    design = [
        [InlineKeyboardButton(text="Google", callback_data="Google"),
         InlineKeyboardButton(text="Facebook", callback_data="Facebook")],
        [InlineKeyboardButton(text="Wk", callback_data="Wk"),
         InlineKeyboardButton(text='Twitter', callback_data="Twitter")],
        [InlineKeyboardButton(text="Telefon raqam", callback_data="Telefon raqam")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=design)


async def yes_or_no_users():
    design = [
        [InlineKeyboardButton(text=tashladim, callback_data=tashladim),
         InlineKeyboardButton(text=back_donat, callback_data=back_donat)]
    ]
    return InlineKeyboardMarkup(inline_keyboard=design)


async def with_balance(state: FSMContext, user_id: str):
    async with state.proxy() as data:
        summa = data["summa"]
    design = [
        [InlineKeyboardButton(text="To'ldirdim✅", callback_data=f"toldirishda|{user_id}:{summa}")],
        [InlineKeyboardButton(text="Bekor qilish❎", callback_data=f"2bek:{user_id}")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=design)


# async def add_sub_food_button(state: FSMContext, product: json):
#     design = [
#         [InlineKeyboardButton(text="➖", callback_data=f"{state}: {product}"),
#          InlineKeyboardButton(text=f"{[2]}", callback_data=f"save_{[2]}"),
#          InlineKeyboardButton(text="➕", callback_data=f"+_{product['name']}")],
#         [InlineKeyboardButton(text="Savatdan o'chirish 🛒", callback_data='del')]
#     ]
#     return InlineKeyboardMarkup(inline_keyboard=design)

async def profil_button():
    design = [
        [InlineKeyboardButton(text=update, callback_data=update)]]
    return InlineKeyboardMarkup(inline_keyboard=design)


async def profile_update():
    design = [
        [InlineKeyboardButton(text=username, callback_data=username),
         InlineKeyboardButton(text=tg_username, callback_data=tg_username)],
        [InlineKeyboardButton(text=pubg_id, callback_data=pubg_id),
         InlineKeyboardButton(text=phone_number, callback_data=phone_number)],
    ]
    return InlineKeyboardMarkup(inline_keyboard=design)
