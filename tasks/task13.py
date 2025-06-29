from typing import List, Tuple, Optional
from collections import deque


def is_bipartite(graph) -> Tuple[bool, Optional[List[int]]]:
    """
    Проверяет, является ли граф двудольным, используя BFS.
    
    Returns:
        Tuple[bool, Optional[List[int]]]: (is_bipartite, coloring)
        Если граф двудольный, возвращает True и раскраску вершин (0 или 1)
        Если не двудольный, возвращает False и None
    """
    n = graph.size()
    coloring = [-1] * n  # -1 означает, что вершина не раскрашена
    queue = deque()
    
    # Проверяем все компоненты связности
    for start in range(n):
        if coloring[start] == -1:
            coloring[start] = 0
            queue.append(start)
            
            while queue:
                vertex = queue.popleft()
                current_color = coloring[vertex]
                
                # Проверяем всех соседей
                for neighbor in graph.adjacency_list(vertex + 1):  # +1 для 1-индексации
                    neighbor_idx = neighbor - 1  # Переводим в 0-индексацию
                    
                    if coloring[neighbor_idx] == -1:
                        # Раскрашиваем соседа в противоположный цвет
                        coloring[neighbor_idx] = 1 - current_color
                        queue.append(neighbor_idx)
                    elif coloring[neighbor_idx] == current_color:
                        # Нашли конфликт - граф не двудольный
                        return False, None
    
    return True, coloring


def find_maximum_matching(graph) -> Tuple[int, List[Tuple[int, int]]]:
    """
    Находит максимальное паросочетание в двудольном графе используя алгоритм Куна.
    
    Returns:
        Tuple[int, List[Tuple[int, int]]]: (размер паросочетания, список рёбер)
    """
    n = graph.size()
    
    # Проверяем, является ли граф двудольным
    is_bip, coloring = is_bipartite(graph)
    if not is_bip or coloring is None:
        return 0, []
    
    # Разделяем вершины на две доли
    left_partition = []
    right_partition = []
    for i in range(n):
        if coloring[i] == 0:
            left_partition.append(i)
        else:
            right_partition.append(i)
    
    # Сортируем доли для детерминированного результата
    left_partition.sort()
    right_partition.sort()
    
    # Строим отображения: номер вершины -> индекс в доле
    left_index = {v: i for i, v in enumerate(left_partition)}
    right_index = {v: i for i, v in enumerate(right_partition)}
    
    # Строим списки смежности для левой доли (по индексам правой доли)
    left_adj = [[] for _ in range(len(left_partition))]
    for i, left_vertex in enumerate(left_partition):
        neighbors = graph.adjacency_list(left_vertex + 1)
        for neighbor in neighbors:
            neighbor_idx = neighbor - 1
            if neighbor_idx in right_index:
                left_adj[i].append(right_index[neighbor_idx])
        left_adj[i].sort()  # Для детерминированности
    
    left_size = len(left_partition)
    right_size = len(right_partition)
    
    # Массив для хранения паросочетания
    match_left = [-1] * left_size  # match_left[i] = j означает, что левая вершина i соединена с правой j
    match_right = [-1] * right_size  # match_right[j] = i означает, что правая вершина j соединена с левой i
    
    def dfs(left_vertex: int, visited: List[bool]) -> bool:
        """DFS для поиска увеличивающего пути."""
        if visited[left_vertex]:
            return False
        visited[left_vertex] = True
        
        # Ищем все соседние правые вершины
        for right_vertex in left_adj[left_vertex]:
            # Если правая вершина не занята или можно найти альтернативный путь
            if match_right[right_vertex] == -1 or dfs(match_right[right_vertex], visited):
                match_left[left_vertex] = right_vertex
                match_right[right_vertex] = left_vertex
                return True
        
        return False
    
    # Находим максимальное паросочетание
    max_matching = 0
    for left_vertex in range(left_size):
        visited = [False] * left_size
        if dfs(left_vertex, visited):
            max_matching += 1
    
    # Восстанавливаем рёбра паросочетания (используем 0-индексацию)
    matching_edges = []
    for left_vertex in range(left_size):
        if match_left[left_vertex] != -1:
            left_original = left_partition[left_vertex]  # 0-индексация
            right_original = right_partition[match_left[left_vertex]]  # 0-индексация
            matching_edges.append((left_original, right_original))
    
    # Сортируем рёбра по возрастанию (по первой, затем по второй вершине)
    matching_edges.sort()
    
    return max_matching, matching_edges


def solve_task(graph) -> str:
    """
    Решает задачу поиска максимального паросочетания в двудольном графе.
    
    Args:
        graph: объект графа
        
    Returns:
        str: результат в требуемом формате
    """
    # Проверяем, является ли граф двудольным
    is_bip, _ = is_bipartite(graph)
    
    if not is_bip:
        return "Graph is not bipartite."
    
    # Находим максимальное паросочетание
    max_matching_size, matching_edges = find_maximum_matching(graph)
    
    # Формируем результат
    result = f"Maximum matching number: {max_matching_size}.\n"
    result += "Matching maximum size:\n"
    result += f"\t{matching_edges}.\n"
    
    return result 


"""
Задание 13: Максимальное паросочетание в двудольном графе

Реализует алгоритм Куна для поиска максимального паросочетания.

Алгоритм:
- Кун (DFS для поиска увеличивающих путей)

Временная сложность: O(V*E)
Пространственная сложность: O(V)

Пример вывода:
    Maximum matching number: 3.
    Matching maximum size:
    	[(1, 4), (2, 5), (3, 6)].
""" 