class HashTable:
    def __init__(self, size=40):
        self.size = size
        self.table = [[] for _ in range(size)]

    def _hash(self, key):
        return key % self.size

    def insert(self, key, value):
        index = self._hash(key)

        # Update if key already exists
        for i, (k, v) in enumerate(self.table[index]):
            if k == key:
                self.table[index][i] = (key, value)
                return

        # Otherwise insert
        self.table[index].append((key, value))

    def lookup(self, key):
        index = self._hash(key)

        for k, v in self.table[index]:
            if k == key:
                return v

        return None

    def get_all(self):
        items = []
        for bucket in self.table:
            for k, v in bucket:
                items.append(v)
        return items