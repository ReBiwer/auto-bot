from typing import Any
from typing import Awaitable
from typing import Callable
from typing import Dict

from aiogram import BaseMiddleware
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram.types import Message

from db_settings.app_models import UserAppModel
from db_settings.DTO_models import UserChangeDTO
from db_settings.DTO_models import UserGetDTO


class UserDBMiddleware(BaseMiddleware):

    async def __call__(
        self,
        handler: Callable[[Message | CallbackQuery, Dict[str, Any]], Awaitable[Any]],
        event: Message | CallbackQuery,
        data: Dict[str, Any],
    ) -> Any:
        tg_id_user = event.from_user.id
        state: FSMContext = data["state"]
        state_data = await state.get_data()
        if "user" in state_data:
            return await handler(event, data)
        else:
            user_db = UserAppModel()
            user_data = {
                "username": event.from_user.username,
                "name": (event.from_user.first_name if event.from_user.first_name else None),
                "id_telegram": tg_id_user,
            }
            user = UserChangeDTO(**user_data)
            await user_db.add_user(user)
            info_user: UserGetDTO = await user_db.get_user(tg_id_user)
            await state.set_data({"user": info_user.model_dump_json()})
            return await handler(event, data)
