import pytest

from src import obj


def test_copy_string():
    #
    """Checks obj.copy_string converts strings as intended."""
    item = obj.copy_string("", 0)

    assert item.obj.is_string()
    assert item.length == 0
    assert item.chars == ['\x00']
    assert item.hash_value == obj.FNV_32_INIT

    assert obj.copy_string("hi", 2).chars == ['h', 'i','\x00']
    assert obj.copy_string("hi", 1).chars == ['h', '\x00']
    assert obj.copy_string("hi", 0).chars == ['\x00']

    with pytest.raises(IndexError):
        assert obj.copy_string("hi", 3).chars == ['h', 'i','\x00']
