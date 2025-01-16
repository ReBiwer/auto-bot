from db_settings.DTO_models import RefuelGetDTO

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_inline_kb_check_data() -> InlineKeyboardMarkup:
    inline_but = [
        [InlineKeyboardButton(text='Все верно', callback_data='correct')],
        [InlineKeyboardButton(text='Не верно', callback_data='incorrect')],
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_but)


def get_inline_kb_refuels(refuels: dict[int, RefuelGetDTO], changed_buttons: bool = False) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for id_refuel, refuel in refuels.items():
        if changed_buttons:
            builder.row(
                InlineKeyboardButton(text=f'Заправка {refuel.date.strftime('%d.%m.%Y')} числа',
                                     callback_data=f'change_refuel_{id_refuel}')
            )
        else:
            builder.row(
                InlineKeyboardButton(text=f'Заправка {refuel.date.strftime('%d.%m.%Y')} числа',
                                     callback_data=f'detail_refuel_{id_refuel}')
            )
    builder.adjust(1)
    return builder.as_markup()


def inline_choose_changed_parameters_refueling():
    inline_but = [
        [InlineKeyboardButton(text='Количество бензина', callback_data='update_amount_gasoline')],
        [InlineKeyboardButton(text='Пробег', callback_data='update_mileage')],
        [InlineKeyboardButton(text='Стоимость заправки', callback_data='update_cost_refueling')],
        [InlineKeyboardButton(text='Цена за литр бензина', callback_data='update_price_gasoline')],
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_but)


def get_inline_butt_back():
    but = InlineKeyboardButton(text='Обратно к списку заправок', callback_data='go_to_refuels')
    return InlineKeyboardMarkup(inline_keyboard=[[but]])
