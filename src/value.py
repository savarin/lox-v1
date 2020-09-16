import memory


class ValueArray():
    def __init__(self):
        #
        """
        """
        self.values = []
        self.capacity = 0
        self.count = 0

    def write_value_array(self, value):
        #
        """
        """
        if self.capacity < self.count + 1:
            old_capacity = self.capacity
            self.capacity = memory.grow_capacity(old_capacity)
            self.values = memory.grow_array(
                self.values,
                old_capacity,
                self.capacity,
            )

        self.values[self.count] = value
        self.count += 1

    def free_value_array(self):
        #
        """
        """
        self.values = memory.free_array(self.values, self.capacity)
        self.capacity = 0
        self.count = 0
