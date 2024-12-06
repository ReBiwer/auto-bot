from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message
from db_handler.orm import RefuelingORM
from db_handler.models import RefuelingTable


class RefuelsMiddleware(BaseMiddleware):

    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]) -> Any:
        tg_id_user = event.from_user.id
        refuel_orm = RefuelingORM()
        refuels: list[RefuelingTable] = await refuel_orm.get_refuels(tg_id_user)
        if refuels:
            data["refuels"] = refuels
            return await handler(event, data)

