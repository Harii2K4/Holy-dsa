from typing import Any
import random


class HashMap:
    def __init__(self, size: int = 0) -> None:
        self.hash_map: list[tuple | None] = [None] * size

    def key_to_idx(self, key: str) -> int:
        # hash function
        return sum([ord(char) for char in key]) % len(self.hash_map)

    def get_current_load(self) -> float:
        size = len(self.hash_map)
        if size == 0:
            # Means it is full
            return 1
        filled_buckets = 0
        for bucket in self.hash_map:
            if not bucket:
                continue
            filled_buckets += 1
        return filled_buckets / size

    def resize(self) -> None:
        size = len(self.hash_map)
        if size == 0:
            self.hash_map = [None]
            return None

        load = self.get_current_load()
        if load <= 0.75:
            return None

        tmp = self.hash_map.copy()
        self.hash_map = [None] * (size * 10)
        for bucket in tmp:
            if not bucket:
                continue
            key, val = bucket
            idx = self.linear_probing(self.key_to_idx(key), key)
            self.hash_map[idx] = (key, val)
        return None

    def linear_probing(self, orig_idx: int, key: str) -> int:
        idx = orig_idx
        first_iter = True
        size = len(self.hash_map)

        while True:
            bucket = self.hash_map[idx]

            if idx == orig_idx and not first_iter:
                raise Exception("Hash map is full")

            if not bucket or bucket[0] == key:
                break
            idx = (idx + 1) % size
            first_iter = False
        return idx

    def insert(self, key: str, val: Any) -> None:
        if isinstance(key, list) or isinstance(key, dict):
            raise ValueError("Key must be immutable")

        if not isinstance(key, str):
            key = str(key)

        self.resize()
        idx = self.linear_probing(self.key_to_idx(key), key)
        self.hash_map[idx] = (key, val)
        return None

    def get(self, key: str) -> Any:
        if len(self.hash_map) == 0:
            raise Exception("Hash Map is empty")

        if isinstance(key, list) or isinstance(key, dict):
            raise ValueError("Key must be immutable")

        if not isinstance(key, str):
            key = str(key)

        idx = self.linear_probing(self.key_to_idx(key), key)
        bucket = self.hash_map[idx]
        if not bucket:
            return None
        return bucket[-1]

    def __len__(self) -> int:
        return len(self.hash_map)

    def __setitem__(self, key: str, val: Any) -> None:
        self.insert(key, val)

    def __getitem__(self, key: str) -> Any:
        return self.get(key)

    def __repr__(self) -> str:
        res = []
        for bucket in self.hash_map:
            if not bucket:
                continue
            key, val = bucket
            res.append(f"{key}:{val}")
        return "{" + ",".join(res) + "}"


def get_random_key():
    length = random.randint(1, 4)
    key = ""

    for _ in range(length):
        key += chr(random.randint(97, 122))
    return key


h = HashMap(1)
n = 10

for idx in range(n):
    key = get_random_key()
    val = random.randint(1, 1000)
    h[key] = val
print(h)
