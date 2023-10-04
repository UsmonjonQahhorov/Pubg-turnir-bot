import json
from aiogram.dispatcher import FSMContext
from aiohttp.abc import HTTPException

from bot.buttons.inline_buttons import with_balance
from bot.dispatcher import dp, bot
from aiogram import types
from bot.buttons.text import uzcard, humo, hamyon, payeer, oson
from bot.handlers.admin_menu import main
from db.model import Players


def load_json_data():
    with open('dollar_currency', 'r') as json_file:
        json_data = json.load(json_file)
    return json_data


@dp.callback_query_handler(lambda call: call.data in [uzcard, humo, hamyon, payeer, oson], state="summa_request")
async def withdraw_method_handler(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        data["method"] = call.data
    user_id = call.from_user.id
    user_id_str = str(user_id)
    player = await Players.get_by_chat_id(chat_id=user_id_str)
    json_data = load_json_data()
    dollar_cur = int(json_data["dollar_withdraw"])
    await call.message.answer(f"<b>Qancha yechmoqchiligingizni kiriting👇\n\n"
                              f"Sizning balansingizda {player[0].balance}$ pull bor\n"
                              f"💱 Valyuta kursi 1$: ♻️ {dollar_cur} UZS\n"
                              f"💳 Minimal Pul kiritish 30$</b>", parse_mode="HTML")
    await call.message.delete()
    await state.set_state("card_req")


@dp.message_handler(state="card_req")
async def withdraw_method_handler(msg: types.Message, state: FSMContext):
    try:
        summa = float(msg.text)
    except ValueError:
        await msg.answer("Notogri summa kirgizdingiz! Summani raqam shaklida kiriting.")
        return

    if summa < 30:
        await msg.answer("Minimal Pul kiritish 30$ yoki balansingizda mablag' yetarli emas!")
    else:
        await msg.answer("Karta raqamingizni jo'nating👇")
        async with state.proxy() as data:
            data["summa"] = summa
            data["summa_with"] = summa
            print(f"data57:{data}")
        await state.set_state("send_to_with")


@dp.message_handler(state="send_to_with")
async def back_handler(msg: types.Message, state: FSMContext):
    try:
        await bot.delete_message(msg.from_user.id, msg.message_id - 1)
    except:
        pass
    json_data = load_json_data()
    card_num = msg.text
    dollar_cur_value = json_data["dollar_withdraw"]
    async with state.proxy() as data:
        user_id = msg.from_user.id
        user_id_str = str(user_id)
        data["chat_id_w"] = user_id
        player = await Players.get_by_chat_id(chat_id=user_id_str)
        if data["method"] == uzcard:
            prosent = (float(data["summa"]) / 100) * 0.5
            cur_balance = float(data["summa"]) - prosent
            summ = cur_balance * dollar_cur_value

            admins_royxati = await main()
            for i in admins_royxati:
                msg_text = (f"<b>Pull yechib olish uchun yangi so'rov‼\n\n"
                            f"CHAT_ID🆔: {player[0].chat_id}\n"
                            f"PUBG_ID🆔: {player[0].pubg_id}\n"
                            f"USERNAME: {player[0].username}\n"
                            f"PHONE_NUM📱: {player[0].phone_number}\n"
                            f"E-MAIL📧: {player[0].email}\n"
                            f"TG_USERNAME📱:{player[0].tg_username}\n"
                            f"ISM: {player[0].name}\n"
                            f"BALANCE💰: {player[0].balance}\n"
                            f"CARD_NUM💳: {card_num}\n"
                            f"USER YECHMOQCHI BOLGAN SUMMA: {float(data['summa'])}\n"
                            f"O'TKIZISHINGIZ KERAK BOLGAN SUMMA: {cur_balance}$\n"
                            f"UZB_SUM: {summ} SOM</b>")
                await msg.bot.send_message(chat_id=i, reply_markup=await with_balance(state, user_id), text=msg_text,
                                           parse_mode="HTML")

        elif data["method"] == humo:
            prosent = (float(data["summa"]) / 100) * 1
            cur_balance = float(data["summa"]) - prosent
            summ = cur_balance * dollar_cur_value
            admins_royxati = await main()
            for i in admins_royxati:
                msg_text = (f"<b>Pull yechib olish uchun yangi so'rov‼\n\n"
                            f"CHAT_ID🆔: {player[0].chat_id}\n"
                            f"PUBG_ID🆔: {player[0].pubg_id}\n"
                            f"USERNAME: {player[0].username}\n"
                            f"PHONE_NUM📱: {player[0].phone_number}\n"
                            f"E-MAIL📧: {player[0].email}\n"
                            f"TG_USERNAME📱:{player[0].tg_username}\n"
                            f"ISM: {player[0].name}\n"
                            f"BALANCE💰: {player[0].balance}\n"
                            f"CARD_NUM💳: {card_num}\n"
                            f"USER YECHMOQCHI BOLGAN SUMMA: {float(data['summa'])}\n"
                            f"O'TKIZISHINGIZ KERAK BOLGAN SUMMA: {cur_balance}$\n"
                            f"UZB_SUM: {summ} SOM</b>")
                await msg.bot.send_message(chat_id=i, reply_markup=await with_balance(state, user_id), text=msg_text,
                                           parse_mode="HTML")

        elif data["method"] == payeer:
            prosent = (float(data["summa"]) / 100) * 4
            cur_balance = float(data["summa"]) - prosent
            summ = cur_balance * dollar_cur_value
            admins_royxati = await main()
            for i in admins_royxati:
                msg_text = (f"<b>Pull yechib olish uchun yangi so'rov‼\n\n"
                            f"CHAT_ID🆔: {player[0].chat_id}\n"
                            f"PUBG_ID🆔: {player[0].pubg_id}\n"
                            f"USERNAME: {player[0].username}\n"
                            f"PHONE_NUM📱: {player[0].phone_number}\n"
                            f"E-MAIL📧: {player[0].email}\n"
                            f"TG_USERNAME📱:{player[0].tg_username}\n"
                            f"ISM: {player[0].name}\n"
                            f"BALANCE💰: {player[0].balance}\n"
                            f"CARD_NUM💳: {card_num}\n"
                            f"USER YECHMOQCHI BOLGAN SUMMA: {float(data['summa'])}\n"
                            f"O'TKIZISHINGIZ KERAK BOLGAN SUMMA: {cur_balance}$\n"
                            f"UZB_SUM: {summ} SOM</b>")
                await msg.bot.send_message(chat_id=i, reply_markup=await with_balance(state, user_id), text=msg_text,
                                           parse_mode="HTML")


@dp.callback_query_handler(lambda call: call.data.startswith("toldirishda"),
                           state="*")
async def handler_fill_callback(call: types.CallbackQuery, state: FSMContext):
    summa = call.data.split(":")[1]
    user_id = call.data.split("|")
    chat_id = user_id[1].split(":")[0]
    async with state.proxy() as data:
        data["summa"] = summa
        data["accept_id"] = chat_id
        print(f"data88:{data}")
    await call.message.answer(text="<b> Chekni jonating📨</b>", parse_mode='HTML')
    await state.set_state("chek2")


@dp.message_handler(content_types=types.ContentType.PHOTO, state="chek2")
async def handle_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        chat_id = data["accept_id"]
        photo_file_id = message.photo[-1].file_id
        user_id_str = chat_id
        player = await Players.get_by_chat_id(chat_id=user_id_str)

        amount = data["summa"]
        print(amount)
        balance = player[0].balance
        new_balance = float(balance) - float(amount)
        await Players.update2(user_id_str, balance=new_balance)

        msg_text = (f"<b>Userga pull o'tkazildi✅\n\n"
                    f"PUBG_ID🆔: {player[0].pubg_id}\n"
                    f"USERNAME: {player[0].username}\n"
                    f"TG_USERNAME📱:{player[0].tg_username}\n"
                    f"PHONE_NUM📱: {player[0].phone_number}\n"
                    f"E-MAIL📧: {player[0].email}\n"
                    f"ISM: {player[0].name}\n"
                    f"BALANCE💰: {player[0].balance}\n</b>")

        msg_text1 = (f"<b>Sizga pull o'tkizildi✅\n\n"
                     f"PUBG_ID🆔: {player[0].pubg_id}\n"
                     f"USERNAME: {player[0].username}\n"
                     f"PHONE_NUM📱: {player[0].phone_number}\n"
                     f"E-MAIL📧: {player[0].email}\n"
                     f"TG_USERNAME📱:{player[0].tg_username}\n"
                     f"ISM: {player[0].name}\n"
                     f"BALANCE💰: {player[0].balance}\n</b>")

    await message.bot.send_photo(chat_id=-1001858175397, caption=msg_text, parse_mode="HTML", photo=photo_file_id)
    await message.bot.send_photo(chat_id=chat_id, caption=msg_text1, parse_mode="HTML", photo=photo_file_id)
    await state.finish()


@dp.callback_query_handler(lambda call: call.data.startswith("2bek"), state="*")
async def what_delete_handler(call: types.CallbackQuery, state: FSMContext):
    chat_id = call.data.split(":")[1]
    async with state.proxy() as data:
        data["cancel_id"] = chat_id

    if await state.get_state() != "what_delate":
        await state.set_state("what_delate")
        await call.message.answer(text="Nima uchun bekor qildingiz❓\n\nIzoh yozish majburiy❗️")


@dp.message_handler(state='what_delate')
async def not_save_handler(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        chat_id = data["cancel_id"]
        print(chat_id)
    await bot.send_message(chat_id=chat_id,
                           text=f"<b>Sizning sorovingiz bekor qilindi❗️\nAdmin izohi: {msg.text}\n\nMurojat uchun: https://t.me/Pubg_turnerbot</b>",
                           parse_mode="HTML")
    await state.finish()
