def grow_capacity(capacity):
    #
    """
    """
    if capacity < 8:
        return 8

    return capacity * 2


def grow_array(array, old_count, new_count):
    #
    """
    """
    return reallocate(array, old_count, new_count)


def free_array(array, old_count):
    #
    """
    """
    return reallocate(array, old_count, 0)


def reallocate(array, old_size, new_size):
    #
    """
    """
    if new_size == 0:
        return None
    elif old_size > new_size:
        return array[:new_size]

    # Create empty list if array is None
    array = array or []
    return array + (new_size - old_size) * [None]
