"""
Задание 1: Поиск компонент связности

Реализует алгоритмы поиска компонент связности для неориентированных графов
и слабо связных компонент для орграфов.

Алгоритмы:
- DFS (Depth-First Search) - поиск в глубину
- BFS (Breadth-First Search) - поиск в ширину

Временная сложность: O(V + E), где V - количество вершин, E - количество рёбер
Пространственная сложность: O(V)

Автор: [Ваше имя]
Дата: [Дата создания]
"""

from typing import List, Set
from utils import Graph
from collections import deque
import sys


def find_connected_components_dfs(graph: Graph) -> List[List[int]]:
    """
    Находит компоненты связности графа с использованием итеративного DFS.
    
    Алгоритм:
    1. Проходим по всем вершинам графа
    2. Для каждой непосещённой вершины запускаем DFS
    3. Все вершины, достижимые из стартовой, образуют компоненту связности
    
    Args:
        graph: граф для анализа
    """
    visited = set()
    components = []
    
    def dfs_iterative(start_vertex: int) -> List[int]:
        """
        Итеративный DFS для поиска компоненты связности.
        
        Использует стек вместо рекурсии для избежания переполнения стека
        на больших графах.
        
        Args:
            start_vertex: стартовая вершина для поиска
        """
        component = []
        stack = [start_vertex]
        visited.add(start_vertex)
        
        while stack:
            vertex = stack.pop()
            component.append(vertex)
            
            # Добавляем всех непосещенных соседей в стек
            for neighbor in graph.adjacency_list(vertex):
                if neighbor not in visited:
                    visited.add(neighbor)
                    stack.append(neighbor)
        
        return component
    
    # Проходим по всем вершинам
    for vertex in range(1, graph.size() + 1):
        if vertex not in visited:
            component = dfs_iterative(vertex)
            components.append(component)
    
    return components


def find_connected_components_bfs(graph: Graph) -> List[List[int]]:
    """
    Находит компоненты связности графа с использованием BFS.
    
    Алгоритм:
    1. Проходим по всем вершинам графа
    2. Для каждой непосещённой вершины запускаем BFS
    3. Все вершины, достижимые из стартовой, образуют компоненту связности
    
    BFS обеспечивает поиск в ширину, что может быть полезно для некоторых задач.
    
    Args:
        graph: граф для анализа
        
    Returns:
        список компонент связности, где каждая компонента - список номеров вершин
        
    Пример:
        >>> graph = Graph("test.txt", "matrix")
        >>> components = find_connected_components_bfs(graph)
        >>> print(components)
        [[1, 2, 3], [4, 5], [6]]
    """
    visited = set()
    components = []
    
    def bfs(start_vertex: int) -> List[int]:
        """
        BFS для поиска компоненты связности.
        
        Использует очередь для обеспечения поиска в ширину.
        
        Args:
            start_vertex: стартовая вершина для поиска
            
        Returns:
            список вершин в компоненте связности
        """
        component = []
        queue = deque([start_vertex])
        visited.add(start_vertex)
        
        while queue:
            vertex = queue.popleft()
            component.append(vertex)
            
            # Добавляем всех непосещенных соседей в очередь
            for neighbor in graph.adjacency_list(vertex):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
        
        return component
    
    # Проходим по всем вершинам
    for vertex in range(1, graph.size() + 1):
        if vertex not in visited:
            component = bfs(vertex)
            components.append(component)
    
    return components


def find_weakly_connected_components(graph: Graph) -> List[List[int]]:
    """
    Находит слабо связные компоненты орграфа.
    
    Слабо связная компонента - это компонента связности неориентированного графа,
    полученного из орграфа удалением ориентации рёбер.
    
    Алгоритм:
    1. Если граф неориентированный, используем обычный поиск компонент связности
    2. Для орграфа создаём неориентированное представление
    3. Применяем DFS для поиска компонент связности в неориентированном графе
    
    Args:
        graph: орграф для анализа
        
    Returns:
        список слабо связных компонент
        
    Пример:
        >>> graph = Graph("digraph.txt", "matrix")  # орграф
        >>> components = find_weakly_connected_components(graph)
        >>> print(components)
        [[1, 2, 3], [4, 5]]
    """
    if not graph.is_directed():
        # Если граф неориентированный, используем обычный поиск компонент связности
        return find_connected_components_dfs(graph)
    
    # Для орграфа создаем неориентированный граф (матрицу смежности)
    # и используем итеративный DFS для поиска компонент связности
    visited = set()
    components = []
    
    def dfs_undirected_iterative(vertex: int) -> List[int]:
        """
        Итеративный DFS для неориентированного представления орграфа.
        
        При поиске соседей проверяем рёбра в обе стороны, так как
        мы работаем с неориентированным представлением орграфа.
        
        Args:
            vertex: текущая вершина
            
        Returns:
            список вершин в слабо связной компоненте
        """
        component = []
        stack = [vertex]
        visited.add(vertex)
        
        while stack:
            current_vertex = stack.pop()
            component.append(current_vertex)
            
            # Проверяем все возможные рёбра (в обе стороны)
            for neighbor in range(1, graph.size() + 1):
                if neighbor not in visited and (graph.is_edge(current_vertex, neighbor) or graph.is_edge(neighbor, current_vertex)):
                    visited.add(neighbor)
                    stack.append(neighbor)
        
        return component
    
    # Проходим по всем вершинам
    for vertex in range(1, graph.size() + 1):
        if vertex not in visited:
            component = dfs_undirected_iterative(vertex)
            components.append(component)
    
    return components


def solve_task(graph: Graph, algorithm: str = 'dfs') -> str:
    """
    Решает задачу 1: поиск компонент связности.
    
    Основная функция для решения задачи. Автоматически определяет тип графа
    (ориентированный или неориентированный) и применяет соответствующий алгоритм.
    
    Args:
        graph: граф для анализа
        algorithm: алгоритм ('dfs' или 'bfs') - используется только для неориентированных графов
        
    Returns:
        строка с результатом в требуемом формате:
        - "Graph is connected" / "Graph is not connected" для неориентированных графов
        - "Diraph is connected" / "Diraph is not connected" для орграфов
        - Список компонент связности
        
    Пример вывода:
        Graph is not connected
        
        Connected components:
        [1, 2, 3, 5]
        [4, 6]
        
    Raises:
        ValueError: если указан неподдерживаемый алгоритм
    """
    # Автоматически увеличиваем лимит рекурсии для больших графов
    if graph.size() > 1000:
        sys.setrecursionlimit(max(sys.getrecursionlimit(), graph.size() * 2))
    
    is_digraph = graph.is_directed()
    if is_digraph:
        components = find_weakly_connected_components(graph)
    else:
        if algorithm == 'dfs':
            components = find_connected_components_dfs(graph)
        elif algorithm == 'bfs':
            components = find_connected_components_bfs(graph)
        else:
            raise ValueError(f"Неподдерживаемый алгоритм: {algorithm}")
    
    # Формируем результат
    result = []
    
    if len(components) == 1:
        result.append("Diraph is connected" if is_digraph else "Graph is connected")
    else:
        result.append("Diraph is not connected" if is_digraph else "Graph is not connected")
    
    result.append("")
    result.append("Connected components:")
    
    # Сортируем компоненты по размеру (по убыванию) и по первому элементу
    components.sort(key=lambda x: (len(x), x[0]))
    
    for component in components:
        # Сортируем вершины в компоненте
        component.sort()
        result.append(str(component))
    
    return "\n".join(result)


def test_task1():
    """Тестирует задачу 1 на примере из файлов."""
    import os
    
    # Пути к тестовым файлам
    base_path = "graph-tests/task1"
    matrix_file = os.path.join(base_path, "matrix_t1_001.txt")
    adjacency_file = os.path.join(base_path, "adjacency_list_t1_001.txt")
    edges_file = os.path.join(base_path, "list_of_edges_t1_001.txt")
    answer_file = os.path.join(base_path, "ans_t1_001.txt")
    
    print("Тестирование задачи 1:")
    print("=" * 50)
    
    # Тестируем с матрицей смежности
    if os.path.exists(matrix_file):
        print("\n1. Тест с матрицей смежности:")
        graph = Graph(matrix_file, 'matrix')
        result = solve_task(graph, 'dfs')
        print(result)
        
        # Сравниваем с ожидаемым результатом
        if os.path.exists(answer_file):
            with open(answer_file, 'r', encoding='utf-8') as f:
                expected = f.read().strip()
            print(f"\nОжидаемый результат:\n{expected}")
            print(f"\nРезультат {'совпадает' if result.strip() == expected else 'НЕ совпадает'}")
    
    # Тестируем со списками смежности
    if os.path.exists(adjacency_file):
        print("\n2. Тест со списками смежности:")
        graph = Graph(adjacency_file, 'adjacency_list')
        result = solve_task(graph, 'dfs')
        print(result)
    
    # Тестируем со списком рёбер
    if os.path.exists(edges_file):
        print("\n3. Тест со списком рёбер:")
        graph = Graph(edges_file, 'edges')
        result = solve_task(graph, 'dfs')
        print(result)
    
    print("\n" + "=" * 50)


if __name__ == "__main__":
    test_task1() 