from django.core.exceptions import ValidationError


def validation_hex(value):
    if value[0] != "#" and len(value) < 7:
        raise ValidationError(
            "Оформите цвет в HEX формате. Пример: #000000"
        )
