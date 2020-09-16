import chunk
import debug

if __name__ == "__main__":
    bytecode = chunk.Chunk()
    bytecode.write_chunk(chunk.OpCode.OP_RETURN)
    debug.disassemble_chunk(bytecode, "test chunk")
    bytecode.free_chunk()
