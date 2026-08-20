from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from bot.lexicon.lexicon_ru import BOT_BTN

get_info_btn = InlineKeyboardButton(text=BOT_BTN['get_info'], callback_data='check_user')
reply_keyboard = InlineKeyboardMarkup(inline_keyboard=[[get_info_btn],])

def link_keyboard(url: str):
    url_btn = InlineKeyboardButton(text=BOT_BTN['profile'], url=url)
    return InlineKeyboardMarkup(inline_keyboard=[[url_btn],])