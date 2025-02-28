from datetime import datetime
from decimal import Decimal
from typing import Any
from typing import Optional

from pydantic import BaseModel
from pydantic import field_validator
from typing_extensions import Self


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

    id: Optional[int] = None
    user_id: int
    amount_gasoline: str
    mileage: str
    cost_refueling: str
    price_gasoline: str

    @field_validator("amount_gasoline", mode="before")
    def validate_amount_gasoline(cls, value):
        return str(value)

    @field_validator("mileage", mode="before")
    def validate_mileage(cls, value):
        return str(value)

    @field_validator("cost_refueling", mode="before")
    def validate_cost_refueling(cls, value):
        return str(value)

    @field_validator("price_gasoline", mode="before")
    def validate_price_gasoline(cls, value):
        return str(value)


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

    @property
    def formated_date(self):
        return self.date.strftime("%d.%m.%Y")
