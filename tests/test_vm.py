from src import value
from src import vm


def test_concatenate():
    #
    """
    """
    a = value.obj_val(value.take_string("str", 3))
    b = value.obj_val(value.take_string("ing", 3))

    emulator = vm.VM()
    emulator.push(a)
    emulator.push(b)

    emulator.concatenate()

    result = emulator.pop()
    assert result.as_cstring() == ['s', 't', 'r', 'i', 'n', 'g', '\x00']
