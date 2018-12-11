import typing


def hex_id(obj: typing.Any) -> str:
    return hex(id(obj))


def none_or_hex_id(obj: typing.Any) -> typing.Optional[str]:
    return hex_id(obj) if obj is not None else None
