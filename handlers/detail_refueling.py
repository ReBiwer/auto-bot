from aiogram import F
from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram.types import Message

from keyboards.inline import get_inline_butt_back
from keyboards.inline import get_inline_kb_refuels
from middlewares.refueling import RefuelsMiddleware
from utils.convert_data import get_refuels_info

detail_refueling_router = Router()
detail_refueling_router.message.middleware(RefuelsMiddleware())
detail_refueling_router.callback_query.middleware(RefuelsMiddleware())


@detail_refueling_router.message(Command("detail_refueling"))
async def get_all_refuels(message: Message, state: FSMContext):
    refuels = await get_refuels_info(state)
    if refuels:
        await message.answer(
            text="Выберите заправку. Ниже указана дата заправки",
            reply_markup=get_inline_kb_refuels(refuels),
        )
    else:
        await message.answer(text="У вас пока нет заправок")


@detail_refueling_router.callback_query(F.data.startswith("detail_refuel_"))
async def detail_refueling(call: CallbackQuery, state: FSMContext):
    refuel_id = int(call.data.replace("detail_refuel_", ""))
    refuels = await get_refuels_info(state)
    refuel = refuels[refuel_id]
    info = (
        f"Дата заправки: {refuel.date}\n"
        f"Пробег: {refuel.mileage}\n"
        f"Объем заправленного топлива: {refuel.amount_gasoline}\n"
        f"Стоимость заправки: {refuel.cost_refueling}\n"
        f"Цена за 1 литр: {refuel.price_gasoline}"
    )
    await call.message.answer(info, reply_markup=get_inline_butt_back())


@detail_refueling_router.callback_query(F.data == "go_to_refuels")
async def get_all_refuels(call: CallbackQuery, state: FSMContext):
    refuels = await get_refuels_info(state)
    await call.message.answer(
        text="Выберите заправку. Ниже указана дата заправки",
        reply_markup=get_inline_kb_refuels(refuels),
    )
