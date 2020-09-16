import chunk
import debug

if __name__ == "__main__":
    bytecode = chunk.Chunk()

    constant = bytecode.add_constant(1.2)
    bytecode.write_chunk(chunk.OpCode.OP_CONSTANT, 123)
    bytecode.write_chunk(constant, 123)

    bytecode.write_chunk(chunk.OpCode.OP_RETURN, 123)
    debug.disassemble_chunk(bytecode, "test chunk")
    bytecode.free_chunk()
