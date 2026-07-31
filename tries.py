class Trie:
    def __init__(self, stop_symbol: str = "*") -> None:
        self.root: dict[str, bool | dict] = {}
        self.stop_symbol = "/" + stop_symbol

    def __repr__(self) -> str:
        return self.root.__repr__()

    def add(self, prefix: str) -> None:
        curr_lvl = self.root

        if not isinstance(prefix, str):
            raise ValueError(f"prefix arg needs be a string not {type(prefix)}")
        if not prefix:
            return None

        for char in prefix:
            assert isinstance(curr_lvl, dict)
            if char not in curr_lvl:
                curr_lvl[char] = {}
            curr_lvl = curr_lvl[char]

        assert isinstance(curr_lvl, dict)
        curr_lvl[self.stop_symbol] = True
        return None

    def exists(self, prefix: str) -> bool:

        if not isinstance(prefix, str):
            raise ValueError(f"prefix arg needs be a string not {type(prefix)}")
        if not prefix:
            return False

        curr_lvl = self.root
        for char in prefix:
            assert isinstance(curr_lvl, dict)
            if char not in curr_lvl:
                return False
            curr_lvl = curr_lvl[char]

        assert isinstance(curr_lvl, dict)
        if self.stop_symbol in curr_lvl:
            return True
        return False

    def words_with_prefix(self, prefix: str) -> list[str]:
        if not isinstance(prefix, str):
            raise ValueError(f"prefix arg needs be a string not {type(prefix)}")
        if not prefix:
            return []

        curr_lvl = self.root.get(prefix[0], None)
        if not curr_lvl:
            return []

        for char in prefix[1:]:
            assert isinstance(curr_lvl, dict)
            if char not in curr_lvl:
                return []
            curr_lvl = curr_lvl[char]

        assert isinstance(curr_lvl, dict)
        return self.search_lvl(curr_lvl, prefix, [])

    def search_lvl(
        self, curr_lvl: dict[str, bool | dict], curr_word: str, words: list[str]
    ) -> list[str]:

        for char in sorted(curr_lvl.keys()):
            if char == self.stop_symbol:
                words.append(curr_word)
                continue

            nxt_lvl = curr_lvl[char]
            assert isinstance(nxt_lvl, dict)
            self.search_lvl(nxt_lvl, curr_word + char, words)
        return words

    def find_matches(self, doc: str) -> set[str]:
        res: set[str] = set()

        for i in range(0, len(doc)):
            curr_lvl = self.root

            for j in range(i, len(doc)):
                char = doc[j]

                if char not in curr_lvl:
                    break
                curr_lvl = curr_lvl[char]
                assert isinstance(curr_lvl, dict)
                if self.stop_symbol in curr_lvl:
                    res.add(doc[i : j + 1])
        return res

    def longest_common_prefix(self) -> str:
        curr_lvl = self.root
        prefix = ""

        while True:
            assert isinstance(curr_lvl, dict)
            if len(curr_lvl) != 1:
                return prefix
            key = next(iter(curr_lvl))
            if key == self.stop_symbol:
                return prefix
            prefix += key
            curr_lvl = curr_lvl[key]
