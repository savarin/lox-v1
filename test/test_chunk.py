import pytest

from src import chunk


@pytest.fixture
def bytecode():
    #
    """
    """
    return chunk.Chunk()


def test_init(bytecode):
    #
    """
    """
    assert bytecode.count == 0
    assert bytecode.capacity == 0
    assert bytecode.code is None
    assert bytecode.lines is None
    assert bytecode.constants.count == 0
    assert bytecode.constants.capacity == 0
    assert bytecode.constants.values is None


def test_write_chunk_op_return(bytecode):
    #
    """
    """
    bytecode.write_chunk(chunk.OpCode.OP_RETURN, 123)
    assert bytecode.count == 1
    assert bytecode.capacity == 8
    assert bytecode.code[0] == chunk.OpCode.OP_RETURN
    assert bytecode.lines[0] == 123


def test_free_chunk_op_return(bytecode):
    #
    """
    """
    bytecode.write_chunk(chunk.OpCode.OP_RETURN, 123)
    bytecode.free_chunk()
    assert bytecode.count == 0
    assert bytecode.capacity == 0
    assert bytecode.code is None
    assert bytecode.lines is None


def test_write_chunk_op_constant(bytecode):
    #
    """
    """
    constant = bytecode.add_constant(1.2)
    assert constant == 0

    bytecode.write_chunk(chunk.OpCode.OP_CONSTANT, 123)
    bytecode.write_chunk(constant, 456)
    assert bytecode.count == 2
    assert bytecode.capacity == 8
    assert bytecode.code[0] == chunk.OpCode.OP_CONSTANT
    assert bytecode.code[1] == 0
    assert bytecode.lines[0] == 123
    assert bytecode.lines[1] == 456
