import memory
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

    def find_entry(self, key):
        # type: (ObjectString) -> Optional[Entry]
        """Table method to retrieve Entry with matching key."""
        return find_entry(self.entries, self.capacity, key)

    def adjust_capacity(self, capacity):
        # type: (int) -> None
        """Change size of table to given capacity."""
        entries = memory.allocate(capacity)

        for i in range(capacity):
            entries[i] = Entry(key=None, val=value.nil_val())

        self.count = 0

        for j in range(self.capacity):
            entry = self.entries[j]

            if entry.key is None:
                continue

            dest = self.find_entry(entry.key)
            dest.key = entry.key
            dest.value = entry.value
            self.count += 1

        self.entries = memory.free_array(self.entries, self.capacity)
        self.entries = entries
        self.capacity = capacity

    def table_get(self, key):
        # type: (ObjectString) -> Optional[Any]
        """Retrieves value for matching key. Implementation differs from text
        since text sets the return value to a pointer.
        """
        if self.count == 0:
            return None

        entry = self.find_entry(key)

        if entry.key is None:
            return None

        return entry.value

    def table_set(self, key, val):
        # type: (ObjectString, Any) -> bool
        """Insert key-value pair as Entry in Table."""
        if self.count + 1 > self.capacity * TABLE_MAX_LOAD:
            capacity = memory.grow_capacity(self.capacity)
            self.adjust_capacity(capacity)

        entry = self.find_entry(key)
        is_new_key = entry.key == None

        if is_new_key and entry.value.is_nil():
            self.count += 1

        entry.key = key
        entry.value = val

        return is_new_key

    def table_delete(self, key):
        # type: (ObjectString) -> bool
        """Removes Entry with given key and place a tombstone in the entry."""
        if self.count == 0:
            return False

        # Find the entry
        entry = self.find_entry(key)

        if entry.key is None:
            return False

        # Place a tombstone in the entry
        entry.key = None
        entry.value = value.bool_val(True)

        return True

    def table_add_all(self, other):
        # type: (Table) -> None
        """Transfer all Entries in other Table to current table."""
        for i in range(other.capacity):
            entry = other.entries[i]

            if not entry.key is None:
                self.table_set(entry.key, entry.value)


def find_entry(entries, capacity, key):
    # type: (List[Entry], int, ObjectString) -> Optional[Entry]
    """Given ObjectString key, retrieve Entry in Table with the matching key.
    Separate function created (instead of a class method) since adjust_capacity
    requires retrieval of non-current Table."""
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
        elif entry.key.chars == key.chars:
            return entry

        index = (index + 1) % capacity
