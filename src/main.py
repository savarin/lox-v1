import chunk
import debug
import vm

if __name__ == "__main__":
    emulator = vm.VM()
    bytecode = chunk.Chunk()

    constant = bytecode.add_constant(1.2)
    bytecode.write_chunk(chunk.OpCode.OP_CONSTANT, 123)
    bytecode.write_chunk(constant, 123)

    constant = bytecode.add_constant(3.4)
    bytecode.write_chunk(chunk.OpCode.OP_CONSTANT, 123)
    bytecode.write_chunk(constant, 123)

    bytecode.write_chunk(chunk.OpCode.OP_ADD, 123)

    constant = bytecode.add_constant(5.6)
    bytecode.write_chunk(chunk.OpCode.OP_CONSTANT, 123)
    bytecode.write_chunk(constant, 123)

    bytecode.write_chunk(chunk.OpCode.OP_DIVIDE, 123)
    bytecode.write_chunk(chunk.OpCode.OP_NEGATE, 123)

    bytecode.write_chunk(chunk.OpCode.OP_RETURN, 123)
    debug.disassemble_chunk(bytecode, "test chunk")
    emulator.interpret(bytecode)
    emulator.free_vm()
    bytecode.free_chunk()
