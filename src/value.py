from enum import Enum
from typing import Any, List, Optional, Union

import memory

FNV_32_INIT = 2166136261
FNV_32_PRIME = 16777619
FNV_32_SIZE = 2**32


class ObjectType(Enum):
    OBJ_STRING = "OBJ_STRING"


class Object():
    def __init__(self, object_type, obj):
        # type: (ObjectType, Any)
        """Initialize Object."""
        self.object_type = object_type
        self.obj = obj

    def is_object_type(self, object_type):
        # type: (ObjectType) -> bool
        """Checks if Object type matches argument."""
        return self.object_type == object_type

    def is_string(self):
        # type: () -> bool
        """Checks if Object version is string."""
        return self.is_object_type(ObjectType.OBJ_STRING)


def allocate_object(size, object_type):
    #
    """
    """
    return Object(
        object_type=object_type,
        obj=memory.reallocate(None, 0, size),
    )


class ObjectString():
    def __init__(self, obj):
        # type: (Object) -> None
        """Initialize string version of Object."""
        self.obj = obj
        self.length = 0
        self.chars = obj.obj
        self.hash_value = None
        # Reset array created by obj.obj
        self.obj.obj = None


def take_string(chars, length):
    # type: (List[str], int) -> ObjectString
    """Applies for concatenation. Takes ownership of characters passed as
    argument, since no need for copy of characters on the heap.
    """
    hash_value = hash_string(chars, length)
    # interned = table.table_find_string(strings, chars, length, hash_value)

    # if not interned is None:
    #     chars = memory.free_array(chars, length + 1)
    #     return interned

    return allocate_string(chars, length, hash_value)


def copy_string(chars, length):
    # type: (str, int) -> ObjectString
    """Copies existing string and calls allocate_string. Assumes ownership of
    characters passed as argument cannot be taken away, so creates a copy. This
    is desired as characters may be in the middle of the source string"""
    heap_chars = memory.allocate(length + 1)

    heap_chars[:length] = chars[:length]
    heap_chars[length] = "\0"

    hash_value = hash_string(heap_chars, length)

    # interned = table.table_find_string(strings, chars, length, hash_value)

    # if not interned is None:
    #     return interned

    return allocate_string(heap_chars, length, hash_value)


def allocate_string(chars, length, hash_value):
    # type: (List[str], int, Any) -> ObjectString
    """Creates ObjectString from Object and copies chars. Note length represents
    length of characters excluding end of string token."""
    obj = allocate_object(length + 1, ObjectType.OBJ_STRING)

    string = ObjectString(obj)
    string.chars[:len(chars)] = chars
    string.length = length
    string.hash_value = hash_value

    # table.table_set(strings, string, nil_val())

    return string


def hash_string(chars, length):
    # type: (List[str], int) -> int
    """Applies FNV-1a to character string.
    http://www.isthe.com/chongo/tech/comp/fnv/#FNV-1
    """
    hash_int = FNV_32_INIT
    key = bytes("".join(chars), "UTF-8")

    for i in range(length):
        hash_int = hash_int ^ key[i]
        hash_int = (hash_int * FNV_32_PRIME) % FNV_32_SIZE

    return hash_int


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
        # type: () -> Object
        """
        """
        assert self.is_obj()
        return self.value_as

    def as_string(self):
        # type: () -> ObjectString
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
