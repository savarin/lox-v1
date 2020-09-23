import pytest

from src import table
from src import value


def test_init_table():
    #
    """
    """
    hash_table = table.Table()

    assert hash_table.count == 0
    assert hash_table.capacity == 0
    assert hash_table.entries is None

    k1 = value.copy_string("key", 3)
    v1 = value.copy_string("value", 5)
    hash_table.table_set(k1, v1)

    assert hash_table.count == 1
    assert hash_table.capacity == 8
    assert hash_table.entries is not None
    
    k2 = value.copy_string("key", 3)
    result = hash_table.table_get(k2)

    assert result.obj.is_string()
    assert result.length == 5
    assert result.chars == ['v', 'a', 'l', 'u', 'e', '\x00']

    hash_table.table_delete(k2)

    assert hash_table.table_get(k2) is None
    assert hash_table.count == 1
    assert hash_table.capacity == 8

    hash_table.free_table()

    assert hash_table.count == 0
    assert hash_table.capacity == 0
    assert hash_table.entries is None
