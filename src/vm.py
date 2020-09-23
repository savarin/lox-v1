from enum import Enum

import chunk
import compiler
import memory
import table
import value

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
        self.globals = table.Table()

    def free_vm(self):
        #
        """
        """
        self.globals.free_table()

    def reset_stack(self):
        #
        """
        """
        self.stack_top = 0

    def runtime_error(self, messages):
        # type: (Union[str, List[str]]) -> None
        """
        """
        print(messages if isinstance(messages, str) else " ".join(messages))
        print("[line {} in script]".format(self.bytecode.lines[self.ip]))

        self.reset_stack()

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

    def peek(self, distance):
        #
        """
        """
        return self.stack[self.stack_top - 1 - distance]

    def is_falsey(self, val):
        #
        """
        """
        return val.is_nil() or (val.is_bool() and not val.as_bool())

    def concatenate(self):
        #
        """
        """
        b = self.pop().as_string()
        a = self.pop().as_string()

        length = a.length + b.length
        chars = memory.allocate(length + 1)

        chars[:a.length] = a.chars[:a.length]
        chars[a.length:(a.length + b.length)] = b.chars[:b.length]
        chars[length] = "\0"

        result = value.take_string(chars, length)
        self.push(value.obj_val(result))

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

        def read_string():
            return read_constant().as_string()

        def binary_op(value_type, op):
            if not self.peek(0).is_number() or not self.peek(1).is_number():
                self.runtime_error("Operands must be numbers.")
                return InterpretResult.INTERPRET_RUNTIME_ERROR

            b = self.pop().as_number()
            a = self.pop().as_number()

            self.push(value_type(eval("a {} b".format(op))))

        while True:
            instruction = read_byte()

            if instruction == chunk.OpCode.OP_CONSTANT:
                constant = read_constant()
                self.push(constant)

            elif instruction == chunk.OpCode.OP_NIL:
                self.push(value.nil_val())

            elif instruction == chunk.OpCode.OP_TRUE:
                self.push(value.bool_val(True))

            elif instruction == chunk.OpCode.OP_FALSE:
                self.push(value.bool_val(False))

            elif instruction == chunk.OpCode.OP_POP:
                self.pop()

            elif instruction == chunk.OpCode.OP_GET_GLOBAL:
                name = read_string()
                val = self.globals.table_get(name)

                if not val:
                    self.runtime_error("Undefined variable '{}'.".format(name.chars))
                    return InterpretResult.INTERPRET_RUNTIME_ERROR

                self.push(val)

            elif instruction == chunk.OpCode.OP_DEFINE_GLOBAL:
                name = read_string()
                self.globals.table_set(name, self.peek(0))
                self.pop()

            elif instruction == chunk.OpCode.OP_EQUAL:
                b = self.pop()
                a = self.pop()
                self.push(value.bool_val(a.values_equal(b)))

            elif instruction == chunk.OpCode.OP_GREATER:
                binary_op(value.bool_val, ">")

            elif instruction == chunk.OpCode.OP_LESS:
                binary_op(value.bool_val, "<")

            elif instruction == chunk.OpCode.OP_ADD:
                if self.peek(0).is_string() and self.peek(1).is_string():
                    self.concatenate()
                elif self.peek(0).is_number() and self.peek(1).is_number():
                    b = self.pop().as_number()
                    a = self.pop().as_number()
                    self.push(value.number_val(a + b))
                else:
                    self.runtime_error(
                        "Operands must be two numbers or two strings.")
                    return InterpretResult.INTERPRET_RUNTIME_ERROR

            elif instruction == chunk.OpCode.OP_SUBTRACT:
                binary_op(value.number_val, "-")

            elif instruction == chunk.OpCode.OP_MULTIPLY:
                binary_op(value.number_val, "*")

            elif instruction == chunk.OpCode.OP_DIVIDE:
                binary_op(value.number_val, "/")

            elif instruction == chunk.OpCode.OP_NOT:
                self.push(value.bool_val(self.is_falsey(self.pop())))

            elif instruction == chunk.OpCode.OP_NEGATE:
                if not self.peek(0).is_number():
                    self.runtime_error("Operand must be a number")
                    return InterpretResult.INTERPRET_RUNTIME_ERROR

                self.push(value.number_val(-self.pop().as_number()))

            elif instruction == chunk.OpCode.OP_PRINT:
                self.pop().print_value()

            elif instruction == chunk.OpCode.OP_RETURN:
                return InterpretResult.INTERPRET_OK
