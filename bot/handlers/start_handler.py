from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart, Text
from bot.buttons.inline_buttons import check_button
from bot.buttons.reply_buttons import main_menu_buttons
from bot.buttons.text import info, statistics, turnir, balance, back_menu, check_sub, profil, admin
from bot.dispatcher import dp, bot
from aiogram import types
from db.model import User, Total, Players
from save import CHANNELS
from utils import subcription
from middlewares import BigBrother


# -1001858175397 -> payment -> qaysi user balance toldirmoqchi shunaqa narsalar
# -1001911289543 -> information -> shaxsiy malumotlar
# -1001834462254 -> statistics -> turnir statistikalari

# dp.message.middleware.register(BigBrother())


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
        """referal"""
        # if msg.get_args() != "":
        #     add_user = await User.get(msg.get_args())
        #     if add_user:
        #         add = add_user[0].added_user + 1
        #         await User.update(msg.get_args(), added_user=add)
        #         await bot.send_message(chat_id=int(msg.get_args()),
        #                                text=f"<b>Sizning yangi referal azoingiz🆕\n🆔ID: <a href='tg://user?id={msg.from_user.id}'>{msg.from_user.id}</a>\n🆔Yashirin ID: {hidden_id}\nIsm-Familiya: {msg.from_user.full_name}</b>",
        #                                parse_mode='HTML')
        #         ref = await User.get(msg.get_args())
        #         await User.update(str(msg.from_user.id), add_user=msg.get_args())
        """referal end"""
    else:
        try:
            await msg.answer(text=f"<b>Assalomu alaykum {msg.from_user.full_name}</b>",
                         reply_markup=await main_menu_buttons(), parse_mode='HTML')
            await state.set_state("menu")
        except:
            pass


# @dp.message_handler(Text([info, statistics]), state="menu")
# async def name_handler(msg: types.Message, state: FSMContext):
#     await msg.answer(text="Salom")


@dp.message_handler(Text(admin), state="*")
async def support_handler(msg: types.Message, state: FSMContext):
    support = "https://t.me/Pubg_turner_bot"
    await msg.answer(f"<b>Adminga murojat qilish uchun ushbu botga murojat qiling👇\n\n"
                     f" {support}</b>", parse_mode="HTML")
    await state.set_state("menu")
