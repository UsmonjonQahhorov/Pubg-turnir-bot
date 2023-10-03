import asyncio

from aiogram import types
from aiogram.dispatcher import FSMContext

from aiogram.dispatcher.filters import CommandStart, Text
from aiogram.utils import callback_data

from bot.buttons.inline_buttons import payment_button, payment_method, fill_balance, agree_or_disagree, \
    with_balance
from bot.buttons.reply_buttons import main_menu_buttons, balance_panel
from bot.buttons.text import info, statistics, turnir, balance, fill, back_menu, uzcard, humo, hamyon, tether, payeer, \
    withdraw, agree, cancel, oson
from bot.dispatcher import dp, bot
from bot.handlers.withdraw_balance import load_json_data
# from bot.handlers.withdraw_balance import json_data
from db.model import Players, Admins
import json


# from .admin_menu import admins


async def main():
    admins = await Admins.get_all_chat_ids()
    return admins


@dp.message_handler(Text([balance]), state="menu")
async def balance_menu_handler(msg: types.Message, state: FSMContext):
    chat_id = msg.from_user.id
    chat_id_str = str(chat_id)
    player = await Players.get_by_chat_id(chat_id=chat_id_str)
    # print(player)
    if player:
        await msg.answer(text="Balance Menu", reply_markup=await balance_panel())
        await state.set_state("balance")
    else:
        await msg.answer(f"<b> Siz hali ro'yxatdan o'tmagansiz iltimos turnir bo'limida ro'yhatdan o'ting‼</b>",
                         parse_mode="HTML")


@dp.message_handler(state='balance')
async def balance_menu_handler(msg: types.Message, state: FSMContext):
    json_data = load_json_data()
    dollar_cur_value = json_data["dollar_cur"]
    await msg.answer(f"<b>Qanchaga to'ldirmoqchisiz📥\n\n"
                     f"💳 Summani dollar$ hisobida kiriting❗\n"
                     f"💱 Valyuta kursi 1💲 ♻️{dollar_cur_value} UZS\n"
                     f"💳 Minimal Pul kiritish 5💲</b>", parse_mode="HTML")
    await state.set_state("req_card")


@dp.message_handler(state="req_card")
async def fill_handler(msg: types.Message, state: FSMContext):
    try:
        summa = float(msg.text)
    except ValueError:
        await msg.answer("Notogri summa kirgizdingiz! Summani raqam shaklida kiriting.")
        return  # Return to the previous state without setting a new state

    if summa < 5:  # Check if summa is less than the minimum allowed amount
        await msg.answer("Minimal Pul kiritish 5$.")
    else:
        json_data = load_json_data()
        dollar_cur_value = float(json_data["dollar_cur"])
        async with state.proxy() as data:
            data["entered_summa"] = msg.text
        real_s = dollar_cur_value * int(msg.text)
        await msg.answer(
            f"<b>Siz o'z balansingizni  {msg.text}$ ga to'ldirmoqchisiz\n"
            f"💵Balansni to'ldirish uchun ushbu 💳 Kartalardan birini tanlang va pull otkazing\n"
            f"Otkizishingiz kerak bolgan summa: {real_s} Uzbek somi\n\n"
            f"⚠️Chekni botga jonating!!</b>",
            parse_mode='HTML', reply_markup=await payment_method())
        await state.set_state("payment")


@dp.callback_query_handler(Text([uzcard, humo, hamyon, payeer, oson]), state="payment")
async def money_google_handler(call: types.CallbackQuery, state: FSMContext):
    card_name = call.data
    card_number = (
        "8600140480026229 Allayorov Xayitboy" if card_name == uzcard else
        "9860106624418237 Allayorov Xayitboy" if card_name == humo else
        "+998943137825" if card_name == hamyon or card_name == oson else
        "P66585992"

    )
    await call.message.answer(f"{card_name} {card_number}", reply_markup=await payment_button())
    await state.set_state("chek")
    await call.message.delete()


@dp.callback_query_handler(state='chek')
async def chek_handler(call: types.CallbackQuery, state: FSMContext):
    user_id = call.from_user.id
    async with state.proxy() as data:
        data["user_id"] = user_id
    await call.message.answer(text="<b> Chekni jonating📨</b>", parse_mode='HTML')
    await state.set_state("chek1")


photo_file_id = ""


@dp.message_handler(content_types=types.ContentType.PHOTO, state="chek1")
async def handle_photo(message: types.Message, state: FSMContext):
    try:
        global photo_file_id
        photo_file_id = message.photo[-1].file_id
        json_data = load_json_data()
        dollar_cur_value = float(json_data["dollar_cur"])
        photo = await bot.get_file(photo_file_id)
        async with state.proxy() as data:
            if photo:
                admins_royxati = await main()
                print(data)
                for i in admins_royxati:
                    caption_text = (
                        f"👤Balance to'ldirish uchun yangi so'rov\n 📄Chekni tekshiring‼️\n\n🆔ID: {message.from_user.id}\n"
                        f"📝Ism-Familia: {message.from_user.full_name}\n©️Username: @{message.from_user.username}\n"
                        f"User o'z hisobiga {data['entered_summa']}$ || {dollar_cur_value * int(data['entered_summa'])} somga to'ldirmoqchi")
                    await message.bot.send_photo(chat_id=i, photo=photo.file_id,
                                                 reply_markup=await fill_balance(data["user_id"]),
                                                 caption=caption_text)
            else:
                print("Photo file ID is missing in data.")
    except Exception as e:
        print(f"Error in chek3_handler: {e}")


# @dp.callback_query_handler(lambda call: call.data.startswith("fill"), state='*')
# async def chek3_handler(call: types.CallbackQuery, state: FSMContext):
#     try:
#         global photo_file_id
#         json_data = load_json_data()
#         dollar_cur_value = float(json_data["dollar_cur"])
#         photo = await bot.get_file(photo_file_id)
#         async with state.proxy() as data:
#             if photo:
#                 admins_royxati = await main()
#                 print(data)
#                 for i in admins_royxati:
#                     caption_text = (
#                         f"👤Balance to'ldirish uchun yangi so'rov\n 📄Chekni tekshiring‼️\n\n🆔ID: {call.from_user.id}\n"
#                         f"📝Ism-Familia: {call.from_user.full_name}\n©️Username: @{call.from_user.username}\n"
#                         f"User o'z hisobiga {data['entered_summa']}$ || {dollar_cur_value * int(data['entered_summa'])} somga to'ldirmoqchi")
#                     await call.bot.send_photo(chat_id=i, photo=photo.file_id,
#                                               reply_markup=await fill_balance(data["user_id"]),
#                                               caption=caption_text)
#             else:
#                 print("Photo file ID is missing in data.")
#     except Exception as e:
#         print(f"Error in chek3_handler: {e}")


@dp.callback_query_handler(lambda call: call.data.startswith("reject"), state="*")
async def what_delete_handler(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    chat_id = call.data.split(":")[1]
    print(f"chat id 374:{chat_id}")
    async with state.proxy() as data:
        data["chat_id"] = chat_id
    await state.set_state("why_reject")
    await call.message.answer(text="Nima uchun bekor qildingiz❓\n\nIzoh yozish majburiy❗️")


@dp.message_handler(state='why_reject')
async def not_save_handler(msg: types.Message, state: FSMContext):
    try:
        await bot.delete_message(msg.from_user.id, msg.message_id - 1)
    except:
        pass
    async with state.proxy() as data:
        chat_id = data["chat_id"]
    await bot.send_message(chat_id=chat_id,
                           text=f"<b>Sizning sorovingiz bekor qilindi❗️\nAdmin izohi: {msg.text}\n\nMurojat uchun: https://t.me/Pubg_turner_bot</b>",
                           parse_mode="HTMl")


@dp.callback_query_handler(lambda call: call.data.startswith("fill"), state="*")
async def handle_fill_callback(call: types.CallbackQuery, state: FSMContext):
    chat_id = call.data.split(":")[1]
    print(chat_id)
    print(call.data)

    async with state.proxy() as data:
        data["chat_id"] = chat_id
    msg = await call.message.answer(f"<b>💰Balanseni qanchaga to'ldirmoqchisiz iltimos kiriting👇</b>", parse_mode="HTML")
    await state.set_state("fill_req")


@dp.message_handler(state="fill_req")
async def process_channel_text(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        summa = message.text
        data["summa"] = float(summa)
        summa = message.text
        await message.answer(
            f"<b>Siz to'ldirmoqchi bo'lgan summa {summa}$\nBalansni to'ldirishni hohlaysizmi</b>",
            reply_markup=await agree_or_disagree(), parse_mode="HTML")
    await state.set_state("req_agree")


@dp.callback_query_handler(lambda call: call.data.startswith(agree), state="req_agree")
async def update_balance(call: types.CallbackQuery, state: FSMContext):
    try:
        await bot.delete_message(call.from_user.id, call.message.message_id - 1)
    except:
        pass
    async with state.proxy() as data:
        chat_id = data["chat_id"]
        # photo_file_id = data["photo_file_id"]
        summa = data.get("summa")
        print(data)
    user_id_str = str(chat_id)

    player = await Players.get_by_chat_id(chat_id=user_id_str)
    if player:
        player = player[0]
        new_balance = player.balance + float(summa)
        await Players.update2(user_id_str, balance=new_balance)

        msg_text = (f"<b>User balansi to'ldirildi✅\n"
                    f"PUBG_ID🆔: {player.pubg_id}\n"
                    f"PHONE_NUM📱{player.phone_number}\n"
                    f"E-MAIL📧: {player.email}\n"
                    f"USERNAME: {player.username}\n"
                    f"TG_USERNAME📱:{player.tg_username}\n"
                    f"ISM: {player.name}\n"
                    f"BALANCE💰: {new_balance}</b>")

        await bot.send_photo(chat_id=-1001858175397, photo=photo_file_id, caption=msg_text, parse_mode="HTML")
        await bot.send_message(chat_id, text=f"Sizning balancingiz {summa}$ ga toldirildi✅\n"
                                             f"Hozirgi balance {new_balance}$")
        await state.finish()
    else:
        await call.message.answer(f"<b>Bunday user topilmadi😔</b>", parse_mode="HTML")


@dp.callback_query_handler(Text(cancel))
async def update_balance(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer(
        text=f"<b>{call.from_user.full_name} asosiy bo'limdasiz✅\n\nBo'limlardan birini tanlang⬇️</b>",
        reply_markup=await main_menu_buttons(), parse_mode='HTML')
    await state.finish()


@dp.message_handler(state="send_admin")
async def send_admin_handler(message: types.Message, state: FSMContext):
    await message.answer("So'rovingiz adminga yetkazildi\nAdmin javobini kuting‼")


@dp.message_handler(Text(back_menu), state='*')
async def back_handler(msg: types.Message, state: FSMContext):
    await msg.delete()
    await msg.answer(text=f"<b>{msg.from_user.full_name} asosiy bo'limdasiz✅\n\nBo'limlardan birini tanlang⬇️</b>",
                     reply_markup=await main_menu_buttons(), parse_mode='HTML')
    # await state.finish()


"""Yechish"""
