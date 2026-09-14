from unittest.mock import Mock, patch

def test_mocked_outcome():
    reservation = Mock()
    reservation.return_value = 7
    assert reservation(10, 3) == 7

@patch("reservations.domain.stock.reserve")
def test_patched_domain(reserve):
    reserve.return_value = 7
    assert reserve(10, 3) == 7

def test_mock_fixture(mocker):
    mocker.patch("reservations.domain.stock.reserve")
