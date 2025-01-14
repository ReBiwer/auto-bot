from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message
from db_settings.app_models import RefuelingAppModel
from db_settings.db_models import Refueling


class RefuelsMiddleware(BaseMiddleware):
    """
    Middleware для получения всех заправок пользователя, если они есть
    """

    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]) -> Any:
        tg_id_user = event.from_user.id
        refuel_orm = RefuelingAppModel()
        refuels: dict[int, Refueling] = await refuel_orm.get_refuels(tg_id_user)
        if refuels:
            data["refuels"] = refuels
        else:
            data["refuels"] = None
        return await handler(event, data)
