from enum import Enum
from typing import Union

import memory

class ValueType(Enum):
    VAL_BOOL = "VAL_BOOL"
    VAL_NIL = "VAL_NIL"
    VAL_NUMBER = "VAL_NUMBER"


ValueAs = Union[bool, float]


class Value():
    def __init__(self, value_type, value_as):
        # type: (ValueType, ValueAs) -> None
        """
        """
        self.value_type = value_type
        self.value_as = value_as

    def is_bool(self):
        #
        """
        """
        return value.value_type == ValueType.VAL_BOOL

    def is_nil(self):
        #
        """
        """
        return value.value_type == ValueType.VAL_NIL

    def is_number(self):
        #
        """
        """
        return value.value_type == ValueType.VAL_NUMBER

    def as_bool(self):
        # type: () -> bool
        """
        """
        assert self.is_bool()
        return value.value_as

    def as_number(self):
        # type: () -> float
        """
        """
        assert self.is_number()
        return value.value_as

    def print_value(self):
        # type: () -> None
        """
        """
        print("{}", self.as_number)


def bool_val(value):
    #
    """
    """
    return Value(ValueType.VAL_BOOL, value)


def nil_val(value):
    #
    """
    """
    return Value(ValueType.VAL_NIL, 0)


def number_val(value):
    #
    """
    """
    return Value(ValueType.VAL_NUMBER, value)


class ValueArray():
    def __init__(self):
        #
        """
        """
        self.count = 0
        self.capacity = 0
        self.values = None

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
        self.count = 0
        self.capacity = 0
