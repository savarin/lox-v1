import chunk
import value


def disassemble_chunk(bytecode, name):
    #
    """
    """
    print("\n== {} ==".format(name))

    offset = 0

    while offset < bytecode.count:
        offset = disassemble_instruction(bytecode, offset)


def disassemble_instruction(bytecode, offset):
    #
    """
    """
    print("{:04d}".format(offset), end=" ")

    if offset > 0 and bytecode.lines[offset] == bytecode.lines[offset - 1]:
        print("   |", end=" ")
    else:
        print("{:4d}".format(bytecode.lines[offset]), end=" ")

    instruction = bytecode.code[offset]

    if instruction == chunk.OpCode.OP_CONSTANT:
        return constant_instruction("OP_CONSTANT", bytecode, offset)
    elif instruction == chunk.OpCode.OP_NIL:
        return simple_instruction("OP_NIL", offset)
    elif instruction == chunk.OpCode.OP_TRUE:
        return simple_instruction("OP_TRUE", offset)
    elif instruction == chunk.OpCode.OP_FALSE:
        return simple_instruction("OP_FALSE", offset)
    elif instruction == chunk.OpCode.OP_POP:
        return simple_instruction("OP_POP", offset)
    elif instruction == chunk.OpCode.OP_GET_LOCAL:
        return byte_instruction("OP_GET_LOCAL", bytecode, offset)
    elif instruction == chunk.OpCode.OP_SET_LOCAL:
        return byte_instruction("OP_SET_LOCAL", bytecode, offset)
    elif instruction == chunk.OpCode.OP_GET_GLOBAL:
        return constant_instruction("OP_GET_GLOBAL", bytecode, offset)
    elif instruction == chunk.OpCode.OP_DEFINE_GLOBAL:
        return constant_instruction("OP_DEFINE_GLOBAL", bytecode, offset)
    elif instruction == chunk.OpCode.OP_SET_GLOBAL:
        return constant_instruction("OP_SET_GLOBAL", bytecode, offset)
    elif instruction == chunk.OpCode.OP_EQUAL:
        return simple_instruction("OP_EQUAL", offset)
    elif instruction == chunk.OpCode.OP_GREATER:
        return simple_instruction("OP_GREATER", offset)
    elif instruction == chunk.OpCode.OP_LESS:
        return simple_instruction("OP_LESS", offset)
    elif instruction == chunk.OpCode.OP_ADD:
        return simple_instruction("OP_ADD", offset)
    elif instruction == chunk.OpCode.OP_SUBTRACT:
        return simple_instruction("OP_SUBTRACT", offset)
    elif instruction == chunk.OpCode.OP_MULTIPLY:
        return simple_instruction("OP_MULTIPLY", offset)
    elif instruction == chunk.OpCode.OP_DIVIDE:
        return simple_instruction("OP_DIVIDE", offset)
    elif instruction == chunk.OpCode.OP_NEGATE:
        return simple_instruction("OP_NEGATE", offset)
    elif instruction == chunk.OpCode.OP_PRINT:
        return simple_instruction("OP_PRINT", offset)
    elif instruction == chunk.OpCode.OP_NOT:
        return simple_instruction("OP_NOT", offset)
    elif instruction == chunk.OpCode.OP_JUMP:
        return jump_instruction("OP_JUMP", 1, bytecode, offset)
    elif instruction == chunk.OpCode.OP_JUMP_IF_FALSE:
        return jump_instruction("OP_JUMP_IF_FALSE", 1, bytecode, offset)
    elif instruction == chunk.OpCode.OP_LOOP:
        return jump_instruction("OP_LOOP", -1, bytecode, offset)
    elif instruction == chunk.OpCode.OP_RETURN:
        return simple_instruction("OP_RETURN", offset)

    print("Unknown opcode {}".format(instruction))
    return offset + 1


def simple_instruction(name, offset):
    #
    """
    """
    print("{}".format(name))
    return offset + 1


def byte_instruction(name, bytecode, offset):
    #
    """
    """
    slot = bytecode.code[offset + 1]

    print("{:16s} {:4d}".format(name, slot))
    return offset + 2


def jump_instruction(name, sign, bytecode, offset):
    #
    """
    """
    jump = bytecode.code[offset + 1] << 8
    jump = jump | bytecode.code[offset + 2]

    print("{:16s} {:4d} -> {}".format(name, offset, offset + 3 + sign * jump))
    return offset + 3


def constant_instruction(name, bytecode, offset):
    #
    """
    """
    constant = bytecode.code[offset + 1]
    val = convert_value(bytecode.constants.values[constant])

    print("{:16s} {:4d} '{}'".format(name, constant, val))
    return offset + 2


def convert_value(val):
    #
    """
    """
    if isinstance(val, value.Value) and val.is_string():
        return "".join(val.as_cstring()[:-1])

    return val
