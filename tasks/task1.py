from typing import List, Set
from utils import Graph
from collections import deque
import sys


def find_connected_components_dfs(graph: Graph) -> List[List[int]]:
    """
    Находит компоненты связности графа с использованием итеративного DFS.
    
    Args:
        graph: граф для анализа
        
    Returns:
        список компонент связности, где каждая компонента - список номеров вершин
    """
    visited = set()
    components = []
    
    def dfs_iterative(start_vertex: int) -> List[int]:
        """Итеративный DFS для поиска компоненты связности."""
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
    
    Args:
        graph: граф для анализа
        
    Returns:
        список компонент связности, где каждая компонента - список номеров вершин
    """
    visited = set()
    components = []
    
    def bfs(start_vertex: int) -> List[int]:
        """BFS для поиска компоненты связности."""
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
    
    Args:
        graph: орграф для анализа
        
    Returns:
        список слабо связных компонент
    """
    if not graph.is_directed():
        # Если граф неориентированный, используем обычный поиск компонент связности
        return find_connected_components_dfs(graph)
    
    # Для орграфа создаем неориентированный граф (матрицу смежности)
    # и используем итеративный DFS для поиска компонент связности
    visited = set()
    components = []
    
    def dfs_undirected_iterative(vertex: int) -> List[int]:
        """Итеративный DFS для неориентированного представления орграфа."""
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
    
    Args:
        graph: граф для анализа
        algorithm: алгоритм ('dfs' или 'bfs')
        
    Returns:
        строка с результатом в требуемом формате
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
        else:
            components = find_connected_components_bfs(graph)
    
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