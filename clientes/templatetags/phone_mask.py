import re
from django import template

register = template.Library()

@register.filter
def mask_phone(value):
    digits = re.sub(r"\D", "", str(value or ""))
    if len(digits) > 11 and digits.startswith("55"):
        digits = digits[2:]
    if len(digits) < 4:
        return "***"
    dd = digits[:2]
    rest = digits[2:]
    final = digits[-2:]
    if len(digits) == 11:  # móvel: (85) 9 8***-**72
        return f"({dd}) {rest[0]} {rest[1]}***-**{final}"
    if len(digits) == 10:  # fixo: (85) 8***-**72
        return f"({dd}) {rest[0]}***-**{final}"
    hidden = len(digits) - 4
    return f"({dd}) {'*' * hidden}-{final}"
