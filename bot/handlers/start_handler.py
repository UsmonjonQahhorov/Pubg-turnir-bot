from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart, Text
from bot.buttons.inline_buttons import check_button
from bot.buttons.reply_buttons import main_menu_buttons
from bot.buttons.text import info, statistics, turnir, balance, back_menu, check_sub, profil, admin
from bot.dispatcher import dp, bot
from aiogram import types
from db.model import User, Total, Players


@dp.message_handler(Text(back_menu), state='*')
async def back_handler(msg: types.Message, state: FSMContext):
    await msg.delete()
    await msg.answer(
        text=f"<b>{msg.from_user.full_name} asosiy bo'limdasiz✅\n\nBo'limlardan birini tanlang⬇️</b>",
        reply_markup=await main_menu_buttons(), parse_mode='HTML')
    await state.set_state('menu')


@dp.message_handler(commands=['start', 'help'], state='*')
async def start_handler(msg: types.Message, state: FSMContext):
    user_id = str(msg.from_user.id)
    user = await User.get_by_chat_id(chat_id=user_id)
    if user is None:
        username = msg.from_user.username
        fullname = f"{msg.from_user.first_name} {msg.from_user.last_name}"
        await User.create(chat_id=user_id, fullname=fullname, username=username)
        await msg.bot.send_message(-1001911289543,
                                   text=f"👤Yangi bot foydalanuvchi\n\n🆔ID: {msg.from_user.id}\n📝Ism-Familia: {msg.from_user.full_name}\n©️Username: @{msg.from_user.username}")

        await msg.answer(text=f"<b>Assalomu alaykum {msg.from_user.full_name}</b>",
                         reply_markup=await main_menu_buttons(), parse_mode='HTML')
        await state.set_state("menu")

    else:
        try:
            await msg.answer(text=f"<b>Assalomu alaykum {msg.from_user.full_name}</b>",
                             reply_markup=await main_menu_buttons(), parse_mode='HTML')
            await state.set_state("menu")
        except:
            pass


@dp.message_handler(Text(admin), state="*")
async def support_handler(msg: types.Message, state: FSMContext):
    support = "https://t.me/Pubg_turner_bot"
    await msg.answer(f"<b>Adminga murojat qilish uchun ushbu botga murojat qiling👇\n\n"
                     f" {support}</b>", parse_mode="HTML")
    await state.set_state("menu")
