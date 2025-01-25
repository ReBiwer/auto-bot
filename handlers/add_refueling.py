import asyncio
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery
from aiogram.utils.chat_action import ChatActionSender

from create_bot import bot
from keyboards.inline import get_inline_kb_check_data
from utils.conerters import search_numbers_in_strings
from db_settings.app_models import RefuelingAppModel
from db_settings.DTO_models import UserGetDTO, RefuelChangeDTO
from utils.convert_user_data import get_user_info

add_refuel_router = Router()


class Refuel(StatesGroup):
    user_id = State()
    amount_gasoline = State()
    mileage = State()
    cost_refueling = State()
    price_gasoline = State()
    check_state = State()


@add_refuel_router.message(Command('add_refueling'))
async def add_refueling_start(message: Message, state: FSMContext):
    """
    Стартовый хэндлер, где начинается сбор данных заправки для добавления
    :param message: сообщение
    :param state: состояние, где сохраняются все данные заправки
    :return:
    """
    await state.set_state(Refuel.user_id)
    user = await get_user_info(state)
    await state.update_data(user_id=user.id)
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        await asyncio.sleep(2)
        await message.answer('Сколько литров заправили?')
    await state.set_state(Refuel.amount_gasoline)


@add_refuel_router.message(Refuel.amount_gasoline)
async def add_refueling_amount(message: Message, state: FSMContext):
    """
    Хэндлер, где сохраняется кол-во заправленного бензина и запрашивается пробег
    :param message:
    :param state:
    :return:
    """
    amount_gasoline = search_numbers_in_strings(message.text)
    if amount_gasoline:
        await state.update_data(amount_gasoline=amount_gasoline)
        async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
            await asyncio.sleep(2)
            await message.answer('Сколько километров пробег?')
        await state.set_state(Refuel.mileage)
    else:
        async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
            await asyncio.sleep(2)
            await message.answer('Введите корректное значение')


@add_refuel_router.message(Refuel.mileage)
async def add_refueling_mileage(message: Message, state: FSMContext):
    """
    Хэндлер, где сохраняется пробег и запрашивается стоимость заправки
    :param message:
    :param state:
    :return:
    """
    mileage = search_numbers_in_strings(message.text)
    if mileage:
        await state.update_data(mileage=mileage)
        async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
            await asyncio.sleep(2)
            await message.answer('Сколько стоила заправка?')
        await state.set_state(Refuel.cost_refueling)
    else:
        async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
            await asyncio.sleep(2)
            await message.answer('Введите корректное значение')


@add_refuel_router.message(Refuel.cost_refueling)
async def add_refueling_cost(message: Message, state: FSMContext):
    """
    Хэндлер, где сохраняется кол-во стоимость заправки и запрашивается цена за 1 литр бензина
    :param message:
    :param state:
    :return:
    """
    cost_refueling = search_numbers_in_strings(message.text)
    if cost_refueling:
        await state.update_data(cost_refueling=cost_refueling)
        async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
            await asyncio.sleep(2)
            await message.answer('Какая цена бензина за 1 литр?')
        await state.set_state(Refuel.price_gasoline)
    else:
        async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
            await asyncio.sleep(2)
            await message.answer('Введите корректное значение')


@add_refuel_router.message(Refuel.price_gasoline)
async def add_refueling_price(message: Message, state: FSMContext):
    """
    Хэндлер, где сохраняется цена за 1 литр бензина и запрашивается подтверждение полученных данных
    :param message:
    :param state:
    :return:
    """
    price_gasoline = search_numbers_in_strings(message.text)
    await state.update_data(price_gasoline=price_gasoline)
    data = await state.get_data()
    check_text = (f'Проверьте введенные данные перед сохранением:\n'
                  f'<b>Заправлено:</b> {data.get('amount_gasoline')} л\n'
                  f'<b>Пробег:</b> {data.get('mileage')} км\n'
                  f'<b>Стоимость заправки:</b> {data.get('cost_refueling')} руб\n'
                  f'<b>Цена бензина:</b> {data.get('price_gasoline')} руб/л\n')
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        await asyncio.sleep(2)
        await message.answer(check_text, reply_markup=get_inline_kb_check_data())
    await state.set_state(Refuel.check_state)


@add_refuel_router.callback_query(F.data == 'correct', Refuel.check_state)
async def add_refueling_correct_data(call: CallbackQuery, state: FSMContext):
    """
    Хэндлер, где сохраняется заправка в БД
    :param call:
    :param state:
    :return:
    """
    data = await state.get_data()
    refuel = RefuelingAppModel()
    await state.set_state()
    refuel_data = {
        'user_id': data.get('user_id'),
        'amount_gasoline': data.get('amount_gasoline'),
        'mileage': data.get('mileage'),
        'cost_refueling': data.get('cost_refueling'),
        'price_gasoline': data.get('price_gasoline'),
    }
    refuel_dto = RefuelChangeDTO(**refuel_data)
    await refuel.add_refueling(refuel_dto)
    await call.message.answer('Данные успешно добавлены')


@add_refuel_router.callback_query(F.data == 'incorrect', Refuel.check_state)
async def add_refueling_incorrect_data(call: CallbackQuery, state: FSMContext):
    """
    Хэндлер, где происходит повторный сбор данных
    :param call:
    :param state:
    :return:
    """
    async with ChatActionSender.typing(bot=bot, chat_id=call.message.chat.id):
        await asyncio.sleep(2)
        await call.message.answer('Заполните заново.\nСколько литров заправили?')
    await state.set_state(Refuel.amount_gasoline)
