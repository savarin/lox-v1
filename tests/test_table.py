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

    key = value.copy_string("key", 3)
    val = value.copy_string("value", 5)
    hash_table.table_set(key, val)

    assert hash_table.count == 1
    assert hash_table.capacity == 8
    assert hash_table.entries is not None
    
    result = hash_table.table_get(key)

    assert result.obj.is_string()
    assert result.length == 5
    assert result.chars == ['v', 'a', 'l', 'u', 'e', '\x00']

    hash_table.table_delete(key)

    assert hash_table.table_get(key) is None
    assert hash_table.count == 1
    assert hash_table.capacity == 8

    hash_table.free_table()

    assert hash_table.count == 0
    assert hash_table.capacity == 0
    assert hash_table.entries is None
