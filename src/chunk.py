import memory


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
            self.code = memory.grow_array(self.code, old_capacity, self.capacity)

        self.code[self.count] = byte
        self.count += 1


if __name__ == "__main__":
    chunk = Chunk()

    print(chunk.code)

    chunk.write_chunk('0')

    print(chunk.code)

    for i in range(1, 16):
        chunk.write_chunk(str(i))
        print(chunk.code)

    print(memory.reallocate(chunk.code, chunk.count, 12))

    chunk.free_chunk()

    print(chunk.code)