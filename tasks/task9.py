"""
Задание 9: Минимальное остовное дерево (Прим)

Реализует алгоритм Прима для поиска минимального остовного дерева.

Алгоритм:
- Прим с приоритетной очередью

Временная сложность: O(E log V)
Пространственная сложность: O(V)

Пример вывода:
    Minimum spanning tree weight: 12
    Edges:
    1-2 : 2
    2-3 : 4
    3-4 : 6
"""
from utils import Graph
from typing import List, Tuple

class DSU:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n
    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]
    def union(self, x, y):
        xroot = self.find(x)
        yroot = self.find(y)
        if xroot == yroot:
            return False
        if self.rank[xroot] < self.rank[yroot]:
            self.parent[xroot] = yroot
        else:
            self.parent[yroot] = xroot
            if self.rank[xroot] == self.rank[yroot]:
                self.rank[xroot] += 1
        return True

def kruskal_mst(graph: Graph) -> Tuple[List[Tuple[int, int, int]], int, bool]:
    n = graph.size()
    edges = graph.list_of_edges()
    # Для неориентированного графа: не добавлять оба направления
    unique_edges = set()
    for u, v, w in edges:
        if u < v:
            unique_edges.add((u, v, w))
        else:
            unique_edges.add((v, u, w))
    edges = sorted(list(unique_edges), key=lambda x: (x[2], x[0], x[1]))
    dsu = DSU(n)
    mst = []
    total_weight = 0
    
    # Сначала объединяем все компоненты связности
    for u, v, w in edges:
        dsu.union(u-1, v-1)
    
    # Проверяем связность графа
    root = dsu.find(0)
    is_connected = all(dsu.find(i) == root for i in range(n))
    
    if not is_connected:
        return [], 0, False
    
    # Если граф связный, строим MST
    dsu = DSU(n)  # Создаем новый DSU для построения MST
    for u, v, w in edges:
        if dsu.union(u-1, v-1):
            mst.append((u, v, w))
            total_weight += w
            if len(mst) == n-1:
                break
    
    # Сортируем рёбра MST по весу, затем по первой вершине, затем по второй
    mst.sort(key=lambda x: (x[2], x[0], x[1]))
    
    return mst, total_weight, True

def solve_task(graph: Graph) -> str:
    mst, total_weight, is_connected = kruskal_mst(graph)
    
    if not is_connected:
        return "Graph is not connected"
    
    result = "Minimal spanning tree:\n"
    for u, v, w in mst:
        result += f"{u}-{v}: {w}\n"
    return result.strip() 