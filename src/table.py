import value

TABLE_MAX_LOAD = 0.75


class Entry():
    def __init__(self, key, val):
        #
        """
        """
        self.key = key
        self.value = val


class Table():
    def __init__(self):
        #
        """
        """
        self.count = 0
        self.capacity = 0
        self.entries = None

    def free_table(self):
        #
        """
        """
        self.entries = memory.free_array(self.entries, self.capacity)
        self.count = 0
        self.capacity = 0


def find_entry(entries, capacity, key):
    #
    """
    """
    index = key.hash_value % capacity
    tombstone = None

    while True:
        entry = entries[index]

        if entry.key is None:
            # Empty entry
            if entry.value.is_nil():
                return tombstone or entry

            # Tombstone found
            if tombstone is None:
                tombstone = entry

        # Key found
        elif entry.key == key:
            return entry

        index = (index + 1) % capacity


def adjust_capacity(table, capacity):
    #
    """
    """
    entries = memory.allocate(capacity)

    for i in range(capacity):
        entries[i] = Entry(None, value.nil_val())

    table.count = 0

    for j in range(table.capacity):
        entry = table.entries[j]

        if entry.key is None:
            continue

        dest = find_entry(entries, capacity, entry.key)
        dest.key = entry.key
        dest.value = entry.value
        table.count += 1

    table.entries = memory.free_array(table.entries, table.capacity)
    table.entries = entries
    table.capacity = capacity


def table_set(table, key, val):
    #
    """
    """
    if table.count + 1 > table.capacity * TABLE_MAX_LOAD:
        capacity = memory.grow_capacity(table.capacity)
        adjust_capacity(table, capacity)

    entry = find_entry(table.entries, table.capacity, key)
    is_new_key = entry.key == None

    if is_new_key and entry.value.is_nil():
        table.count += 1

    entry.key = key
    entry.value = val

    return is_new_key


def table_delete(table, key):
    #
    """
    """
    if table.count == 0:
        return False

    # Find the entry
    entry = find_entry(table.entries, table.capacity, key)

    if entry.key is None:
        return False

    # Place a tombstone in the entry
    entry.key = None
    entry.value = value.bool_val(True)

    return True


def table_add_all(table_from, table_to):
    #
    """
    """
    for i in range(table_from.capacity):
        entry = table_from.entries[i]

        if not entry.key is None:
            table_set(table_to, entry.key, entry.value)
