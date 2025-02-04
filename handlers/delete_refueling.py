import asyncio

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.utils.chat_action import ChatActionSender

from create_bot import bot
from db_settings.DTO_models import RefuelGetDTO
from keyboards.inline import get_inline_kb_refuels, inline_confirm_buttons
from db_settings.app_models import RefuelingAppModel
from middlewares.refueling import RefuelsMiddleware

delete_refueling_router = Router()
delete_refueling_router.message.middleware(RefuelsMiddleware())


class DeleteRefuel(StatesGroup):
    refuels = State()
    confirmation = State()


@delete_refueling_router.message(Command("delete_refueling"))
async def get_all_refuels(
    message: Message, state: FSMContext, refuels: dict[int, RefuelGetDTO] | None
):
    if refuels:
        serialized_refuels = {
            key: refuel.model_dump_json() for key, refuel in refuels.items()
        }
        await state.set_state(DeleteRefuel.refuels)
        await state.update_data(refuels=serialized_refuels)
        await message.answer(
            text="Какую заправку вы хотите удалить?",
            reply_markup=get_inline_kb_refuels(refuels, delete_buttons=True),
        )
    else:
        await message.answer(text="У вас пока нет заправок")


@delete_refueling_router.callback_query(
    F.data.startswith("delete_refuel_"), DeleteRefuel.refuels
)
async def confirm_delete_refuel(call: CallbackQuery, state: FSMContext):
    data_from_state = await state.get_data()
    refuel_id = int(call.data.replace("delete_refuel_", ""))
    await state.set_data({"refuel_id": refuel_id})
    await state.set_state(DeleteRefuel.confirmation)
    refuel_json = data_from_state["refuels"][str(refuel_id)]
    info_delete_refuel: RefuelGetDTO = RefuelGetDTO.model_validate_json(refuel_json)
    async with ChatActionSender.typing(bot=bot, chat_id=call.message.chat.id):
        await asyncio.sleep(2)
        await call.message.answer(
            text=f"Подтвердите удаление заправки.\n"
            f"Дата заправки: {info_delete_refuel.formated_date}\n"
            f"Пробег: {info_delete_refuel.mileage}\n"
            f"Объем заправленного топлива: {info_delete_refuel.amount_gasoline}\n"
            f"Стоимость заправки: {info_delete_refuel.cost_refueling}\n"
            f"Цена за 1 литр: {info_delete_refuel.price_gasoline}\n",
            reply_markup=inline_confirm_buttons(),
        )


@delete_refueling_router.callback_query(F.data == "confirm", DeleteRefuel.confirmation)
async def delete_refuel(call: CallbackQuery, state: FSMContext):
    refuel_db = RefuelingAppModel()
    data_from_state = await state.get_data()
    refuel_id = int(data_from_state["refuel_id"])
    await refuel_db.delete_refuel(refuel_id)
    await call.message.answer(text="Заправка успешно удалено")
    await state.set_state()


@delete_refueling_router.callback_query(
    F.data == "not_confirm", DeleteRefuel.confirmation
)
async def not_confirm_delete(call: CallbackQuery, state: FSMContext):
    await state.set_state()
    await call.message.answer(text="Удаление заправки прервано")
