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
    instruction = bytecode.code[offset]

    if instruction == chunk.OpCode.OP_CONSTANT:
        return constant_instruction("OP_CONSTANT", bytecode, offset)
    if instruction == chunk.OpCode.OP_RETURN:
        return simple_instruction("OP_RETURN", offset)

    print("{:04d} Unknown opcode {}".format(offset, instruction))
    return offset + 1


def simple_instruction(name, offset):
    #
    """
    """
    print("{:04d} {}".format(offset, name))
    return offset + 1


def constant_instruction(name, bytecode, offset):
    #
    """
    """
    constant = bytecode.code[offset + 1]
    print("{:04d} {:16s} {:04d} {}".format(
        offset, name, constant, bytecode.constants.values[constant]))
    return offset + 2
