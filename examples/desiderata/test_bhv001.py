from unittest.mock import MagicMock

def test_mocked_reservation():
    stock = MagicMock()
    stock.reserve.return_value = 7
    assert stock.reserve(3) == 7
