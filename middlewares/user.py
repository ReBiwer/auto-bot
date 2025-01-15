from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from db_settings.app_models import UserAppModel
from db_settings.db_models import User
from db_settings.DTO_models import UserChangeDTO, UserGetDTO


class UserDBMiddleware(BaseMiddleware):

    async def __call__(
            self,
            handler: Callable[[Message | CallbackQuery, Dict[str, Any]], Awaitable[Any]],
            event: Message | CallbackQuery,
            data: Dict[str, Any]) -> Any:
        tg_id_user = event.from_user.id
        if 'user' in data:
            return await handler(event, data)
        else:
            user_db = UserAppModel()
            user_data = {
                'username': event.from_user.username,
                'name': event.from_user.first_name if event.from_user.first_name else None,
                'id_telegram': tg_id_user,
            }
            user = UserChangeDTO(**user_data)
            await user_db.add_user(user)
            data["user"] = user
            return await handler(event, data)
