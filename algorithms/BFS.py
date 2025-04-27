from utils.graph import Graph
from typing import List
from collections import deque


def find_weakly_connected_components_bfs(graph: Graph) -> List[List[int]]:
    if not graph.is_directed():
        return find_connected_components_bfs(graph)  # если граф неориентированный
    
    visited = set()
    components = []
    
    for vertex in range(1, graph.size() + 1):
        if vertex not in visited:
            queue = deque([vertex])
            visited.add(vertex)
            component = []
            
            while queue:
                current = queue.popleft()
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
                        queue.append(neighbor)
            
            components.append(component)
    
    return components


def find_connected_components_bfs(graph: Graph) -> List[List[int]]:
    visited = set()
    components = []
    
    for vertex in range(1, graph.size() + 1):
        if vertex not in visited:
            queue = deque([vertex])
            visited.add(vertex)
            component = []
            
            while queue:
                current = queue.popleft()
                component.append(current)
                
                for neighbor in graph.adjacency_list(current):
                    if neighbor not in visited:
                        visited.add(neighbor)
                        queue.append(neighbor)
            
            components.append(component)
    
    return components

def get_bfs_spanning_tree(graph: Graph) -> str:
    if graph.is_directed():
        raise ValueError("Граф должен быть неориентированным")
    
    visited = set()
    edges = []
    queue = deque([1])
    visited.add(1)
    
    while queue:
        u = queue.popleft()
        for v in sorted(graph.adjacency_list(u)):  # Сортируем соседей
            if v not in visited:
                visited.add(v)
                edges.append((min(u, v), max(u, v)))
                queue.append(v)
    
    # Форматируем вывод
    output = ["Spanning tree:"]
    for u, v in sorted(edges):
        output.append(f"{u}-{v}")
    
    return '\n'.join(output)