
# Hashtable Class
class HashTable:
    # Constructor initializes the hash table.
    # Default size is 40 to create 40 buckets
    def __init__(self, size=40):
        self.size = size
        # Create a list of 40 empty lists
        # Each list represents a bucket to handle errors such as multiple keys mapped to same index
        self.table = [[] for _ in range(size)]
    # Hash function
    # Converts a key (package ID) into an index within the table
    # Use modulo to keep index within valid range
    def _hash(self, key):
        return key % self.size
    #Insert Function
    # Adds a key value pair (package ID and Package object) to the table
    def insert(self, key, value):
        index = self._hash(key)

        # Check if the key already exists in the bucket
        # If it exists, update the value instead of adding a duplicate.
        for i, (k, v) in enumerate(self.table[index]):
            if k == key:
                self.table[index][i] = (key, value)
                return

        # If the key does not exist, append the new key value pair.
        self.table[index].append((key, value))

    # Look up Function
    # Retrieves the value (Package object) associated with the given key
    def lookup(self, key):
        index = self._hash(key)
        # Search through the bucket for the matching key
        for k, v in self.table[index]:
            if k == key:
                return v
        # Return none if the key isn't found
        return None

    # Returns all stored values in the hash table
    # Useful for iterating through all packages
    def get_all(self):
        items = []

        # Loop through all buckets and collect all values
        for bucket in self.table:
            for k, v in bucket:
                items.append(v)
        return items