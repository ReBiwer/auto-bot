from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from db_settings.app_models import RefuelingAppModel
from db_settings.DTO_models import RefuelGetDTO


class RefuelsMiddleware(BaseMiddleware):
    """
    Middleware для получения всех заправок пользователя, если они есть
    """

    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        tg_id_user = event.from_user.id
        state: FSMContext = data["state"]
        state_data = await state.get_data()
        if "refuels" in state_data:
            return await handler(event, data)
        else:
            refuel_orm = RefuelingAppModel()
            refuels: dict[int, RefuelGetDTO] = await refuel_orm.get_refuels(tg_id_user)
            await state.set_data(
                {
                    "refuels": {
                        key: refuel.model_dump_json() for key, refuel in refuels.items()
                    }
                }
            )
            return await handler(event, data)
