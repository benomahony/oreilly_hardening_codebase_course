import pytest

def test_unspecific_error():
    with pytest.raises(Exception):
        raise TypeError("an unrelated bug also passes")
