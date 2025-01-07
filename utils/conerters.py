import re
from decimal import Decimal


def convert_to_decimal(value: str):
    """
    Конвертирует строку в Decimal
    :param value: строка, где имеется число
    :return: Decimal число содержащиеся в строке (value)
    """
    processed_value = (value
                       .replace(',', '.')
                       .replace(' ', '')
                       .replace('\n', '')
                       )
    decimal_pattern = r'\d{1,}.\d{2}'
    re_value = re.search(
        decimal_pattern,
        processed_value,
    ).group(0)
    return Decimal(re_value)
