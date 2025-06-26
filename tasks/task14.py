from typing import List, Tuple, Optional
from collections import deque


def find_source_and_sink(graph) -> Tuple[int, int]:
    """
    Находит источник и сток в сети.
    Источник - вершина с наибольшим исходящим потоком.
    Сток - вершина с наибольшим входящим потоком.
    
    Returns:
        Tuple[int, int]: (источник, сток) в 1-индексации
    """
    n = graph.size()
    out_flow = [0] * n
    in_flow = [0] * n
    
    # Вычисляем исходящий и входящий потоки для каждой вершины
    for i in range(n):
        for j in range(n):
            weight = graph.weight(i + 1, j + 1)  # +1 для 1-индексации
            out_flow[i] += weight
            in_flow[j] += weight
    
    # Находим вершины с максимальными потоками
    source = max(range(n), key=lambda x: out_flow[x]) + 1  # +1 для 1-индексации
    sink = max(range(n), key=lambda x: in_flow[x]) + 1     # +1 для 1-индексации
    
    return source, sink


def ford_fulkerson(graph, source: int, sink: int) -> Tuple[int, List[List[int]]]:
    """
    Реализация алгоритма Форда-Фалкерсона для поиска максимального потока.
    
    Args:
        graph: объект графа
        source: источник (1-индексация)
        sink: сток (1-индексация)
        
    Returns:
        Tuple[int, List[List[int]]]: (максимальный поток, матрица потоков)
    """
    n = graph.size()
    
    # Создаем остаточную сеть
    residual = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            residual[i][j] = graph.weight(i + 1, j + 1)  # +1 для 1-индексации
    
    # Матрица потоков
    flow = [[0] * n for _ in range(n)]
    
    # Функция для поиска увеличивающего пути с помощью BFS
    def bfs() -> Optional[List[int]]:
        """Находит увеличивающий путь от источника к стоку."""
        parent = [-1] * n
        visited = [False] * n
        queue = deque()
        
        source_idx = source - 1  # Переводим в 0-индексацию
        sink_idx = sink - 1      # Переводим в 0-индексацию
        
        queue.append(source_idx)
        visited[source_idx] = True
        
        while queue and parent[sink_idx] == -1:
            u = queue.popleft()
            
            for v in range(n):
                if not visited[v] and residual[u][v] > 0:
                    visited[v] = True
                    parent[v] = u
                    queue.append(v)
                    
                    if v == sink_idx:
                        break
        
        # Восстанавливаем путь
        if parent[sink_idx] == -1:
            return None
        
        path = []
        current = sink_idx
        while current != -1:
            path.append(current)
            current = parent[current]
        path.reverse()
        
        return path
    
    # Основной цикл алгоритма
    max_flow = 0
    
    while True:
        path = bfs()
        if not path:
            break
        
        # Находим минимальную пропускную способность на пути
        min_capacity = float('inf')
        for i in range(len(path) - 1):
            u, v = path[i], path[i + 1]
            min_capacity = min(min_capacity, residual[u][v])
        
        # Обновляем остаточную сеть и потоки
        for i in range(len(path) - 1):
            u, v = path[i], path[i + 1]
            residual[u][v] -= min_capacity
            residual[v][u] += min_capacity
            
            # Обновляем матрицу потоков
            if graph.weight(u + 1, v + 1) > 0:  # +1 для 1-индексации
                flow[u][v] += min_capacity
            else:
                flow[v][u] -= min_capacity
        
        max_flow += min_capacity
    
    return int(max_flow), flow


def solve_task(graph) -> str:
    """
    Решает задачу поиска максимального потока в сети.
    
    Args:
        graph: объект графа
        
    Returns:
        str: результат в требуемом формате
    """
    # Находим источник и сток
    source, sink = find_source_and_sink(graph)
    
    # Находим максимальный поток
    max_flow_value, flow_matrix = ford_fulkerson(graph, source, sink)
    
    # Формируем результат
    result = f"Maximum flow value: {max_flow_value}.\n"
    result += f"Source: {source}, sink: {sink}.\n"
    result += "Flow:\n"
    
    # Выводим ненулевые потоки только по рёбрам, которые есть в исходном графе
    n = graph.size()
    flow_edges = []
    for i in range(n):
        for j in range(n):
            if flow_matrix[i][j] > 0 and graph.weight(i + 1, j + 1) > 0:
                flow_edges.append((i + 1, j + 1, flow_matrix[i][j]))  # +1 для 1-индексации

    # Сортируем рёбра по первой вершине, затем по второй
    flow_edges.sort()

    for u, v, flow_value in flow_edges:
        result += f"{u}-{v} : {flow_value}\n"

    return result 