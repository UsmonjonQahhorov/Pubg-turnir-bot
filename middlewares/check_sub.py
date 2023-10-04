from aiogram import types
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import logging
from bot.buttons.inline_buttons import member_buttons
from bot.dispatcher import bot
from save import CHANNELS
from utils.mics import subscription


class BigBrother(BaseMiddleware):
    async def on_pre_process_update(self, update: types.Update, data: dict):
        if update.message:
            user = update.message.from_user.id
        elif update.callback_query:
            user = update.callback_query.from_user.id
            if update.callback_query.data == 'check_subs':
                return
        else:
            return
        logging.info(user)
        result = "<i>Botdan foydalanish uchun quydagi kanallarga obuna bo'ling:</i\n>"
        final_status = True
        for channel in CHANNELS:
            status = await subscription.check(user_id=user, channel=channel)

            final_status *= status

        if not final_status:
            print(final_status)
            try:
                await update.message.answer(result, disable_web_page_preview=True, reply_markup=await member_buttons(),
                                            parse_mode="HTML")
            except:
                pass

            raise CancelHandler
