import pytest

from src import value


def test_allocate_object():
    # type: () -> None
    """Checks allocate_objects creates a container as intended."""
    item = value.allocate_object(size=8, object_type=value.ObjectType.OBJ_STRING)

    assert item.object_type == value.ObjectType.OBJ_STRING
    assert item.obj == [None] * 8


def test_copy_string():
    # type: () -> None
    """Checks copy_string converts strings as intended."""
    item = value.copy_string("", 0)

    assert value.copy_string("hi", 2).chars == ['h', 'i', '\x00']
    assert value.copy_string("hi", 1).chars == ['h', '\x00']
    assert value.copy_string("hi", 0).chars == ['\x00']

    with pytest.raises(IndexError):
        assert value.copy_string("hi", 3).chars == ['h', 'i','\x00']


def test_allocate_string():
    # type: () -> None
    """Checks allocate_string stores arguments in a ObjectString as
    intended."""
    item = value.allocate_string(['\x00'], 0,  value.FNV_32_INIT)

    assert item.obj.is_string()
    assert item.length == 0
    assert item.chars == ['\x00']
    assert item.hash_value == value.FNV_32_INIT


def test_hash_string():
    #
    """
    """
    assert value.hash_string(['f', 'n', 'v', '\x00'], 3) == 0xb2f5cb99


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
