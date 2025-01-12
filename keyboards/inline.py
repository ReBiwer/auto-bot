from db_handler.models import RefuelingTable

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_inline_kb_check_data() -> InlineKeyboardMarkup:
    inline_but = [
        [InlineKeyboardButton(text='Все верно', callback_data='correct')],
        [InlineKeyboardButton(text='Не верно', callback_data='incorrect')],
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_but)


def get_inline_kb_refuels(refuels: dict[int, RefuelingTable]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for id_refuel, refuel in refuels.items():
        builder.row(
            InlineKeyboardButton(text=f'Заправка {refuel.date.strftime('%d.%m.%Y')} числа',
                                 callback_data=f'detail_refuel_{id_refuel}')
        )
    builder.adjust(1)
    return builder.as_markup()


def get_inline_butt_back():
    but = InlineKeyboardButton(text='Обратно к списку заправок', callback_data='go_to_refuels')
    return InlineKeyboardMarkup(inline_keyboard=[[but]])
