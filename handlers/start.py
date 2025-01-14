from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message


from db_settings.db_models import UserORM

start_router = Router()


@start_router.message(CommandStart())
async def start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer('Приветствую. \n'
                         'Я бот Быкова Владимир.\n'
                         'Создан для личных нужд создателя.\n'
                         'Что я умею:\n'
                         '<em>- Собирать данные о заправке машины</em>')
