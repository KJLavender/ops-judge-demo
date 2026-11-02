from src.calc import total


def test_total_adds_tax():
    assert total([10.0, 20.0]) == 31.5


def test_empty_order():
    assert total([]) == 0
