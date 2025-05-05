from collections import deque
from typing import Tuple, Optional, Set

from utils.graph import Graph

def is_bipartite(graph: Graph) -> Tuple[bool, Optional[Tuple[Set[int], Set[int]]]]:
    """Проверка двудольности для новой структуры Graph"""
    if graph.is_directed():
        return False, None  # Алгоритм работает только для неориентированных графов
    
    color = {}
    bipartition = (set(), set())
    n = graph.size()
    
    for start in range(1, n + 1):
        if start not in color:
            queue = deque([start])
            color[start] = 0
            bipartition[0].add(start)
            
            while queue:
                u = queue.popleft()
                for v in graph.adjacency_list(u):  # Используем adjacency_list из нового Graph
                    if v not in color:
                        color[v] = 1 - color[u]
                        bipartition[color[v]].add(v)
                        queue.append(v)
                    elif color[v] == color[u]:
                        return False, None
    
    return True, bipartition