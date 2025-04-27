import sys
from typing import List, Tuple
from utils.graph import Graph

def floyd_warshall(graph: Graph) -> Tuple[List[List[int]], List[int], List[int], int, List[int], int, List[int]]:
    n = graph.size()
    
    # Инициализация матрицы расстояний
    dist = [[sys.maxsize] * n for _ in range(n)]
    for i in range(n):
        dist[i][i] = 0
        for j in graph.adjacency_list(i + 1):
            dist[i][j - 1] = 1  # Не взвешенный граф (вес = 1)
    
    # Алгоритм Флойда-Уоршелла
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
    
    # Вычисление степеней вершин
    degrees = [int(len(graph.adjacency_list(v)) / 2) for v in range(1, n + 1)]
    
    # Вычисление эксцентриситетов
    eccentricity = [max(row) for row in dist]
    
    # Диаметр и периферийные вершины
    diameter = max(eccentricity)
    peripheral = [v + 1 for v, e in enumerate(eccentricity) if e == diameter]
    
    # Радиус и центральные вершины
    radius = min(eccentricity)
    central = [v + 1 for v, e in enumerate(eccentricity) if e == radius]
    
    return dist, degrees, eccentricity, diameter, peripheral, radius, central