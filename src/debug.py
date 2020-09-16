import chunk


def disassemble_chunk(bytecode, name):
    #
    """
    """
    print("== {} ==".format(name))

    for offset in range(bytecode.count):
        offset = disassemble_instruction(bytecode, offset)


def disassemble_instruction(bytecode, offset):
    #
    """
    """
    instruction = bytecode.code[offset]

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
