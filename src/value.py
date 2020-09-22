from enum import Enum
from typing import Any, Union

import memory
import obj


class ValueType(Enum):
    VAL_BOOL = "VAL_BOOL"
    VAL_NIL = "VAL_NIL"
    VAL_NUMBER = "VAL_NUMBER"
    VAL_OBJ = "VAL_OBJ"


ValueAs = Union[bool, float, obj.Object]


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
        return self.value_type == ValueType.VAL_BOOL

    def is_nil(self):
        #
        """
        """
        return self.value_type == ValueType.VAL_NIL

    def is_number(self):
        #
        """
        """
        return self.value_type == ValueType.VAL_NUMBER

    def is_obj(self):
        # type: () -> bool
        """Check if Value is an Object."""
        return self.value_type == ValueType.VAL_OBJ

    def is_string(self):
        #
        """
        """
        return self.is_obj() and self.value_as.obj.is_string()

    def as_bool(self):
        # type: () -> bool
        """
        """
        assert self.is_bool()
        return self.value_as

    def as_number(self):
        # type: () -> float
        """
        """
        assert self.is_number()
        return self.value_as

    def as_obj(self):
        # type: () -> obj.Object
        """
        """
        assert self.is_obj()
        return self.value_as

    def as_string(self):
        # type: () -> obj.ObjectString
        """Unwraps Value to return ObjectString."""
        assert self.is_string()
        return self.value_as

    def as_cstring(self):
        # type: () -> str
        """Unwraps Value to return raw string of ObjectString."""
        assert self.is_string()
        return self.value_as.chars

    def print_object(self):
        #
        """
        """
        if self.is_string():
            print(self.as_cstring())

    def print_value(self):
        # type: () -> None
        """
        """
        if self.value_type == ValueType.VAL_BOOL:
            val = self.as_bool()
            print("true" if val else "false")
        elif self.value_type == ValueType.VAL_NIL:
            print("nil")
        elif self.value_type == ValueType.VAL_NUMBER:
            print("{}", self.as_number)
        elif self.value_type == ValueType.VAL_OBJ:
            self.print_object()

    def values_equal(self, other):
        #
        """
        """
        if self.value_type != other.value_type:
            return False

        if self.value_type == ValueType.VAL_BOOL:
            return self.as_bool() == other.as_bool()
        elif self.value_type == ValueType.VAL_NIL:
            return True
        elif self.value_type == ValueType.VAL_NUMBER:
            return self.as_number() == other.as_number()
        elif self.value_type == ValueType.VAL_OBJ:
            return self.as_obj() == other.as_obj()

        return False

    def obj_type(self):
        #
        """
        """
        assert self.is_obj()
        return self.value_as.obj.object_type


def bool_val(val):
    #
    """
    """
    return Value(ValueType.VAL_BOOL, val)


def nil_val():
    #
    """
    """
    return Value(ValueType.VAL_NIL, 0)


def number_val(val):
    #
    """
    """
    return Value(ValueType.VAL_NUMBER, val)


def obj_val(val):
    # type: (Any) -> Value
    """Wraps Object in a Value."""
    return Value(ValueType.VAL_OBJ, val)


class ValueArray():
    def __init__(self):
        #
        """
        """
        self.count = 0
        self.capacity = 0
        self.values = None

    def write_value_array(self, val):
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

        self.values[self.count] = val
        self.count += 1

    def free_value_array(self):
        #
        """
        """
        self.values = memory.free_array(self.values, self.capacity)
        self.count = 0
        self.capacity = 0
