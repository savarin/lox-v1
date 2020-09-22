from enum import Enum

import memory

FNV_32_INIT = 2166136261
FNV_32_PRIME = 16777619
FNV_32_SIZE = 2**32


class ObjectType(Enum):
    OBJ_STRING = "OBJ_STRING"


class Object():
    def __init__(self, object_type, obj):
        #
        """Not create obj.py to avoid circular dependencies."""
        self.object_type = object_type
        self.obj = obj

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
        #
        """
        """
        self.obj = obj
        self.length = 0
        self.chars = obj.obj
        self.hash_value = None
        # Reset array created by obj.obj
        self.obj.obj = None


def take_string(chars, length):
    #
    """Applies for concatenation. Takes ownership of characters passed as
    argument, since no need for copy of characters on the heap.
    """
    hash_value = hash_string(bytes("".join(chars), "UTF-8"), length)
    return allocate_string(chars, length, hash_value)


def copy_string(chars, length):
    # type: (str, int) -> ObjectString
    """Copies existing string and calls allocate_string. Assumes ownership of
    characters passed as argument cannot be taken away, so creates a copy. This
    is desired when characters are in the middle of the source string"""
    hash_value = hash_string(bytes("".join(chars), "UTF-8"), length)
    heap_chars = memory.allocate(length + 1)

    heap_chars[:length] = chars[:length]
    heap_chars[length] = "\0"

    return allocate_string(heap_chars, length, hash_value)


def allocate_string(chars, length, hash_value):
    # type: (str, int, Any) -> ObjectString
    """Creates ObjectString from Object and copies chars. Note length represents
    length of characters excluding end of string token."""
    obj = allocate_object(length + 1, ObjectType.OBJ_STRING)

    string = ObjectString(obj)
    string.chars[:len(chars)] = chars
    string.length = length
    string.hash_value = hash_value

    return string


def hash_string(key, length):
    #
    """
    """
    hash_int = FNV_32_INIT

    for i in range(length):
        hash_int = hash_int ^ key[i]
        hash_int = (hash_int * FNV_32_PRIME) % FNV_32_SIZE

    return hash_int
