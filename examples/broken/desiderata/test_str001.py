from unittest.mock import Mock

def test_internal_call_order():
    stock = Mock()
    stock.reserve(3)
    stock.reserve.assert_called_with(3)
