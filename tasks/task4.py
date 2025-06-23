from utils import Graph
import sys


def floyd_warshall(graph: Graph):
    n = graph.size()
    INF = float('inf')
    dist = [[INF] * n for _ in range(n)]
    for i in range(n):
        dist[i][i] = 0
    matrix = graph.adjacency_matrix()
    for i in range(n):
        for j in range(n):
            if matrix[i][j] > 0:
                dist[i][j] = 1  # Для неориентированного/не взвешенного графа
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
    return dist


def solve_task(graph: Graph, **kwargs) -> str:
    if graph.is_directed():
        return "This task is only for undirected graphs."
    if graph.size() > 1000:
        sys.setrecursionlimit(max(sys.getrecursionlimit(), graph.size() * 2))
    n = graph.size()
    degrees = [len(graph.adjacency_list(i + 1)) for i in range(n)]
    dist = floyd_warshall(graph)
    eccentricity = []
    for i in range(n):
        row = dist[i]
        if any(d == float('inf') and j != i for j, d in enumerate(row)):
            eccentricity.append('+Infinity')
        else:
            max_dist = max([d for d in row if d < float('inf')])
            eccentricity.append(max_dist)
    if any(e == '+Infinity' for e in eccentricity):
        R = D = '+Infinity'
        central = peripherial = list(range(1, n + 1))
    else:
        D = max(eccentricity)
        R = min(eccentricity)
        central = [i + 1 for i, e in enumerate(eccentricity) if e == R]
        peripherial = [i + 1 for i, e in enumerate(eccentricity) if e == D]
    result = []
    result.append("Vertices degrees:")
    result.append(str(degrees))
    result.append("Eccentricity:")
    result.append("[" + ", ".join(str(e) for e in eccentricity) + "]")
    result.append(f"R = {R}")
    result.append("Central vertices:")
    result.append(str(central))
    result.append(f"D = {D}")
    result.append("Peripherial vertices:")
    result.append(str(peripherial))
    return "\n".join(result) 