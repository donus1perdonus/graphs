from utils import Graph
import sys


def find_bridges_and_articulation_points(graph: Graph):
    n = graph.size()
    timer = [0]
    tin = [0] * (n + 1)
    low = [0] * (n + 1)
    visited = [False] * (n + 1)
    bridges = []
    articulation_points: set[int] = set()

    def dfs(v, parent):
        visited[v] = True
        timer[0] += 1
        tin[v] = low[v] = timer[0]
        children = 0
        for to in graph.adjacency_list(v):
            if to == parent:
                continue
            if visited[to]:
                low[v] = min(low[v], tin[to])
            else:
                dfs(to, v)
                low[v] = min(low[v], low[to])
                if low[to] > tin[v]:
                    bridges.append((v, to))
                if low[to] >= tin[v] and parent != -1:
                    articulation_points.add(v)
                children += 1
        if parent == -1 and children > 1:
            articulation_points.add(v)

    for v in range(1, n + 1):
        if not visited[v]:
            dfs(v, -1)

    # Упорядочим мосты и шарниры для вывода
    bridges = [tuple(sorted(edge)) for edge in bridges]
    bridges = sorted(set(bridges))
    articulation_points_sorted = sorted(articulation_points)
    return bridges, articulation_points_sorted


def solve_task(graph: Graph, **kwargs) -> str:
    if graph.is_directed():
        return "This task is only for undirected graphs."
    # Для больших графов увеличим лимит рекурсии
    if graph.size() > 1000:
        sys.setrecursionlimit(max(sys.getrecursionlimit(), graph.size() * 2))
    bridges, articulation_points_sorted = find_bridges_and_articulation_points(graph)
    result = []
    result.append("Bridges:")
    result.append(f" {bridges}")
    result.append("Cut vertices:")
    result.append(f" {articulation_points_sorted}")
    return "\n".join(result) 