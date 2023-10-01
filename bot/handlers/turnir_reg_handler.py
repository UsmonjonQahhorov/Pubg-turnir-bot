from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart, Text

# from bot.buttons.inline_buttons import agree_button
from bot.buttons.reply_buttons import main_menu_buttons, turnir_panel
from bot.buttons.text import info, statistics, turnir, balance, basic, pro, free, save, cancel, agree
from bot.dispatcher import dp, bot
from aiogram import types
import asyncio
from bot.buttons.inline_buttons import agree_button, agree_or_dis, agree_or_dis2, agree_or_dis3, \
    turnir_basic_begin, turnir_pro_begin
# from .admin_menu import admins
from db.model import User, Players, Basic, Free, Pro, Total, Admins


async def main():
    admins = await Admins.get_all_chat_ids()  # Assuming get_all_chat_ids is a coroutine
    return admins


@dp.message_handler(Text([basic]), state="turnir")
async def basic_handler(msg: types.Message, state: FSMContext):
    chat_id = msg.from_user.id
    await msg.answer(text="Basic yonalishni tanladingiz bunda siz har bir killingiz"
                          "ga 3$ dan pull olasiz ishtirok etish summasi 5$",
                     reply_markup=await agree_button())
    await state.set_state("agrea")
    await msg.delete()


@dp.callback_query_handler(state="agrea")
async def basic_handler(call: types.CallbackQuery, state: FSMContext):
    count = await Basic.get_count()
    if count <= 99:
        user_id = str(call.from_user.id)
        player = await Players.get_by_chat_id(chat_id=user_id)
        admins_royxati = await main()
        for i in admins_royxati:
            caption = (f"<b>Basic turniriga qatnashish uchun so'rov\n\n"
                       f"CHAT_ID🆔: {player[0].chat_id}\n"
                       f"NAME: {player[0].name}\n"
                       f"USERNAME: {player[0].username}\n"
                       f"PUBG_ID🆔: {player[0].pubg_id}\n"
                       f"TG_USERNAME: {player[0].tg_username}</b>")
            await bot.send_message(chat_id=i, text=caption, parse_mode="HTML",
                                   reply_markup=await agree_or_dis2(chat_id=user_id))
        await call.message.delete()
    else:
        await call.message.answer("<b>Kechirasiz😔 hozirda turnir qatnashuvchi bilan to'ldi\n"
                                  "20 minut ichida admindan javob olasiz😉</b>", parse_mode="HTML")
    await state.finish()


@dp.callback_query_handler(lambda call: call.data.startswith("5bek"), state="*")
async def what_delete_handler(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    chat_id = call.data.split(":")[1]
    async with state.proxy() as data:
        data["cancel_id"] = chat_id
    await state.set_state("boldimi")
    await call.message.answer(text="Nima uchun bekor qildingiz❓\n\nIzoh yozish majburiy❗️")


@dp.message_handler(state='boldimi')
async def not_save_handler(msg: types.Message, state: FSMContext):
    await bot.delete_message(msg.from_user.id, msg.message_id - 1)
    async with state.proxy() as data:
        chat_id = data.get('cancel_id')
    await bot.send_message(chat_id=chat_id,
                           text=f"<b>Sizning sorovingiz bekor qilindi❗️\nAdmin izohi: {msg.text}\n\nMurojat uchun: @U_Qahhorov</b>",
                           parse_mode="HTMl")


@dp.callback_query_handler(lambda call: call.data.startswith("Baruxsat"))
async def basicsave_handler(call: types.CallbackQuery, state: FSMContext):
    user_id = call.data.split(":")[1]
    player = await Players.get_by_chat_id(chat_id=user_id)
    if player[0].chat_id == user_id:
        if player[0].balance <= 0:
            await call.answer(f"User balancesi💰 yetarli emas‼", show_alert=True)
        else:
            new_balance = player[0].balance - 5.0
            chat_id = player[0].chat_id
            username = player[0].username
            tg_username = player[0].tg_username
            name = player[0].name
            await Players.update2(user_id, balance=new_balance)  # Use the float value
            message = await call.message.answer(f"Pul yechib olindi✅ Hozirgi balance {new_balance}💲")
            await Basic.create(
                chat_id=chat_id,
                username=username,
                tg_username=tg_username,
                name=name
            )
            # await Total.create(
            #     chat_id=chat_id,
            #     username=username,
            #     tg_username=tg_username,
            #     name=name,
            #     priority="Basic"
            # )
            text = (f"Turnir🏟 ishtirokchilari👤\n\n"
                    f"<b>USER CHAT_ID🆔 :{chat_id}"
                    f" USERNAME: {tg_username}"
                    f" TG_USERNAME: {username}"
                    f" NAME: {name}\n"
                    f"TURNIR: Basic</b>")

            session = await bot.send_message(text=text, chat_id=-1001834462254, parse_mode="HTML")

            new_text = ""
            total_u = await Basic.get_all()
            for i in range(len(total_u)):
                new_text += (f"<b>{i + 1}: USER CHAT_ID🆔 : {total_u[i][0].chat_id}"
                             f" USERNAME: {total_u[i][0].username}"
                             f" NAME: {total_u[i][0].name}\n\n</b>"
                             f"TURNIR: Basic")
                # print(text)
                # -1001975309076
            await bot.edit_message_text(text=new_text, chat_id=session.chat.id, parse_mode="HTML",
                                        message_id=session.message_id, reply_markup=await turnir_basic_begin())
            await asyncio.sleep(2)
            await message.delete()

    else:
        await call.message.answer(f"<b>Bunday user topilmadi😔</b>", parse_mode="HTML")
    await call.message.delete()
    await state.finish()


@dp.message_handler(Text([pro]), state="turnir")
async def pro_handler(msg: types.Message, state: FSMContext):
    await msg.answer(text="Pro yonalishni tanladingiz bunda siz har bir killingiz"
                          "ga 5$ dan pull olasiz ishtirok etish summasi 10$", reply_markup=await agree_button())
    await state.set_state("proagree")
    await msg.delete()


@dp.callback_query_handler(state="proagree")
async def basic_handler(call: types.CallbackQuery, state: FSMContext):
    count = await Pro.get_count()
    if count <= 99:
        user_id = str(call.from_user.id)
        player = await Players.get_by_chat_id(chat_id=user_id)
        admins_royxati = await main()
        for i in admins_royxati:
            caption = (f"<b>Pro turniriga qatnashish uchun so'rov\n\n"
                       f"CHAT_ID🆔: {player[0].chat_id}\n"
                       f"NAME: {player[0].name}\n"
                       f"USERNAME: {player[0].username}\n"
                       f"PUBG_ID🆔: {player[0].pubg_id}\n"
                       f"TG_USERNAME: {player[0].tg_username}</b>")
            await bot.send_message(chat_id=i, text=caption, parse_mode="HTML",
                                   reply_markup=await agree_or_dis3(chat_id=user_id))
        await call.message.delete()
    else:
        await call.message.answer("<b>Kechirasiz😔 hozirda turnir qatnashuvchi bilan to'ldi\n"
                                  "20 minut ichida admindan javob olasiz😉</b>", parse_mode="HTML")
    await state.finish()


@dp.callback_query_handler(lambda call: call.data.startswith("3bek"), state="*")
async def what_delete_handler(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    chat_id = call.data.split(":")[1]
    async with state.proxy() as data:
        data["cancel_id"] = chat_id
    await state.set_state("nimaga")
    await call.message.answer(text="Nima uchun bekor qildingiz❓\n\nIzoh yozish majburiy❗️")


@dp.message_handler(state='nimaga')
async def not_save_handler(msg: types.Message, state: FSMContext):
    try:
        await bot.delete_message(msg.from_user.id, msg.message_id - 1)
    except:
        pass
    async with state.proxy() as data:
        chat_id = data.get('cancel_id')
    await bot.send_message(chat_id=chat_id,
                           text=f"<b>Sizning sorovingiz bekor qilindi❗️\nAdmin izohi: {msg.text}\n\nMurojat uchun: @U_Qahhorov</b>",
                           parse_mode="HTMl")


@dp.callback_query_handler(lambda call: call.data.startswith("3Ruxsat"), state="*")
async def basicsave_handler(call: types.CallbackQuery, state: FSMContext):
    user_id = call.data.split(":")[1]
    player = await Players.get_by_chat_id(chat_id=user_id)
    if player[0].chat_id == user_id:
        if player[0].balance <= 0:
            await call.answer(f"User balancesi💰 yetarli emas‼", show_alert=True)
        else:
            new_balance = player[0].balance - 10.0
            chat_id = player[0].chat_id
            username = player[0].username
            tg_username = player[0].tg_username
            name = player[0].name
            await Players.update2(user_id, balance=new_balance)  # Use the float value
            message = await call.message.answer(f"Pul yechib olindi✅ Hozirgi balance {new_balance}💲")
            await Pro.create(
                chat_id=chat_id,
                username=username,
                tg_username=tg_username,
                name=name
            )
            # await Total.create(
            #     chat_id=chat_id,
            #     username=username,
            #     tg_username=tg_username,
            #     name=name,
            #     priority="Pro"
            # )

            text = (f"Turnir🏟 ishtirokchilari👤\n\n"
                    f"<b>USER CHAT_ID🆔 :{chat_id}"
                    f" USERNAME: {tg_username}"
                    f" TG_USERNAME: {username}"
                    f" NAME: {name}\n"
                    f"TURNIR: Pro</b>")

            session = await bot.send_message(text=text, chat_id=-1001834462254, parse_mode="HTML")

            new_text = ""
            total_u = await Pro.get_all()
            for i in range(len(total_u)):
                new_text += (f"<b>{i + 1}: USER CHAT_ID🆔 : {total_u[i][0].chat_id}"
                             f" USERNAME: {total_u[i][0].username}"
                             f" NAME: {total_u[i][0].name}\n\n</b>"
                             f"TURNIR: Pro")
            await bot.edit_message_text(text=new_text, chat_id=session.chat.id, parse_mode="HTML",
                                        message_id=session.message_id, reply_markup=await turnir_pro_begin())
            await asyncio.sleep(2)
            await message.delete()

    else:
        await call.message.answer(f"<b>Bunday user topilmadi😔</b>", parse_mode="HTML")
    await call.message.delete()
    await state.finish()
