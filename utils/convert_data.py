from aiogram.fsm.context import FSMContext

from db_settings.DTO_models import UserGetDTO, RefuelGetDTO


async def get_user_info(state: FSMContext) -> UserGetDTO:
    """
    Функция для извлечения информации о пользователе сохраненной в state
    :param state: состояние, где храниться информация о пользователе
    :return: объект с информацией о пользователе
    """
    data_state = await state.get_data()
    user_data = data_state['user']
    return UserGetDTO.model_validate_json(user_data)


async def get_refuels_info(state: FSMContext) -> dict[int, RefuelGetDTO] | None:
    """
    Функция для извлечения информации о заправках сохраненной в state
    :param state:
    :return:
    """
    data_state = await state.get_data()
    if data_state['refuels'] is not None:
        refuels_data: dict[int, str] = data_state['refuels']
        refuels = {
            key: RefuelGetDTO.model_validate_json(refuel)
            for key, refuel in refuels_data.items()
        }
        return refuels
    else:
        return None
