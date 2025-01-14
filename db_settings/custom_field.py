import datetime
from decimal import Decimal
from typing import Annotated

from sqlalchemy import String, text
from sqlalchemy.types import TypeDecorator
from sqlalchemy.orm import mapped_column

str_256 = Annotated[str, 256]
pk = Annotated[int, mapped_column(primary_key=True)]
created_at = Annotated[datetime.datetime, mapped_column(server_default=text("TIMEZONE('utc-3', now())"))]


class DecimalField(TypeDecorator):
    impl = String

    def process_bind_param(self, value, dialect) -> str:
        """
        Функция для добавления значения в таблицу
        :param value: вставляемое значение в таблицу
        :param dialect: диалект используемой БД
        :return:
        """
        return str(value)

    def process_result_value(self, value, dialect) -> str:
        """
        Функция для получения значения из таблицы
        :param value: доставаемые данные из таблицы
        :param dialect: диалект используемой БД
        :return:
        """
        return str(value)
