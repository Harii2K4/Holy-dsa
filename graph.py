from collections import deque


class Graph:
    def __init__(self) -> None:
        self.graph: dict[int, set[int]] = {}

    def add_vertice(self, v: int) -> None:
        if v not in self.graph:
            self.graph[v] = set()
        return None

    def add_edge(self, u: int, v: int) -> None:
        if v not in self.graph:
            self.graph[v] = set([u])
        else:
            self.graph[v].add(u)
        if u not in self.graph:
            self.graph[u] = set([v])
        else:
            self.graph[u].add(v)
        return None

    def unconnected_edges(self) -> list[int]:
        res = []
        for v in self.graph:
            if not self.graph[v]:
                res.append(v)
        return res

    def bfs(self, v: int) -> list[int]:
        res = [v]
        visited = set([v])
        q = deque([v])

        while q:
            n = len(q)
            for _ in range(n):
                curr_v = q.popleft()
                for next_v in self.graph[curr_v]:
                    if next_v not in visited:
                        q.append(next_v)
                        res.append(next_v)
                        visited.add(next_v)
        return res

    def dfs(self, v: int) -> list[int]:
        res = []

        def rec(visited: list[int], curr_v: int) -> None:
            if curr_v in visited:
                return
            visited.append(curr_v)
            for next_v in self.graph[curr_v]:
                rec(visited, next_v)

        rec(res, v)
        return res

    def __repr__(self) -> str:
        res = ""
        for v in self.graph:
            res += f"{v}->{self.graph[v]}\n"
        return res

    def __len__(self) -> int:
        return len(self.graph)


g = Graph()
g.add_vertice(0)
g.add_vertice(1)
g.add_vertice(2)
g.add_vertice(3)
g.add_vertice(4)
g.add_edge(0, 1)
g.add_edge(4, 1)
g.add_edge(0, 3)
g.add_edge(3, 2)
print(g.bfs(0))
print(g.dfs(0))
