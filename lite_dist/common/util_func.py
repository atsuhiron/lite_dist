import binascii


def from_hex(hex_str: str) -> int:
    return int("0x" + hex_str, base=16)


def to_hex(val: int) -> str:
    return hex(val)[2:]


def to_bytes(val: int) -> bytes:
    hex_str = hex(val)[2:]
    if len(hex_str) % 2 == 1:
        hex_str = "0" + hex_str
    return binascii.unhexlify(hex_str)


def is_power_of_two(n: int) -> bool:
    if n <= 0:
        return False
    return (n & (n - 1)) == 0
