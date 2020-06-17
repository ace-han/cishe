import pytest


@pytest.mark.parametrize("a, b, c", [(1, 2, 3), (2, 3, 5), (3, 5, 8)])
def test_xxx(a, b, c):
    assert a + b == c
