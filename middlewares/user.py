from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from db_settings.app_models import UserAppModel
from db_settings.db_models import User


class UserDBMiddleware(BaseMiddleware):

    async def __call__(
            self,
            handler: Callable[[Message | CallbackQuery, Dict[str, Any]], Awaitable[Any]],
            event: Message | CallbackQuery,
            data: Dict[str, Any]) -> Any:
        tg_id_user = event.from_user.id
        user_db = UserAppModel()
        user_db.create_table()
        user: User = await user_db.get_user(tg_id_user)
        if user:
            data["user_table"] = user
            return await handler(event, data)
        else:
            username = event.from_user.username
            name = event.from_user.first_name
            await user_db.add_user(username=username, name=name, id_telegram=tg_id_user)
            user: User = await user_db.get_user(tg_id_user)
            data["user_table"] = user
            return await handler(event, data)
