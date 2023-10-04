from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from bot.buttons.inline_buttons import pubg_prices_buttons, agree_donat_button, yes_or_no_users, donat_button
from bot.buttons.reply_buttons import main_menu_buttons, back_panel
from bot.buttons.text import donat, back, agree, cancel, \
    tashladim, back_donat
from bot.dispatcher import dp, bot
from bot.handlers.admin_menu import main


@dp.callback_query_handler(Text(cancel), state="agree_donat")
async def agree_donat(call: types.CallbackQuery, state: FSMContext):
    try:
        await bot.delete_message(call.from_user.id, call.message.message_id - 1)
    except:
        pass
    await call.message.answer(
        text=f"<b>{call.from_user.full_name} asosiy bo'limdasiz✅\n\nBo'limlardan birini tanlang⬇️</b>",
        reply_markup=await main_menu_buttons(), parse_mode='HTML')
    await state.set_state('menu')


@dp.message_handler(Text(back), state='*')
async def back_handler(msg: types.Message, state: FSMContext):
    try:
        await bot.delete_message(msg.from_user.id, msg.message_id - 1)
    except:
        pass
    await msg.delete()
    await msg.answer(
        text=f"<b>{msg.from_user.full_name} asosiy bo'limdasiz✅\n\nBo'limlardan birini tanlang⬇️</b>",
        reply_markup=await main_menu_buttons(), parse_mode='HTML')
    await state.set_state('menu')


@dp.message_handler(Text([donat]), state="menu")
async def enter_game_handler(msg: types.Message, state: FSMContext):
    try:
        await bot.delete_message(msg.from_user.id, msg.message_id - 1)
    except:
        pass
    await msg.answer(text="<b>O`zingizga kerakli narxni tanlang⬇️</b>", parse_mode="HTML",
                     reply_markup=await back_panel())
    await msg.answer_photo(photo=open("images/gold-bars-pubg.jpg", "rb"),
                           reply_markup=await pubg_prices_buttons())
    await state.set_state("donat_amount")


@dp.callback_query_handler(state="donat_amount")
async def donat_handler(call: types.CallbackQuery, state: FSMContext):
    try:
        await bot.delete_message(call.from_user.id, call.message.message_id - 1)
    except:
        pass
    donat_amount = call.data
    async with state.proxy() as data:
        data["donat_amount"] = donat_amount
    await call.message.answer("<i>Sizga arzon narxlarda ID orqali donat qilib beriladi✅ Rozimisiz❓</i>",
                              reply_markup=await agree_donat_button(), parse_mode="HTML")
    await state.set_state("agree_donat")


@dp.callback_query_handler(lambda call: call.data.startswith(agree), state="agree_donat")
async def choose_donat(call: types.CallbackQuery, state: FSMContext):
    try:
        await bot.delete_message(call.from_user.id, call.message.message_id - 1)
    except:
        pass
    await call.message.answer("ID yingizni jonating📨")
    await state.set_state("id_donat")


@dp.message_handler(state="id_donat")
async def username_handler(msg: types.Message, state: FSMContext):
    email = msg.text
    async with state.proxy() as data:
        data["id"] = email
    await msg.answer("Pubg usernameyingizni kiriting")
    await state.set_state("username_donat")


@dp.message_handler(state="username_donat")
async def password_handler(message: types.Message, state: FSMContext):
    try:
        await bot.delete_message(message.from_user.id, message.message_id - 1)
    except:
        pass
    username = message.text
    async with state.proxy() as data:
        data["username"] = username
        p_id = data["id"]
    caption = f"""<b>💰To'lovni quyidagi usullar orqali amalga oshirishingiz mumkin.✅
        UZCARD: 8600140480026229💳
        HUMO: 9860106624418237💳
        OSON: +998943137825
        KIWI_UZ: +998943137825
        PAYEER: P66585992
        👤Karta: Allayorov Xayitboy  nomida✅
        ID: {p_id}
        USERNAME: {username}
        👨‍💻Toʻloʻv qilishda muammo boʻlsa: https://T.me/Pubg_turner_bot
        🧾toʻloʻv cheki boʻlishi shart‼️\n\nTo'lo'v qildingizmi❓</b>"""

    reply_markup = await yes_or_no_users()

    await message.answer(caption, parse_mode="HTML", reply_markup=reply_markup)
    await state.set_state("google_photo")


@dp.callback_query_handler(Text([tashladim, back_donat]), state='google_photo')
async def yes_or_no_users_handler(call: types.CallbackQuery, state: FSMContext):
    user_id = call.from_user.id
    async with state.proxy() as data:
        data["user_id"] = user_id
        print(data['user_id'])
    try:
        await bot.delete_message(call.from_user.id, call.message.message_id - 1)
    except:
        pass
    await call.message.delete()
    if call.data == tashladim:
        await state.set_state("chek_photo")
        await call.message.answer(text="<b>Chek rasmini jo`nating🖼</b>", parse_mode="HTML",
                                  reply_markup=await main_menu_buttons())
    else:
        await call.message.answer(
            text=f"<b>{call.from_user.full_name} asosiy bo'limdasiz✅\n\nBo'limlardan birini tanlang⬇️</b>",
            parse_mode="HTML",
            reply_markup=await main_menu_buttons())
    await state.set_state("donat_chek")


@dp.message_handler(content_types=types.ContentType.PHOTO, state="donat_chek")
async def handle_photo(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    try:
        await bot.delete_message(message.from_user.id, message.message_id - 1)
    except:
        pass
    photo_file_id = message.photo[-1].file_id
    admins_royxati = await main()
    for i in admins_royxati:
        async with state.proxy() as data:
            donat_amount = data["donat_amount"]
            data["tg_username"] = message.from_user.username
            data["photo_id"] = photo_file_id
        caption = (f"🆕Yangi buyurtma☑\n\n"
                   f"🛒Miqdor: {donat_amount}\n"
                   f"ID: {data['id']}\n"
                   f"USERNAME: {data['username']}\n"
                   f"Username telegram: @{message.from_user.username}\n"
                   f"Donat UC: {data['donat_amount']}")
        await message.bot.send_photo(chat_id=i, caption=caption, parse_mode="HTML", photo=photo_file_id,
                                     reply_markup=await donat_button(state, chat_id=user_id))
        await state.set_state("google_state")


@dp.callback_query_handler(lambda call: call.data.startswith("donat"), state="*")
async def handle_fill_callback(call: types.CallbackQuery, state: FSMContext):
    try:
        await bot.delete_message(call.from_user.id, call.message.message_id - 1)
    except:
        pass
    list_ = call.data.split(":")
    print(list_)
    user_id = call.data.split(":")[1]

    await bot.send_message(chat_id=user_id, text=f"<i>Sizga muafaqiyatli donat qilib berildi👌</i>\n"
                                                 f"Siz bilan ishlaganimizdan minnatdormiz😉",
                           parse_mode="HTML")
    await bot.send_message(chat_id=-1001858175397, text=f"<i>Donat bajarildi</i>\n\n"
                                                        f"Username: {list_[2]}\n"
                                                        f"TG_Username: {list_[3]}\n"
                                                        f"Donat miqdori: {list_[4]}\n",
                           parse_mode="HTML")
    await call.message.delete()
