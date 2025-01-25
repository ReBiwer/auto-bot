from aiogram.fsm.context import FSMContext

from db_settings.DTO_models import UserGetDTO


async def get_user_info(state: FSMContext) -> UserGetDTO:
    """
    Функция для извлечения информации о пользователе сохраненной в state
    :param state: состояние, где храниться информация о пользователе
    :return: объект с информацией о пользователе
    """
    data_state = await state.get_data()
    user_data = data_state['user']
    return UserGetDTO.model_validate_json(user_data)
