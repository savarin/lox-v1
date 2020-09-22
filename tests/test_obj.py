import pytest

from src import obj


def test_allocate_object():
    # type: () -> None
    """Checks obj.allocate_objects creates a container as intended."""
    item = obj.allocate_object(size=8, object_type=obj.ObjectType.OBJ_STRING)

    assert item.object_type == obj.ObjectType.OBJ_STRING
    assert item.obj == [None] * 8


def test_copy_string():
    # type: () -> None
    """Checks obj.copy_string converts strings as intended."""
    item = obj.copy_string("", 0)

    assert obj.copy_string("hi", 2).chars == ['h', 'i','\x00']
    assert obj.copy_string("hi", 1).chars == ['h', '\x00']
    assert obj.copy_string("hi", 0).chars == ['\x00']

    with pytest.raises(IndexError):
        assert obj.copy_string("hi", 3).chars == ['h', 'i','\x00']


def test_allocate_string():
    # type: () -> None
    """Checks obj.allocate_string stores arguments in a ObjectString as
    intended."""
    item = obj.allocate_string(['\x00'], 0,  obj.FNV_32_INIT)

    assert item.obj.is_string()
    assert item.length == 0
    assert item.chars == ['\x00']
    assert item.hash_value == obj.FNV_32_INIT
