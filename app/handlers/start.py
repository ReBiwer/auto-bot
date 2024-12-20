from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message


from db_handler.models import UserTable

start_router = Router()


@start_router.message(CommandStart())
async def start(message: Message, user_table: UserTable):
    await message.answer('Запуск сообщения по команде /start используя фильтр CommandStart()')
