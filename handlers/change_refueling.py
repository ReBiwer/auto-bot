import asyncio

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message
from aiogram.utils.chat_action import ChatActionSender

from create_bot import bot
from db_settings.app_models import RefuelingAppModel
from db_settings.DTO_models import RefuelChangeDTO, RefuelGetDTO
from keyboards.inline import (
    get_inline_kb_refuels,
    inline_choose_changed_parameters_refueling,
)
from middlewares.refueling import RefuelsMiddleware
from utils.conerters import search_numbers_in_strings
from utils.convert_data import get_refuels_info

change_refueling_router = Router()
change_refueling_router.message.middleware(RefuelsMiddleware())

params_refuel = {
    "amount_gasoline": "количество заправленного бензина",
    "mileage": "пробег",
    "cost_refueling": "стоимость заправки",
    "price_gasoline": "цену за литр бензина",
}


class ChangeRefuel(StatesGroup):
    refuels = State()
    changeable_refuel = State()
    changeable_param = State()


@change_refueling_router.message(Command("change_refueling"))
async def get_all_refuels(message: Message, state: FSMContext):
    """
    Стартовый хэндлер. Выдает имеющиеся заправки в inline клавиатуры.
    :param message: Сообщение от пользователя
    :param state: Состояние где хранится вся закешированная информация
    :return:
    """
    refuels = await get_refuels_info(state)
    if refuels:
        await state.set_state(ChangeRefuel.refuels)
        await message.answer(
            text="Какую заправку вы хотите изменить?",
            reply_markup=get_inline_kb_refuels(refuels, change_buttons=True),
        )
    else:
        await message.answer(text="У вас пока нет заправок")


@change_refueling_router.callback_query(
    F.data.startswith("change_refuel_"), ChangeRefuel.refuels
)
async def change_refueling(call: CallbackQuery, state: FSMContext):
    """
    Хэндлер, где сохраняется id заправки, которую нужно изменить.
    Дальше идет запрос какую именно характеристику нужно изменить
    :param call:
    :param state:
    :return:
    """
    await state.set_state(ChangeRefuel.changeable_refuel)
    refuel_id = int(call.data.replace("change_refuel_", ""))
    refuels = await get_refuels_info(state)
    refuel_info = refuels[refuel_id]
    changeable_refuel: RefuelChangeDTO = RefuelChangeDTO.model_validate(refuel_info)
    await state.update_data(changeable_refuel=changeable_refuel.model_dump_json())
    async with ChatActionSender.typing(bot=bot, chat_id=call.message.chat.id):
        await asyncio.sleep(2)
        await call.message.answer(
            "Что хотите изменить?",
            reply_markup=inline_choose_changed_parameters_refueling(),
        )


@change_refueling_router.callback_query(
    F.data.startswith("update_"), ChangeRefuel.changeable_refuel
)
async def change_params_refuel(call: CallbackQuery, state: FSMContext):
    """
    Хэндлер, где сохраняется имя атрибута, которое нужно изменить.
    Дальше идет запрос нового значения.
    :param call:
    :param state:
    :return:
    """
    await state.set_state(ChangeRefuel.changeable_param)
    key_param_refuel = call.data.replace("update_", "")
    name_param_refuel = params_refuel[key_param_refuel]
    async with ChatActionSender.typing(bot=bot, chat_id=call.message.chat.id):
        await asyncio.sleep(2)
        data_from_state = await state.get_data()
        changeable_refuel: RefuelChangeDTO = RefuelChangeDTO.model_validate_json(
            data_from_state["changeable_refuel"]
        )
        cur_value = changeable_refuel.__getattr__(key_param_refuel)
        await call.message.answer(
            f"Текущее значение: {cur_value}\n" f"Введите {name_param_refuel}"
        )


@change_refueling_router.message(ChangeRefuel.changeable_param)
async def save_param_refuel(message: Message, state: FSMContext):
    """
    Хэндлер, где собирается вся информация и сохраняется в базе данных.
    :param message:
    :param state:
    :return:
    """
    new_value_param = search_numbers_in_strings(message.text)
    data_from_state = await state.get_data()
    changeable_param = data_from_state["changeable_param"]
    changeable_refuel: RefuelChangeDTO = RefuelChangeDTO.model_validate_json(
        data_from_state["changeable_refuel"]
    )
    changeable_refuel.__setattr__(changeable_param, new_value_param)
    refuel_app_model = RefuelingAppModel()
    await refuel_app_model.update_refuel(changeable_refuel)
    await message.answer(text="Данные успешно изменены")
    await state.set_state()
