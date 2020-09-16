from enum import Enum

import memory
import value


class OpCode(Enum):
    OP_CONSTANT = 1
    OP_RETURN = 2


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

    def free_chunk(self):
        #
        """
        """
        self.code = memory.free_array(self.code, self.capacity)
        self.lines = memory.free_array(self.lines, self.capacity)
        self.constants.free_value_array()
        self.count = 0
        self.capacity = 0

    def add_constant(self, value):
        #
        """
        """
        self.constants.write_value_array(value)
        return self.constants.count - 1
