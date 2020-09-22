import pytest

from src import value


def test_hash_string():
    #
    """
    """
    assert value.hash_string(b"fnv", 3) == 0xb2f5cb99


@pytest.fixture
def array():
    #
    """
    """
    return value.ValueArray()


def test_init(array):
    #
    """
    """
    assert array.count == 0
    assert array.capacity == 0
    assert array.values is None


def test_write_value_array(array):
    #
    """
    """
    array.write_value_array(1.2)
    assert array.count == 1
    assert array.capacity == 8
    assert array.values[0] == 1.2


def test_free_value_array(array):
    #
    """
    """
    array.write_value_array(1.2)
    array.free_value_array()
    assert array.count == 0
    assert array.capacity == 0
    assert array.values is None
