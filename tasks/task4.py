"""
Задание 4: Анализ графа - степени вершин, эксцентриситет, центр и периферия

Реализует анализ графа для определения:
- Степени всех вершин
- Эксцентриситета каждой вершины
- Радиуса графа (R)
- Диаметра графа (D)
- Центральных вершин
- Периферийных вершин

Алгоритмы:
- Флойда-Уоршелла для вычисления кратчайших путей между всеми парами вершин
- Вычисление эксцентриситета как максимального расстояния от вершины до других
- Определение центра и периферии на основе эксцентриситетов

Временная сложность: O(V^3) для алгоритма Флойда-Уоршелла
Пространственная сложность: O(V^2)
"""

from utils import Graph
import sys


def floyd_warshall(graph: Graph):
    """
    Реализует алгоритм Флойда-Уоршелла для нахождения кратчайших путей
    между всеми парами вершин.
    
    Алгоритм:
    1. Инициализация матрицы расстояний
    2. Для каждой промежуточной вершины k:
       - Для каждой пары вершин (i, j):
         - Если путь через k короче, обновляем расстояние
    
    Args:
        graph: граф для анализа
        
    Returns:
        матрица кратчайших расстояний между всеми парами вершин
    """
    n = graph.size()
    INF = float('inf')
    dist = [[INF] * n for _ in range(n)]
    
    # Инициализация: расстояние до себя равно 0
    for i in range(n):
        dist[i][i] = 0
    
    # Инициализация: прямые рёбра
    matrix = graph.adjacency_matrix()
    for i in range(n):
        for j in range(n):
            if matrix[i][j] > 0:
                dist[i][j] = 1  # Для неориентированного/не взвешенного графа
    
    # Основной цикл алгоритма Флойда-Уоршелла
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
    
    return dist


def solve_task(graph: Graph, **kwargs) -> str:
    """
    Решает задачу 4: анализ графа - степени, эксцентриситет, центр и периферия.
    
    Вычисляет:
    - Степени всех вершин
    - Эксцентриситет каждой вершины (максимальное расстояние до других вершин)
    - Радиус графа R (минимальный эксцентриситет)
    - Диаметр графа D (максимальный эксцентриситет)
    - Центральные вершины (с эксцентриситетом R)
    - Периферийные вершины (с эксцентриситетом D)
    
    Args:
        graph: неориентированный граф для анализа
        **kwargs: дополнительные параметры (не используются)
        
    Returns:
        строка с результатом анализа в требуемом формате
        
    Пример вывода:
        Vertices degrees:
        [2, 3, 2, 1, 2]
        Eccentricity:
        [2, 1, 2, 3, 2]
        R = 1
        Central vertices:
        [2]
        D = 3
        Peripherial vertices:
        [4]
        
    Raises:
        ValueError: если граф ориентированный
    """
    if graph.is_directed():
        return "This task is only for undirected graphs."
    
    # Увеличиваем лимит рекурсии для больших графов
    if graph.size() > 1000:
        sys.setrecursionlimit(max(sys.getrecursionlimit(), graph.size() * 2))
    
    n = graph.size()
    
    # Вычисляем степени всех вершин
    degrees = [len(graph.adjacency_list(i + 1)) for i in range(n)]
    
    # Находим кратчайшие пути между всеми парами вершин
    dist = floyd_warshall(graph)
    
    # Вычисляем эксцентриситет каждой вершины
    eccentricity = []
    for i in range(n):
        row = dist[i]
        # Проверяем, есть ли недостижимые вершины
        if any(d == float('inf') and j != i for j, d in enumerate(row)):
            eccentricity.append('+Infinity')
        else:
            # Эксцентриситет = максимальное расстояние до других вершин
            max_dist = max([d for d in row if d < float('inf')])
            eccentricity.append(max_dist)
    
    # Определяем радиус, диаметр, центральные и периферийные вершины
    if any(e == '+Infinity' for e in eccentricity):
        # Граф несвязный
        R = D = '+Infinity'
        central = peripherial = list(range(1, n + 1))
    else:
        # Граф связный
        D = max(eccentricity)  # Диаметр = максимальный эксцентриситет
        R = min(eccentricity)  # Радиус = минимальный эксцентриситет
        
        # Центральные вершины имеют эксцентриситет R
        central = [i + 1 for i, e in enumerate(eccentricity) if e == R]
        
        # Периферийные вершины имеют эксцентриситет D
        peripherial = [i + 1 for i, e in enumerate(eccentricity) if e == D]
    
    # Формируем результат
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