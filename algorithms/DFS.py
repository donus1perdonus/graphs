from utils.graph import Graph
from typing import List

def find_weakly_connected_components_dfs(graph: Graph) -> List[List[int]]:
    if not graph.is_directed():
        return find_connected_components_dfs(graph)  # если граф неориентированный
    
    visited = set()
    components = []
    
    for vertex in range(1, graph.size() + 1):
        if vertex not in visited:
            stack = [vertex]
            visited.add(vertex)
            component = []
            
            while stack:
                current = stack.pop()
                component.append(current)
                
                # Добавляем и входящие, и исходящие рёбра (игнорируем направленность)
                neighbors = set(graph.adjacency_list(current))
                # Находим вершины, которые ссылаются на current (входящие рёбра)
                for v in range(1, graph.size() + 1):
                    if graph.is_edge(v, current) and v not in neighbors:
                        neighbors.add(v)
                
                for neighbor in neighbors:
                    if neighbor not in visited:
                        visited.add(neighbor)
                        stack.append(neighbor)
            
            components.append(component)
    
    return components

def find_connected_components_dfs(graph: Graph) -> List[List[int]]:
    visited = set()
    components = []
    
    for vertex in range(1, graph.size() + 1):
        if vertex not in visited:
            stack = [vertex]
            visited.add(vertex)
            component = []
            
            while stack:
                current = stack.pop()
                component.append(current)
                
                for neighbor in graph.adjacency_list(current):
                    if neighbor not in visited:
                        visited.add(neighbor)
                        stack.append(neighbor)
            
            components.append(component)
    
    return components

def dfs_spanning_tree(graph: Graph):
    visited = set()
    edges = []
    
    def dfs(u):
        visited.add(u)
        for v in sorted(graph.adjacency_list(u)):  # Используем исправленный метод
            if v not in visited:
                edges.append((u, v))
                dfs(v)
    
    # Начинаем с вершины 1 (как в примере ответа)
    dfs(1)
    
    # Форматируем вывод
    output = ["Spanning tree:"]
    for u, v in sorted(edges):  # Сортируем ребра для единообразия
        output.append(f"{u}-{v}")
    
    return '\n'.join(output)