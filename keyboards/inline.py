from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_inline_kb_check_data() -> InlineKeyboardMarkup:
    inline_but = [
        [InlineKeyboardButton(text='Все верно', callback_data='correct')],
        [InlineKeyboardButton(text='Не верно', callback_data='incorrect')],
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_but)
