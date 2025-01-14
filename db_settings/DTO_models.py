from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class UserAddDTO(BaseModel):
    """
    Класс для валидации данных при добавлении пользователя
    """
    username: str
    name: Optional[str]
    id_telegram: int


class UserGetDTO(UserAddDTO):
    """
    Класс для валидации данных при извлечении данных
    """
    id: int
    refuelings: list["RefuelAddDTO"]


class RefuelAddDTO(BaseModel):
    """
    Класс для валидации данных при добавлении заправки
    """
    user_id: int
    amount_gasoline: str
    mileage: str
    cost_refueling: str
    price_gasoline: str


class RefuelGetDTO(RefuelAddDTO):
    """
    Класс для валидации данных при извлечении данных
    """
    id: int
    date: datetime
    user: UserGetDTO
