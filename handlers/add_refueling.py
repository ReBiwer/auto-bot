import asyncio
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery
from aiogram.utils.chat_action import ChatActionSender

from create_bot import bot
from keyboards.inline import get_inline_kb_check_data
from utils.conerters import convert_to_decimal
from db_handler.models import UserTable
from db_handler.orm import RefuelingORM

add_refuel_router = Router()


class Refuel(StatesGroup):
    user_id = State()
    amount_gasoline = State()
    mileage = State()
    cost_refueling = State()
    price_gasoline = State()
    check_state = State()


@add_refuel_router.message(Command('add_refueling'))
async def add_refueling_start(message: Message, state: FSMContext, user_table: UserTable):
    await state.clear()
    await state.set_state(Refuel.user_id)
    await state.update_data(user_id=user_table.id)
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        await asyncio.sleep(2)
        await message.answer('Сколько литров заправили?')
    await state.set_state(Refuel.amount_gasoline)


@add_refuel_router.message(Refuel.amount_gasoline)
async def add_refueling_amount(message: Message, state: FSMContext):
    amount_gasoline = convert_to_decimal(message.text)
    await state.update_data(amount_gasoline=amount_gasoline)
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        await asyncio.sleep(2)
        await message.answer('Сколько километров пробег?')
    await state.set_state(Refuel.mileage)


@add_refuel_router.message(Refuel.mileage)
async def add_refueling_mileage(message: Message, state: FSMContext):
    mileage = convert_to_decimal(message.text)
    await state.update_data(mileage=mileage)
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        await asyncio.sleep(2)
        await message.answer('Сколько стоила заправка?')
    await state.set_state(Refuel.cost_refueling)


@add_refuel_router.message(Refuel.cost_refueling)
async def add_refueling_cost(message: Message, state: FSMContext):
    cost_refueling = convert_to_decimal(message.text)
    await state.update_data(cost_refueling=cost_refueling)
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        await asyncio.sleep(2)
        await message.answer('Какая цена бензина за 1 литр?')
    await state.set_state(Refuel.price_gasoline)


@add_refuel_router.message(Refuel.price_gasoline)
async def add_refueling_price(message: Message, state: FSMContext):
    price_gasoline = convert_to_decimal(message.text)
    await state.update_data(price_gasoline=price_gasoline)
    data = await state.get_data()
    check_text = (f'Проверьте введенные данные перед сохранением:\n'
                  f'<b>Количество заправленного бензина:</b> {data.get('amount_gasoline')}\n'
                  f'<b>Пробег:</b> {data.get('mileage')}\n'
                  f'<b>Стоимость заправки:</b> {data.get('cost_refueling')}\n'
                  f'<b>Цена бензина за 1 литр:</b> {data.get('price_gasoline')}\n')
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        await asyncio.sleep(2)
        await message.answer(check_text, reply_markup=get_inline_kb_check_data())
    await state.set_state(Refuel.check_state)


@add_refuel_router.callback_query(F.data == 'correct', Refuel.check_state)
async def add_refueling_correct_data(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    refuel = RefuelingORM()
    await state.clear()
    await refuel.add_refueling(
        id_user=data.get('user_id'),
        amount_gasoline=data.get('amount_gasoline'),
        mileage=data.get('mileage'),
        cost_refueling=data.get('cost_refueling'),
        price_gasoline=data.get('price_gasoline')
    )
    await call.message.answer('Данные успешно добавлены')


@add_refuel_router.callback_query(F.data == 'incorrect', Refuel.check_state)
async def add_refueling_incorrect_data(call: CallbackQuery, state: FSMContext):
    async with ChatActionSender.typing(bot=bot, chat_id=call.message.chat.id):
        await asyncio.sleep(2)
        await call.message.answer('Заполните заново.\nСколько литров заправили?')
    await state.set_state(Refuel.amount_gasoline)
