from aiogram.types import InlineKeyboardButton
from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from db_settings.DTO_models import RefuelGetDTO


def get_inline_kb_check_data() -> InlineKeyboardMarkup:
    inline_but = [
        [InlineKeyboardButton(text="Все верно", callback_data="correct")],
        [InlineKeyboardButton(text="Не верно", callback_data="incorrect")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_but)


def get_inline_kb_refuels(
    refuels: dict[int, RefuelGetDTO],
    change_buttons: bool = False,
    delete_buttons: bool = False,
) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for id_refuel, refuel in refuels.items():
        if change_buttons and not delete_buttons:
            callback_data = f"change_refuel_{id_refuel}"
        elif delete_buttons and not change_buttons:
            callback_data = f"delete_refuel_{id_refuel}"
        elif not change_buttons and not delete_buttons:
            callback_data = f"detail_refuel_{id_refuel}"
        else:
            raise ValueError(
                f"В функцию нужно передать только один из аргументов change_buttons и delete_buttons. "
                f"Текущие аргументы: {change_buttons=}, {delete_buttons=}"
            )
        builder.row(
            InlineKeyboardButton(
                text=f"Заправка {refuel.formated_date} числа",
                callback_data=callback_data,
            )
        )
    builder.adjust(1)
    return builder.as_markup()


def inline_confirm_buttons():
    inline_but = [
        [InlineKeyboardButton(text="Подтверждаю", callback_data="confirm")],
        [InlineKeyboardButton(text="Не подтверждаю", callback_data="not_confirm")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_but)


def inline_choose_changed_parameters_refueling():
    inline_but = [
        [InlineKeyboardButton(text="Количество бензина", callback_data="update_amount_gasoline")],
        [InlineKeyboardButton(text="Пробег", callback_data="update_mileage")],
        [InlineKeyboardButton(text="Стоимость заправки", callback_data="update_cost_refueling")],
        [InlineKeyboardButton(text="Цена за литр бензина", callback_data="update_price_gasoline")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_but)


def get_inline_butt_back():
    but = InlineKeyboardButton(text="Обратно к списку заправок", callback_data="go_to_refuels")
    return InlineKeyboardMarkup(inline_keyboard=[[but]])
