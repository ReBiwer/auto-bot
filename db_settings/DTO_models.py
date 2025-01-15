from datetime import datetime
from typing import Optional
from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class UserChangeDTO(BaseModel):
    """
    Класс для валидации данных при добавлении пользователя
    """
    username: str
    name: Optional[str]
    id_telegram: int


class UserGetDTO(UserChangeDTO):
    """
    Класс для валидации данных при извлечении данных
    """
    id: int


class RefuelChangeDTO(BaseModel):
    """
    Класс для валидации данных при добавлении заправки
    """
    id: int | None
    user_id: int
    amount_gasoline: str
    mileage: str
    cost_refueling: str
    price_gasoline: str


class RefuelGetDTO(BaseModel):
    """
    Класс для валидации данных при извлечении данных
    """
    id: int
    date: datetime
    user_id: int
    amount_gasoline: Decimal
    mileage: Decimal
    cost_refueling: Decimal
    price_gasoline: Decimal
    user: UserGetDTO
