"""
Задание 5: Проверка двудольности графа

Реализует алгоритм проверки двудольности с помощью раскраски в два цвета (BFS).

Алгоритм:
- BFS с раскраской вершин

Временная сложность: O(V + E)
Пространственная сложность: O(V)

Пример вывода:
    Graph is bipartite.
    Partition 1: [1, 3, 5]
    Partition 2: [2, 4, 6]
"""
from utils import Graph
from collections import deque
import sys


def is_bipartite(graph: Graph):
    n = graph.size()
    color = [-1] * n  # 0-индексация
    part1, part2 = [], []
    
    for start in range(n):  # от 0 до n-1
        if color[start] == -1:
            queue = deque([start])
            color[start] = 0
            part1.append(start)
            
            while queue:
                v = queue.popleft()
                for u in graph.adjacency_list(v + 1):  # +1 для перехода к 1-индексации
                    u = u - 1  # переводим обратно в 0-индексацию
                    if color[u] == -1:
                        color[u] = 1 - color[v]
                        if color[u] == 0:
                            part1.append(u)
                        else:
                            part2.append(u)
                        queue.append(u)
                    elif color[u] == color[v]:
                        return False, [], []
    
    return True, sorted(part1), sorted(part2)


def solve_task(graph: Graph, **kwargs) -> str:
    if graph.size() > 1000:
        sys.setrecursionlimit(max(sys.getrecursionlimit(), graph.size() * 2))
    
    bipartite, part1, part2 = is_bipartite(graph)
    
    if bipartite:
        result = []
        result.append("First set:")
        result.append(f"\t{{{', '.join(map(str, part1))}}},")
        result.append("Second set:")
        result.append(f"\t{{{', '.join(map(str, part2))}}}.")
        return "\n".join(result)
    else:
        return "Graph is not bipartite." 