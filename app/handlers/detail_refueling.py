from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from app.db_handler.models import RefuelingTable
from app.middlewares.refueling import RefuelsMiddleware
from app.keyboards.inline import get_inline_kb_refuels, get_inline_butt_back

detail_refueling_router = Router()
detail_refueling_router.message.middleware(RefuelsMiddleware())
detail_refueling_router.callback_query.middleware(RefuelsMiddleware())


@detail_refueling_router.message(Command('detail_refueling'))
async def get_all_refuels(message: Message, refuels: dict[int, RefuelingTable]):
    await message.answer(text='Выберите заправку. Ниже указана дата заправки',
                         reply_markup=get_inline_kb_refuels(refuels))


@detail_refueling_router.callback_query(F.data.startswith('detail_refuel_'))
async def detail_refueling(call: CallbackQuery, refuels: dict[int, RefuelingTable]):
    refuel_id = int(call.data.replace('detail_refuel_', ''))
    refuel = refuels[refuel_id]
    info = (f'Дата заправки: {refuel.date}\n'
            f'Пробег: {refuel.mileage}\n'
            f'Объем заправленного топлива: {refuel.amount_gasoline}\n'
            f'Стоимость заправки: {refuel.cost_refueling}\n'
            f'Цена за 1 литр: {refuel.price_gasoline}')
    await call.message.answer(info, reply_markup=get_inline_butt_back())


@detail_refueling_router.callback_query(F.data == 'go_to_refuels')
async def get_all_refuels(call: CallbackQuery, refuels: dict[int, RefuelingTable]):
    await call.message.answer(text='Выберите заправку. Ниже указана дата заправки',
                              reply_markup=get_inline_kb_refuels(refuels))
