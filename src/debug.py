import chunk


def disassemble_chunk(bytecode, name):
    #
    """
    """
    print("== {} ==".format(name))

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


def constant_instruction(name, bytecode, offset):
    #
    """
    """
    constant = bytecode.code[offset + 1]
    print("{:16s} {:4d} '{}'".format(name, constant,
                                     bytecode.constants.values[constant]))
    return offset + 2
