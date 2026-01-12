from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from bot.lexicon.lexicon_ru import BOT_BTN

get_info_btn = KeyboardButton(text=BOT_BTN['get_info'])
reply_keyboard = ReplyKeyboardMarkup(
    keyboard=[[get_info_btn],],
    resize_keyboard=True,
    one_time_keyboard=True
)