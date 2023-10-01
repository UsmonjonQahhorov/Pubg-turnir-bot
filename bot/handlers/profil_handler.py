from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from bot.buttons.inline_buttons import profil_button, profile_update
from bot.buttons.text import profil, update, username, tg_username, pubg_id, phone_number

from bot.dispatcher import dp
from aiogram import types

from bot.handlers.start_handler import start_handler
from db.model import Players


@dp.message_handler(Text(profil), state="*")
async def profil_handler(msg: types.Message, state: FSMContext):
    chat_id = str(msg.from_user.id)
    me = await Players.get_by_chat_id(chat_id=chat_id)
    if me:
        await msg.answer(f"<b>Profil⚔\n\n"
                         f"PUBG_USERNAME👤: {me[0].username}\n"
                         f"TG_USERNAME📱: {me[0].tg_username}\n"
                         f"PUBG_ID🆔: {me[0].pubg_id}\n"
                         f"PHONE_NUMBER: {me[0].phone_number}\n"
                         f"NAME: {me[0].name}\n"
                         f"BALANCE🏦: {me[0].balance}"
                         f"</b>", parse_mode="HTML", reply_markup=await profil_button())
    else:
        await msg.answer(
            f"<b>Kechirasiz siz hali botda profil ochmagansiz😔</b>", parse_mode="HTML"
        )
    await state.set_state("update_profile")


@dp.callback_query_handler(lambda call: call.data.startswith(update), state="update_profile")
async def update_profile(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer("Quydagilardan ozgartirmoqchi bolganingizni tanlang👇",
                              reply_markup=await profile_update())
    await state.set_state("update_detail")


@dp.callback_query_handler(lambda call: call.data.startswith(username), state="update_detail")
async def update_username(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer("Ozgartirishni kiriting👇")
    await state.set_state("username_update")


@dp.message_handler(state="username_update")
async def username_update(msg: types.Message, state: FSMContext):
    updated_data = msg.text
    user_id = msg.from_user.id
    user_id_str = str(user_id)
    await Players.update2(user_id_str, username=updated_data)
    await msg.answer("Malumotlaringiz muafaqiyatli ozgartirildi👍", reply_markup=await start_handler(msg, state))


@dp.callback_query_handler(lambda call: call.data.startswith(tg_username), state="update_detail")
async def update_tgusername(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer("O'zgartirishni kiriting👇")
    await state.set_state("tgusername_update")


@dp.message_handler(state="tgusername_update")
async def tgusername_update(msg: types.Message, state: FSMContext):
    updated_data = msg.text
    user_id = msg.from_user.id
    user_id_str = str(user_id)
    await Players.update2(user_id_str, tg_username=updated_data)
    await msg.answer("Malumotlaringiz muafaqiyatli o'zgartirildi👍", reply_markup=await start_handler(msg, state))


@dp.callback_query_handler(lambda call: call.data.startswith(pubg_id), state="update_detail")
async def update_pubg_id(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer("O'zgartirishni kiriting👇")
    await state.set_state("pubg_id_update")


@dp.message_handler(state="pubg_id_update")
async def pubg_id_update(msg: types.Message, state: FSMContext):
    updated_data = msg.text
    user_id = msg.from_user.id
    user_id_str = str(user_id)
    await Players.update2(user_id_str, pubg_id=updated_data)
    await msg.answer("Malumotlaringiz muafaqiyatli o'zgartirildi👍", reply_markup=await start_handler(msg, state))


@dp.callback_query_handler(lambda call: call.data.startswith(phone_number), state="update_detail")
async def update_phone_number(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer("O'zgartirishni kiriting👇👇")
    await state.set_state("phone_number_update")


@dp.message_handler(state="phone_number_update")
async def phone_number_update(msg: types.Message, state: FSMContext):
    updated_data = msg.text
    user_id = msg.from_user.id
    user_id_str = str(user_id)
    await Players.update2(user_id_str, phone_number=updated_data)
    await msg.answer("Malumotlaringiz muafaqiyatli o'zgartirildi👍", reply_markup=await start_handler(msg, state))
