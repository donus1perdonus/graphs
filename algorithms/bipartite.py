from collections import deque
from typing import Tuple, Optional, Set

from utils.graph import Graph

def is_bipartite(graph: Graph) -> Tuple[bool, Optional[Tuple[Set[int], Set[int]]]]:
    n = graph.size()
    color = {}
    bipartition = (set(), set())
    
    # Преобразуем матрицу смежности в список смежности (0-based)
    adj = [[] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if graph.weight(i+1, j+1) != 0:  # Проверяем наличие ребра
                adj[i].append(j)
    
    for start in range(n):
        if start not in color:
            queue = deque([start])
            color[start] = 0
            bipartition[0].add(start)
            
            while queue:
                u = queue.popleft()
                for v in adj[u]:
                    if v not in color:
                        color[v] = 1 - color[u]
                        bipartition[color[v]].add(v)
                        queue.append(v)
                    elif color[v] == color[u]:
                        return False, None
    
    return True, bipartition