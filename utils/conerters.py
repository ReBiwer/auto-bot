import re
from decimal import Decimal


def convert_to_decimal(value: str):
    decimal_pattern = r'\d{1,5},\w\w'
    re_value = re.search(decimal_pattern, value).group(0)
    new_value = re_value.replace(',', '.')
    return Decimal(new_value)
