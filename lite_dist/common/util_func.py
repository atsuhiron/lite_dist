def from_hex(hex_str: str) -> int:
    return int("0x" + hex_str, base=16)


def to_hex(val: int) -> str:
    return hex(val)[2:]
