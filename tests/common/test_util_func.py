import pytest

from lite_dist.common.util_func import to_bytes, is_power_of_two


@pytest.mark.parametrize(
    ["value", "expected"],
    [
        pytest.param(0, b"\x00"),
        pytest.param(1, b"\x01"),
        pytest.param(255, b"\xff"),
        pytest.param(65535, b"\xff\xff"),
    ]
)
def test_to_bytes(value: int, expected: bytes):
    actual = to_bytes(value)
    assert actual == expected


@pytest.mark.parametrize(
    ["value", "expected"],
    [
        pytest.param(0, False),
        pytest.param(1, True),
        pytest.param(2, True),
        pytest.param(3, False),
        pytest.param(4, True),
        pytest.param(65536, True),
    ]
)
def test_is_power_of_two(value: int, expected: bool):
    actual = is_power_of_two(value)
    assert actual == expected
