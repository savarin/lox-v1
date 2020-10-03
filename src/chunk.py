from enum import Enum

import memory
import value


class OpCode(Enum):
    OP_CONSTANT = "OP_CONSTANT"
    OP_NIL = "OP_NIL"
    OP_TRUE = "OP_TRUE"
    OP_FALSE = "OP_FALSE"
    OP_POP = "OP_POP"
    OP_GET_LOCAL = "OP_GET_LOCAL"
    OP_SET_LOCAL = "OP_SET_LOCAL"
    OP_GET_GLOBAL = "OP_GET_GLOBAL"
    OP_DEFINE_GLOBAL = "OP_DEFINE_GLOBAL"
    OP_SET_GLOBAL = "OP_SET_GLOBAL"
    OP_EQUAL = "OP_EQUAL"
    OP_GREATER = "OP_GREATER"
    OP_LESS = "OP_LESS"
    OP_ADD = "OP_ADD"
    OP_SUBTRACT = "OP_SUBTRACT"
    OP_MULTIPLY = "OP_MULTIPLY"
    OP_DIVIDE = "OP_DIVIDE"
    OP_NOT = "OP_NOT"
    OP_NEGATE = "OP_NEGATE"
    OP_PRINT = "OP_PRINT"
    OP_JUMP = "OP_JUMP"
    OP_JUMP_IF_FALSE = "OP_JUMP_IF_FALSE"
    OP_LOOP = "OP_LOOP"
    OP_CALL = "OP_CALL"
    OP_RETURN = "OP_RETURN"


class Chunk():
    def __init__(self):
        #
        """
        """
        self.count = 0
        self.capacity = 0
        self.code = None
        self.lines = None
        self.constants = value.ValueArray()

    def free_chunk(self):
        #
        """
        """
        self.code = memory.free_array(self.code, self.capacity)
        self.lines = memory.free_array(self.lines, self.capacity)
        self.constants.free_value_array()
        self.count = 0
        self.capacity = 0

    def write_chunk(self, byte, line):
        #
        """
        """
        if self.capacity < self.count + 1:
            old_capacity = self.capacity
            self.capacity = memory.grow_capacity(old_capacity)
            self.code = memory.grow_array(
                self.code,
                old_capacity,
                self.capacity,
            )
            self.lines = memory.grow_array(
                self.lines,
                old_capacity,
                self.capacity,
            )

        self.code[self.count] = byte
        self.lines[self.count] = line
        self.count += 1

    def add_constant(self, value):
        #
        """
        """
        self.constants.write_value_array(value)
        return self.constants.count - 1
