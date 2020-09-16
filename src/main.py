import chunk
import debug

if __name__ == "__main__":
    bytecode = chunk.Chunk()

    constant = bytecode.add_constant(1.2)
    bytecode.write_chunk(chunk.OpCode.OP_CONSTANT)
    bytecode.write_chunk(constant)

    bytecode.write_chunk(chunk.OpCode.OP_RETURN)
    debug.disassemble_chunk(bytecode, "test chunk")
    bytecode.free_chunk()
