from enum import Enum

import memory


class OpCode(Enum):
    OP_RETURN = 1


class Chunk():
    def __init__(self):
        #
        """
        """
        self.count = 0
        self.capacity = 0
        self.code = []

    def free_chunk(self):
        #
        """
        """
        self.code = memory.free_array(self.code, self.count)
        self.count = 0
        self.capacity = 0

    def write_chunk(self, byte):
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

        self.code[self.count] = byte
        self.count += 1
