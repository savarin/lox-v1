from enum import Enum
from typing import Union

import memory


class ObjectType(enum):
    OBJ_STRING = "OBJ_STRING"


class Object():
    def __init__(self, object_type):
        #
        """Not create obj.py to avoid circular dependencies."""
        self.object_type = object_type

    def is_object_type(self, object_type):
        #
        """
        """
        return self.object_type == object_type

    def is_string(self):
        #
        """
        """
        return self.is_object_type(ObjectType.OBJ_STRING)


class ObjectString():
    def __init__(self, chars):
        #
        """
        """
        self.obj = Object(ObjectType.OBJ_STRING)
        self.length = len(chars)
        self.chars = chars


class ValueType(Enum):
    VAL_BOOL = "VAL_BOOL"
    VAL_NIL = "VAL_NIL"
    VAL_NUMBER = "VAL_NUMBER"
    VAL_OBJ = "VAL_OBJ"


ValueAs = Union[bool, float, Object]


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
        #
        """
        """
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
        #
        """
        """
        assert self.is_obj()
        return self.value_as

    def as_string(self):
        #
        """
        """
        assert self.is_string()
        return self.value_as

    def as_cstring(self):
        #
        """
        """
        assert self.is_string()
        return self.value_as.chars

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
    #
    """
    """
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
