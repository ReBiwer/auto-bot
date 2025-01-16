import asyncio

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.utils.chat_action import ChatActionSender

from create_bot import bot
from utils.conerters import search_numbers_in_strings
from db_settings.app_models import RefuelingAppModel
from db_settings.DTO_models import RefuelGetDTO, RefuelChangeDTO
from middlewares.refueling import RefuelsMiddleware
from keyboards.inline import get_inline_kb_refuels, inline_choose_changed_parameters_refueling


change_refueling_router = Router()
change_refueling_router.message.middleware(RefuelsMiddleware())

params_refuel = {
    'amount_gasoline': 'количество заправленного бензина',
    'mileage': 'пробег',
    'cost_refueling': 'стоимость заправки',
    'price_gasoline': 'цену за литр бензина',
}


class ChangeRefuel(StatesGroup):
    refuels = State()
    changeable_refuel = State()
    changeable_param = State()


@change_refueling_router.message(Command('change_refueling'))
async def get_all_refuels(message: Message, state: FSMContext, refuels: dict[int, RefuelGetDTO]):
    await state.set_state(ChangeRefuel.refuels)
    await state.update_data(refuels=refuels)
    await message.answer(text='Какую заправку вы хотите изменить?',
                         reply_markup=get_inline_kb_refuels(refuels, changed_buttons=True))


@change_refueling_router.callback_query(F.data.startswith('change_refuel_'), ChangeRefuel.refuels)
async def change_refueling(call: CallbackQuery, state: FSMContext):
    await state.set_state(ChangeRefuel.changeable_refuel)
    refuel_id = int(call.data.replace('change_refuel_', ''))
    refuels = await state.get_data()
    refuel_info: RefuelGetDTO = refuels['refuels'][refuel_id]
    changeable_refuel: RefuelChangeDTO = RefuelChangeDTO(**refuel_info.model_dump())
    await state.update_data(changeable_refuel=changeable_refuel)
    async with ChatActionSender.typing(bot=bot, chat_id=call.message.chat.id):
        await asyncio.sleep(2)
        await call.message.answer('Что хотите изменить?',
                                  reply_markup=inline_choose_changed_parameters_refueling())


@change_refueling_router.callback_query(F.data.startswith('change_'), ChangeRefuel.changeable_refuel)
async def change_params_refuel(call: CallbackQuery, state: FSMContext):
    await state.set_state(ChangeRefuel.changeable_param)
    key_param_refuel = call.data.replace('change_', '')
    await state.update_data(changed_param=key_param_refuel)
    name_param_refuel = params_refuel[key_param_refuel]
    async with ChatActionSender.typing(bot=bot, chat_id=call.message.chat.id):
        await asyncio.sleep(2)
        await call.message.answer(f'Введите {name_param_refuel}')


@change_refueling_router.message(ChangeRefuel.changeable_param)
async def save_param_refuel(message: Message, state: FSMContext):
    new_value_param = search_numbers_in_strings(message.text)
    data_from_state = await state.get_data()
    changeable_param = data_from_state['changeable_param']
    changeable_refuel: RefuelChangeDTO = data_from_state['changeable_refuel']
    changeable_refuel.__setattr__(changeable_param, new_value_param)
    refuel_app_model = RefuelingAppModel()
    await refuel_app_model.update_refuel(changeable_refuel)
    await state.clear()
