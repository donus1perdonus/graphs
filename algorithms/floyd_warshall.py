import sys
from typing import List, Tuple
from utils.graph import Graph

def floyd_warshall(graph: Graph) -> Tuple[List[List[int]], List[int], List[int], int, List[int], int, List[int]]:
    n = graph.size()
    
    # Инициализация матрицы расстояний
    dist = [[sys.maxsize] * n for _ in range(n)]
    degrees = [0] * n  # Инициализация степеней вершин
    
    for i in range(n):
        dist[i][i] = 0
        neighbors = graph.adjacency_list(i + 1)
        degrees[i] = len(neighbors)  # Считаем степень вершины
        
        for j in neighbors:
            dist[i][j - 1] = 1  # Не взвешенный граф (вес = 1)
            if not graph.is_directed():
                # Для неориентированного графа добавляем обратное ребро
                dist[j - 1][i] = 1
    
    # Алгоритм Флойда-Уоршелла
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
    
    # Вычисление эксцентриситетов
    eccentricity = [max(row) for row in dist]
    
    # Диаметр и периферийные вершины
    diameter = max(eccentricity)
    peripheral = [v + 1 for v, e in enumerate(eccentricity) if e == diameter]
    
    # Радиус и центральные вершины
    radius = min(eccentricity)
    central = [v + 1 for v, e in enumerate(eccentricity) if e == radius]
    
    return dist, degrees, eccentricity, diameter, peripheral, radius, central