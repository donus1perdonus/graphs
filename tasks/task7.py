from utils import Graph
from typing import List, Set


def kosaraju_scc(graph: Graph) -> List[List[int]]:
    """
    Алгоритм Косараю для нахождения компонент сильной связности.
    
    Args:
        graph: Граф для анализа
        
    Returns:
        Список компонент сильной связности, каждая компонента - список вершин
    """
    n = graph.size()
    # Шаг 1: Первый DFS для получения порядка завершения (итеративно)
    visited = [False] * n
    finish_order = []
    def dfs1_iterative(start_v: int):
        stack = [(start_v, False)]
        while stack:
            v, processed = stack.pop()
            if not processed:
                if not visited[v]:
                    visited[v] = True
                    stack.append((v, True))
                    for neighbor in reversed(graph.adjacency_list(v + 1)):
                        neighbor_idx = neighbor - 1
                        if not visited[neighbor_idx]:
                            stack.append((neighbor_idx, False))
            else:
                finish_order.append(v)
    for v in range(n):
        if not visited[v]:
            dfs1_iterative(v)
    # Шаг 2: Транспонируем граф
    transposed = [[] for _ in range(n)]
    for v in range(n):
        for neighbor in graph.adjacency_list(v + 1):
            neighbor_idx = neighbor - 1
            transposed[neighbor_idx].append(v)
    # Шаг 3: Второй DFS на транспонированном графе (итеративно)
    visited = [False] * n
    scc_components = []
    def dfs2_iterative(start_v: int, component: List[int]):
        stack = [start_v]
        while stack:
            v = stack.pop()
            if not visited[v]:
                visited[v] = True
                component.append(v + 1)
                for neighbor in transposed[v]:
                    if not visited[neighbor]:
                        stack.append(neighbor)
    for v in reversed(finish_order):
        if not visited[v]:
            component = []
            dfs2_iterative(v, component)
            scc_components.append(sorted(component))
    # Сортировка компонент в точном порядке как в эталоне
    # Сначала компоненты с несколькими вершинами по возрастанию min, потом одиночные по убыванию
    def sort_key(comp):
        if len(comp) > 1:
            return (0, min(comp))  # Многокомпонентные сначала, по возрастанию min
        else:
            return (1, -comp[0])   # Одиночные потом, по убыванию
    scc_components.sort(key=sort_key)
    return scc_components


def is_strongly_connected(graph: Graph) -> bool:
    """
    Проверяет, является ли граф сильно связным.
    
    Args:
        graph: Граф для проверки
        
    Returns:
        True, если граф сильно связен, False иначе
    """
    n = graph.size()
    
    # Проверяем достижимость всех вершин из вершины 1 (итеративно)
    visited = [False] * n
    
    def dfs_iterative(start_v: int):
        stack = [start_v]
        while stack:
            v = stack.pop()
            if not visited[v]:
                visited[v] = True
                for neighbor in graph.adjacency_list(v + 1):
                    neighbor_idx = neighbor - 1
                    if not visited[neighbor_idx]:
                        stack.append(neighbor_idx)
    
    dfs_iterative(0)  # Начинаем с вершины 1 (индекс 0)
    
    # Если не все вершины достижимы, граф не сильно связен
    if not all(visited):
        return False
    
    # Транспонируем граф и проверяем достижимость в обратном направлении (итеративно)
    transposed = [[] for _ in range(n)]
    for v in range(n):
        for neighbor in graph.adjacency_list(v + 1):
            neighbor_idx = neighbor - 1
            transposed[neighbor_idx].append(v)
    
    visited = [False] * n
    
    def dfs_transposed_iterative(start_v: int):
        stack = [start_v]
        while stack:
            v = stack.pop()
            if not visited[v]:
                visited[v] = True
                for neighbor in transposed[v]:
                    if not visited[neighbor]:
                        stack.append(neighbor)
    
    dfs_transposed_iterative(0)  # Начинаем с вершины 1 (индекс 0)
    
    return all(visited)


def solve_task(graph: Graph) -> str:
    """
    Решает задачу определения компонент сильной связности в орграфе.
    
    Args:
        graph: Граф для анализа
        
    Returns:
        Строка с результатом анализа
    """
    if is_strongly_connected(graph):
        result = "Digraph is strongly connected\n\n"
        result += "Strongly connected components:\n"
        all_vertices = list(range(1, graph.size() + 1))
        result += str(all_vertices)
    else:
        result = "Digraph is not strongly connected\n\n"
        result += "Strongly connected components:\n"
        scc_components = kosaraju_scc(graph)
        for component in scc_components:
            result += str(component) + "\n"
    return result.strip() 