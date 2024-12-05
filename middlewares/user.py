from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message
from db_handler.orm import UserORM
from db_handler.models import UserTable


class MyMiddleware(BaseMiddleware):

    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]) -> Any:
        tg_id_user = event.from_user.id
        user_db = UserORM()
        user: UserTable = await user_db.get_user(tg_id_user)
        if user:
            data["user_table"] = user
            return await handler(event, data)
        else:
            username = event.from_user.username
            name = event.from_user.first_name
            user_db.add_user(username=username, name=name, id_telegram=tg_id_user)
            user: UserTable = await user_db.get_user(tg_id_user)
            data["user_table"] = user
            return await handler(event, data)
