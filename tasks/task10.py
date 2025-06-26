from utils import Graph
from typing import List, Tuple
import math

def floyd_warshall(n: int, adj: List[List[int]]) -> Tuple[List[List[float]], List[List[int]]]:
    dist = [[math.inf] * n for _ in range(n)]
    nxt = [[-1] * n for _ in range(n)]
    for u in range(n):
        for v in range(n):
            if adj[u][v] != 0:
                dist[u][v] = adj[u][v]
                nxt[u][v] = v
        dist[u][u] = 0
        nxt[u][u] = u
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
                    nxt[i][j] = nxt[i][k]
    return dist, nxt

def restore_path(u: int, v: int, nxt: List[List[int]]) -> List[int]:
    if nxt[u][v] == -1:
        return []
    path = [u]
    while u != v:
        u = nxt[u][v]
        path.append(u)
    return path

def get_components(n: int, adj: List[List[int]]) -> List[List[int]]:
    visited = [False] * n
    components = []
    def dfs(u, comp):
        visited[u] = True
        comp.append(u)
        for v in range(n):
            if adj[u][v] != 0 and not visited[v]:
                dfs(v, comp)
            if adj[v][u] != 0 and not visited[v]:
                dfs(v, comp)
    for i in range(n):
        if not visited[i]:
            comp = []
            dfs(i, comp)
            components.append(sorted(comp))
    return components

def solve_task(graph: Graph) -> str:
    n = graph.size()
    adj = graph.adjacency_matrix()
    dist, nxt = floyd_warshall(n, adj)
    components = get_components(n, adj)
    result = ""
    for idx, comp in enumerate(components):
        if idx > 0:
            result += "\n\n\n"
        if len(components) > 1:
            result += "Vertices list in component:\n"
            result += str([x+1 for x in comp]) + "\n"
        # Степени вершин для этой компоненты
        degrees = [sum(1 for w in adj[i] if w != 0) for i in comp]
        result += "Vertices degrees:\n"
        result += str(degrees) + "\n"
        # Эксцентриситеты для этой компоненты
        eccentricity = []
        for i in comp:
            mx = max(dist[i][j] for j in comp if dist[i][j] < math.inf)
            eccentricity.append(float(mx))
        result += "Eccentricity:\n"
        result += str(eccentricity) + "\n"
        # Радиус и центральные вершины для этой компоненты
        R = float(min(eccentricity))
        result += f"R = {R}\n"
        central = [comp[i]+1 for i, e in enumerate(eccentricity) if e == R]
        result += f"Central vertices:\n{central}\n"
        # Диаметр и периферийные вершины для этой компоненты
        D = float(max(eccentricity))
        result += f"D = {D}\n"
        peripherial = [comp[i]+1 for i, e in enumerate(eccentricity) if e == D]
        result += f"Peripherial vertices:\n{peripherial}"
    return result.strip() 