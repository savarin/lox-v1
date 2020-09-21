from enum import Enum

import chunk
import compiler

STACK_MAX = 16


class InterpretResult(Enum):
    INTERPRET_OK = "INTERPRET_OK"
    INTERPRET_COMPILE_ERROR = "INTERPRET_COMPILE_ERROR"
    INTERPRET_RUNTIME_ERROR = "INTERPRET_RUNTIME_ERROR"


class VM():
    def __init__(self):
        #
        """
        """
        self.bytecode = None
        self.ip = 0
        self.stack = [None] * STACK_MAX
        self.stack_top = 0

    def free_vm(self):
        #
        """
        """
        pass

    def push(self, value):
        #
        """
        """
        self.stack[self.stack_top] = value
        self.stack_top += 1

    def pop(self):
        #
        """
        """
        self.stack_top -= 1
        return self.stack[self.stack_top]

    def interpret(self, source):
        # type: (str) -> InterpretResult
        """
        """
        bytecode = chunk.Chunk()

        if not compiler.compile(source, bytecode):
            bytecode.free_chunk()
            return InterpretResult.INTERPRET_COMPILE_ERROR

        self.bytecode = bytecode
        self.ip = 0  # book refers to pointer of bytecode.code

        result = self.run()

        self.bytecode.free_chunk()
        return result

    def run(self):
        #
        """
        """
        def read_byte():
            self.ip += 1
            return self.bytecode.code[self.ip - 1]

        def read_constant():
            return self.bytecode.constants.values[read_byte()]

        def binary_op(op):
            b = self.pop()
            a = self.pop()

            self.push(eval("a {} b".format(op)))

        while True:
            instruction = read_byte()

            if instruction == chunk.OpCode.OP_CONSTANT:
                constant = read_constant()
                self.push(constant)

            elif instruction == chunk.OpCode.OP_ADD:
                binary_op("+")

            elif instruction == chunk.OpCode.OP_SUBTRACT:
                binary_op("-")

            elif instruction == chunk.OpCode.OP_MULTIPLY:
                binary_op("*")

            elif instruction == chunk.OpCode.OP_DIVIDE:
                binary_op("/")

            elif instruction == chunk.OpCode.OP_NEGATE:
                self.push(-self.pop())

            elif instruction == chunk.OpCode.OP_RETURN:
                print("{}".format(self.pop()))
                return InterpretResult.INTERPRET_OK
