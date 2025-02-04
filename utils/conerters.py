import re
from decimal import Decimal


def search_numbers_in_strings(value: str) -> str | None:
    """
    Находит число в строке
    :param value: строка, где имеется число
    :return: str | None: число содержащиеся в строке (value) или None если нет числа
    """
    try:
        processed_value = value.replace(",", ".").replace("\n", "")
        decimal_pattern = r"\d+\.\d+"
        re_value = re.search(
            decimal_pattern,
            processed_value,
        ).group(0)
        return str(re_value)
    except AttributeError:
        return None
