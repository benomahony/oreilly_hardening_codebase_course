import pytest

@pytest.mark.xfail
def test_hidden_failure():
    assert False
