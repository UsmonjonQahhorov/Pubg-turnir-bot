import asyncio

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart, Text

from bot.buttons.reply_buttons import main_menu_buttons, admin_panel, message_turnir, manage_turnir
from bot.buttons.text import info, statistics, turnir, balance, back_menu, statistika, add_admin, manage_t, habar, \
    delete, msg_basic, msg_pro, msg_free, msg_all, admin_back
from bot.dispatcher import dp, bot
from aiogram import types, Bot
# from db.jconfig import admin_panel, AdminPanel
from db.model import Admins, Pro, Free, Basic, Total, Players


@dp.message_handler(Text(manage_t), state="admin_menu")
async def manage_handler(msg: types.Message, state: FSMContext):
    await msg.answer("Siz turnirni boshqarish panelidasiz⚙", reply_markup=await message_turnir())
    await state.set_state("turnir_manage")


@dp.message_handler(Text(habar), state="turnir_manage")
async def manage2_handler(msg: types.Message, state: FSMContext):
    await msg.answer("Menulardan birini tanlang👇", reply_markup=await manage_turnir())
    await state.set_state("chose_one")


@dp.message_handler(Text(delete), state="turnir_manage")
async def manage2_handler(msg: types.Message, state: FSMContext):
    await Total.delete_all()
    await Basic.delete_all()
    await Pro.delete_all()
    await msg.answer("Yangi turnir boshlash uchun ma'lumotlar tozalandi👍")
    await state.finish()


@dp.message_handler(Text(msg_basic), state="chose_one")
async def manage2_handler(msg: types.Message, state: FSMContext):
    await msg.answer("Basic turniridagi ishtirokchilarga jonatmoqchi bolgan habaringizni jonating👇")
    await state.set_state("basic_send")


@dp.message_handler(state="basic_send")
async def manage2_handler(msg: types.Message, state: FSMContext):
    basic_players = await Basic.get_all()
    message1 = await msg.answer("Raxmat🙂")
    for i in range(len(basic_players)):
        await bot.send_message(text=f"Salom {basic_players[i][0].username}\n"
                                    f" Admindan kelgan habar:{msg.text}",
                               chat_id=basic_players[i][0].chat_id)
    message = await msg.answer("Habarlar yuborildi👍")
    await asyncio.sleep(5)
    await message.delete()
    await message1.delete()


@dp.message_handler(Text(msg_pro), state="chose_one")
async def manage2_handler(msg: types.Message, state: FSMContext):
    await msg.answer("Pro turniridagi ishtirokchilarga jonatmoqchi bolgan habaringizni jonating👇")
    await state.set_state("pro_send")


@dp.message_handler(state="pro_send")
async def manage2_handler(msg: types.Message, state: FSMContext):
    basic_players = await Pro.get_all()
    message1 = await msg.answer("Raxmat🙂")
    for i in range(len(basic_players)):
        await bot.send_message(text=f"Salom {basic_players[i][0].username}\n"
                                    f" Admindan kelgan habar:{msg.text}",
                               chat_id=basic_players[i][0].chat_id)
    message = await msg.answer("Habarlar yuborildi👍")
    await asyncio.sleep(5)
    await message.delete()
    await message1.delete()


@dp.message_handler(Text(msg_free), state="chose_one")
async def manage2_handler(msg: types.Message, state: FSMContext):
    await msg.answer("Free turniridagi ishtirokchilarga jonatmoqchi bolgan habaringizni jonating👇")
    await state.set_state("free_send")


@dp.message_handler(state="free_send")
async def manage2_handler(msg: types.Message, state: FSMContext):
    basic_players = await Free.get_all()
    message1 = await msg.answer("Raxmat🙂")
    for i in range(len(basic_players)):
        await bot.send_message(text=f"Salom {basic_players[i][0].username}\n"
                                    f" Admindan kelgan habar:{msg.text}",
                               chat_id=basic_players[i][0].chat_id)
    message = await msg.answer("Habarlar yuborildi👍")
    await asyncio.sleep(5)
    await message.delete()
    await message1.delete()


@dp.message_handler(Text(msg_all), state="chose_one")
async def manage2_handler(msg: types.Message, state: FSMContext):
    await msg.answer("Hammaga habaringizni jonating👇")
    await state.set_state("all_send")


@dp.message_handler(state="all_send")
async def manage2_handler(msg: types.Message, state: FSMContext):
    basic_players = await Players.get_all()
    message1 = await msg.answer("Raxmat🙂")
    for i in range(len(basic_players)):
        await bot.send_message(text=f"<b>Salom {basic_players[i][0].username}🙂\n"
                                    f" Siz uchun admindan habar📨: {msg.text}</b>",
                               chat_id=basic_players[i][0].chat_id, parse_mode="HTML")
    message = await msg.answer("Habarlar yuborildi👍")
    await asyncio.sleep(5)
    await message.delete()
    await message1.delete()


@dp.message_handler(Text(admin_back), state='*')
async def back_handler(msg: types.Message, state: FSMContext):
    await msg.delete()
    await msg.answer(text=f"<b>Tanlang👇</b>",
                     reply_markup=await admin_panel(), parse_mode='HTML')
    await state.set_state("admin_menu")
