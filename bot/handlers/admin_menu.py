from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart, Text
from bot.buttons.reply_buttons import main_menu_buttons, admin_panel
from bot.buttons.text import info, statistics, turnir, balance, back_menu, statistika, add_admin
from bot.dispatcher import dp
from aiogram import types, Bot
# from db.jconfig import admin_panel, AdminPanel
from db.model import Admins

# admins = [1105995218]
# admins_royxati = await main()
#         for i in admins_royxati:



async def main():
    admins = await Admins.get_all_chat_ids()  # Assuming get_all_chat_ids is a coroutine
    return admins


@dp.message_handler(commands="admin", state="*")
async def admin_handler(msg: types.Message, state: FSMContext):
    admin_id = str(msg.from_user.id)
    admins_royxati = await main()
    for i in admins_royxati:
        if i == admin_id:
            admin_markup = await admin_panel()  # Call the admin_panel method
            await msg.answer(
                text=f"<b>Assalomu alaykum {msg.from_user.full_name} siz adminsiz!</b>",
                reply_markup=admin_markup,
                parse_mode='HTML'
            )
            await state.set_state("admin_menu")


@dp.message_handler(Text(statistika), state="admin_menu")
async def stat_handler(msg: types.Message, state: FSMContext):
    bot = Bot.get_current()
    chat_id = '@pythondevsof'
    members = await bot.get_chat_members_count(chat_id)
    await msg.answer(f"Kanaldagi foydalanuvchilar soni: {members}")


@dp.message_handler(Text(add_admin), state="admin_menu")
async def add_admin_handler(msg: types.Message, state: FSMContext):
    await msg.answer("<b>Qoshmoqchi bolgan foydalanuvchi CHAT_ID sini kiriting🆔: </b>", parse_mode="HTML")
    await state.set_state("admin_id")


@dp.message_handler(state="admin_id")
async def add_admin_handler(msg: types.Message, state: FSMContext):
    chat_id = msg.text
    admins_royxati = await main()
    # for admin in admins_royxati:
    await Admins.create(chat_id=chat_id)
    await msg.answer(f"Admin muafaqiyatli qoshildi✅\n"
                     f"Adminlar royxati {admins_royxati}")
