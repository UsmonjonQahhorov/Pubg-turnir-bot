from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart, Text
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# from bot.buttons.inline_buttons import agree_button
from bot.buttons.reply_buttons import main_menu_buttons, turnir_panel
from bot.buttons.text import info, statistics, turnir, balance, basic, pro, free, save, cancel, done
from bot.dispatcher import dp, bot
from aiogram import types
import asyncio
from bot.buttons.inline_buttons import agree_or_dis, agree_or_dis2, done_button, agree_or_dis_free, turnir_free_begin
# from .admin_menu import admins
from db.model import User, Players, Basic, Free, Pro, Total, Admins


async def main():
    admins = await Admins.get_all_chat_ids()  # Assuming get_all_chat_ids is a coroutine
    return admins


@dp.message_handler(Text([turnir]), state="menu")
async def turnir_handler(msg: types.Message, state: FSMContext):
    user_id = str(msg.from_user.id)
    user = await Players.get_by_chat_id(chat_id=user_id)

    if user:
        await msg.answer(text="Turnir Menu", reply_markup=await turnir_panel())
        await state.set_state("turnir")
    else:
        await msg.answer(text=f"<b>Turnirga kirish uchun o'zingizni ma'lumotlaringizni kiriting👇"
                              f"Ma'lumotlarni to'g'ri kiriting, sohta ma'lumot kiritish faqat o'zingiz uchun zarar bolishi mumkin‼\n\n"
                              f"🆔: PUBG dagi ID ingizni yuboring👇 </b>", parse_mode="HTML")
        await state.set_state("tinfo")


@dp.message_handler(state="tinfo")
async def turnir_handler1(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["pubg_id"] = msg.text
    await msg.answer(f"<b>PUBG usernameni kiriting👇</b>", parse_mode="HTML")
    await state.set_state("username")
    await msg.delete()


@dp.message_handler(state="username")
async def turnir_handler2(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["username"] = msg.text
    await msg.answer(f"<b> Ismingizni kiriting kiriting👇</b>", parse_mode="HTML")
    await state.set_state("number")
    await msg.delete()


@dp.message_handler(state="number")
async def turnir_handler2(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["name"] = msg.text
    rkm = ReplyKeyboardMarkup(keyboard=[[KeyboardButton("Contact📱", request_contact=True)]], resize_keyboard=True)
    await msg.answer("Telefon raqamingizni yuboring📱👇", reply_markup=rkm)
    await msg.delete()
    await state.set_state("phone_num")


@dp.message_handler(content_types=types.ContentType.CONTACT, state="phone_num")
async def contact_handler2(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["phone_number"] = msg.contact.phone_number
        await msg.answer("📧Emailingizni kiriting👇")
    await state.set_state("e-mail")


@dp.message_handler(state="e-mail")
async def display_handler(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['email'] = msg.text
        caption = await msg.answer(f"<b>Kiritilgan ma'lumotlar📄\n\n"
                                   f"PUBG_ID🆔: {data['pubg_id']}\n"
                                   f"Username: {data['username']}\n"
                                   f"Email📧: {data['email']}\n"
                                   f"PHONE_NUM: {data.get('phone_number', 'N/A')}\n"
                                   f"Name: {data['name']}</b>", parse_mode="HTML")
        key = types.InlineKeyboardMarkup(row_width=2)
        key.add(types.InlineKeyboardButton(text="Saqlash✅", callback_data="save"),
                types.InlineKeyboardButton(text="Bekor qilish❌", callback_data="cancel"))
        await msg.answer("Saqlash✅ yoki Bekor qilish❌", reply_markup=key)
        await msg.delete()
        await state.set_state("save_state")
        # await asyncio.sleep(15)
        # await caption.delete()


@dp.callback_query_handler(text="save", state="save_state")
async def handle_save(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        pubg_id = data.get("pubg_id")
        username = data.get("username")
        name = data.get("name")
        phone_num = data.get('phone_number')
        email = data.get('email')

    # Ma'lumotlarni xabar yuborish
    message_text = f"<b>Yangi user PUBG turnirida royxatdan o'tdi📄\n\n" \
                   f"PUBG_ID🆔: {pubg_id}\n" \
                   f"Username: {username}\n" \
                   f"PHONE_NUM: {phone_num}\n" \
                   f"Name: {name}\n" \
                   f"Email📧: {email}</b>"
    user_id = str(call.from_user.id)
    tg_username = call.from_user.username
    await Players.create(pubg_id=data['pubg_id'],
                         username=data['username'],
                         name=data['name'],
                         chat_id=user_id,
                         phone_number=phone_num,
                         email=email,
                         tg_username=tg_username)
    await bot.send_message(-1001911289543, message_text, parse_mode="HTML")
    await call.message.delete()
    await state.finish()
    keyboard = await turnir_panel()
    await call.message.answer("Ma'lumotlaringiz muafaqiyatli saqlandi", reply_markup=keyboard)
    await state.set_state('turnir')


@dp.callback_query_handler(text="cancel", state="name")
async def handle_cancel(call: types.CallbackQuery, state: FSMContext):
    await call.answer("Saqlash bekor qilindi", show_alert=True)
    await call.message.delete()
    await state.finish()
    keyboard = await main_menu_buttons()
    await call.message.answer("Saqlash bekor qilindi menulardan birini tanlang👇", reply_markup=keyboard)
    await state.set_state('menu')


@dp.message_handler(Text([free]), state="turnir")
async def free_handler(msg: types.Message, state: FSMContext):
    await msg.answer(
        text="<b>Free yonalishni tanladingiz, Free bolimida ishtirok etish"
             " uchun sizga admin orqali shartlar beriladi va siz u shartlarni bajarishingiz kerak bo'ladi\n\n"
             "Murojat uchun https://t.me/Pubg_turner_bot</b>",
        reply_markup=await done_button(), parse_mode="HTML")
    await state.set_state("free_turnit_handler")


@dp.callback_query_handler(text=done, state="free_turnit_handler")
async def basic_handler(call: types.CallbackQuery, state: FSMContext):
    count = await Free.get_count()
    if count <= 99:
        user_id = str(call.from_user.id)
        player = await Players.get_by_chat_id(chat_id=user_id)
        admins_royxati = await main()
        for i in admins_royxati:
            caption = (f"<b>Free turniriga qatnashish uchun so'rov\n\n"
                       f"CHAT_ID🆔: {player[0].chat_id}\n"
                       f"NAME: {player[0].name}\n"
                       f"USERNAME: {player[0].username}\n"
                       f"PUBG_ID🆔: {player[0].pubg_id}\n"
                       f"TG_USERNAME: {player[0].tg_username}</b>")
            await bot.send_message(chat_id=i, text=caption, parse_mode="HTML",
                                   reply_markup=await agree_or_dis_free(chat_id=user_id))
        await call.message.delete()
    else:
        await call.message.answer("<b>Kechirasiz😔 hozirda turnir qatnashuvchi bilan to'ldi\n"
                                  "20 minut ichida admindan javob olasiz😉</b>", parse_mode="HTML")
    await state.finish()


@dp.callback_query_handler(lambda call: call.data.startswith("pasholnax"), state="*")
async def what_delete_handler(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    chat_id = call.data.split(":")[1]
    async with state.proxy() as data:
        data["cancel_id"] = chat_id
    await state.set_state("sikvording")
    await call.message.answer(text="Nima uchun bekor qildingiz❓\n\nIzoh yozish majburiy❗️")


@dp.message_handler(state='sikvording')
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


@dp.callback_query_handler(lambda call: call.data.startswith("sukamisan"), state="*")
async def basicsave_handler(call: types.CallbackQuery, state: FSMContext):
    user_id = call.data.split(":")[1]
    player = await Players.get_by_chat_id(chat_id=user_id)
    username = player[0].username
    tg_username = player[0].username
    name = player[0].name
    await Free.create(
        chat_id=user_id,
        username=username,
        tg_username=tg_username,
        name=name
    )

    text = (f"Turnir🏟 ishtirokchilari👤\n\n"
            f"<b>USER CHAT_ID🆔 :{user_id}"
            f" USERNAME: {tg_username}"
            f" TG_USERNAME: {username}"
            f" NAME: {name}\n"
            f"TURNIR: Free</b>")

    session = await bot.send_message(text=text, chat_id=-1001834462254, parse_mode="HTML")

    new_text = ""
    total_u = await Free.get_all()
    for i in range(len(total_u)):
        new_text += (f"<b>{i + 1}: USER CHAT_ID🆔 : {total_u[i][0].chat_id}"
                     f" USERNAME: {total_u[i][0].username}"
                     f" NAME: {total_u[i][0].name}\n\n</b>"
                     f"TURNIR: Free")
    await bot.edit_message_text(text=new_text, chat_id=session.chat.id, parse_mode="HTML",
                                message_id=session.message_id, reply_markup=await turnir_free_begin())
    await asyncio.sleep(2)
    await call.message.delete()
