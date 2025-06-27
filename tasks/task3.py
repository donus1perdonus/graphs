"""
Задание 3: Остовное дерево (Spanning Tree)

Реализует построение остовного дерева с помощью DFS или BFS.

Алгоритмы:
- DFS (поиск в глубину)
- BFS (поиск в ширину)

Временная сложность: O(V + E)
Пространственная сложность: O(V)

Пример вывода:
    Spanning tree edges:
    (1, 2)
    (2, 3)
    (3, 4)
"""
from utils import Graph
from collections import deque
import sys

def spanning_tree_edges(graph: Graph, method: str = 'dfs'):
    n = graph.size()
    visited = [False] * (n + 1)
    tree_edges = []

    def dfs(u):
        visited[u] = True
        for v in graph.adjacency_list(u):
            if not visited[v]:
                tree_edges.append(tuple(sorted((u, v))))
                dfs(v)

    def bfs(start):
        queue = deque([start])
        visited[start] = True
        while queue:
            u = queue.popleft()
            for v in graph.adjacency_list(u):
                if not visited[v]:
                    visited[v] = True
                    tree_edges.append(tuple(sorted((u, v))))
                    queue.append(v)

    for v in range(1, n + 1):
        if not visited[v]:
            if method == 'dfs':
                dfs(v)
            else:
                bfs(v)
    return tree_edges


def solve_task(graph: Graph, algorithm: str = 'dfs', **kwargs) -> str:
    if graph.is_directed():
        return "This task is only for undirected graphs."
    if graph.size() > 1000:
        sys.setrecursionlimit(max(sys.getrecursionlimit(), graph.size() * 2))
    edges = spanning_tree_edges(graph, method=algorithm)
    # Удаляем дубликаты и сортируем рёбра по формату эталона
    edges = sorted(set(edges))
    result = ["Spanning tree:"]
    for u, v in edges:
        result.append(f"{u}-{v}")
    return "\n".join(result) 