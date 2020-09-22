from src import memory


def test_allocate():
    # type: () -> None
    """Checks allocate creates empty array as intended."""
    assert memory.allocate(0) is None
    assert memory.allocate(8) == [None] * 8
    assert memory.allocate(16) == [None] * 16


def test_grow_capacity():
    #
    """
    """
    assert memory.grow_capacity(0) == 8
    assert memory.grow_capacity(8) == 16
    assert memory.grow_capacity(16) == 32


def test_reallocate():
    #
    """
    """
    array = [1] + [None] * 15

    assert memory.grow_array(array, 16, 0) is None
    assert memory.grow_array(array, 16, 8) == [1] + [None] * 7
    assert memory.grow_array(array, 16, 32) == [1] + [None] * 31
