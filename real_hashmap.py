from enum import Enum

MIN_SIZE = 128


# implementing the dbj2 hash function
def dbj2(string):
    hash_num = 5381
    for char in string:
        hash_num = ((hash_num << 5) + hash_num) + ord(char)
    return hash_num


class State(Enum):
    EMPTY = 0
    VALID = 1
    DELETED = 2


class HashMap:
    def __init__(self):
        self.size = MIN_SIZE
        self.occ_buckets = 0
        self.del_buckets = 0
        self.states = [0] * self.size
        self.map = [None] * self.size

    def load(self):
        return self.occ_buckets / self.size

    def resize(self):
        load_factor = (self.occ_buckets + self.del_buckets) / self.size

        if load_factor < 0.25:
            new_size = self.size // 2
        elif load_factor > 0.75:
            new_size = self.size * 2
        else:
            return

        if new_size < MIN_SIZE:
            return

        self.size = new_size
        self.del_buckets = 0
        new_states = [0] * self.size
        new_map = [None] * self.size

        for idx, item in enumerate(self.map):
            if (
                self.states[idx] == State.EMPTY.value
                or self.states[idx] == State.DELETED.value
            ):
                continue
            key, val = self.map[idx]

            hash_num = dbj2(key)
            bucket = hash_num % self.size
            offset = 0
            # Until you find empty or deleted bucket or same key is found
            while new_states[bucket] == State.VALID.value and new_map[bucket][0] != key:
                offset += 1
                bucket = (hash_num + offset) % self.size

            new_map[bucket] = (key, val)
            new_states[bucket] = 1

        self.map = new_map
        self.states = new_states

    def write(self, key, val):
        if not isinstance(key, str):
            raise KeyError("keys must be of string type")

        self.resize()

        hash_num = dbj2(key)
        bucket = hash_num % self.size
        first_empty = None
        offset = 0
        # Until you find empty or deleted bucket or same key is found
        while self.states[bucket] != State.EMPTY.value:
            if self.states[bucket] == State.DELETED.value:
                first_empty = bucket
            elif (
                self.states[bucket] == State.VALID.value and self.map[bucket][0] == key
            ):
                break

            offset += 1
            bucket = (hash_num + offset) % self.size

        if self.states[bucket] == State.VALID.value:
            self.map[bucket] = (key, val)
        else:
            if first_empty is not None:
                self.map[first_empty] = (key, val)
                self.states[first_empty] = 1
                self.del_buckets -= 1
            else:
                self.map[bucket] = (key, val)
                self.states[bucket] = 1
            self.occ_buckets += 1

    def read(self, key):
        if not isinstance(key, str):
            raise KeyError("keys must be of string type")

        hash_num = dbj2(key)
        bucket = hash_num % self.size
        offset = 0
        # Until you find empty or deleted bucket or same key is found
        while self.states[bucket] == State.DELETED.value or (
            self.states[bucket] == State.VALID.value and self.map[bucket][0] != key
        ):
            offset += 1
            bucket = (hash_num + offset) % self.size

        if self.states[bucket] == State.EMPTY.value:
            raise KeyError(f"Error: key({key}) doesnt exist")

        key_ret, val = self.map[bucket]
        return val

    def delete(self, key):
        if not isinstance(key, str):
            raise KeyError("keys must be of string type")

        hash_num = dbj2(key)
        bucket = hash_num % self.size
        offset = 0
        # Until you find empty or deleted bucket or same key is found
        while self.states[bucket] == State.DELETED.value or (
            self.states[bucket] == State.VALID.value and self.map[bucket][0] != key
        ):
            offset += 1
            bucket = (hash_num + offset) % self.size

        if self.states[bucket] == State.EMPTY.value:
            return

        self.states[bucket] = 2
        self.map[bucket] = None
        self.occ_buckets -= 1
        self.del_buckets += 1

        self.resize()

    def __setitem__(self, key, val):
        self.write(key, val)

    def __getitem__(self, key):
        return self.read(key)

    def __delitem__(self, key):
        self.delete(key)

    def __repr__(self):
        res = []

        for idx in range(0, self.size):
            if not self.map[idx]:
                continue
            key, val = self.map[idx]
            res.append(f"{key}:{val}")

        return "{ " + ",".join(res) + " }"


hm = HashMap()
hm["e"] = 1
hm["da"] = 2
print(hm)
del hm["e"]
hm["da"] = 3
print(hm)
del hm["da"]
print(hm["da"])
