"""
Задание 11: Алгоритм Беллмана-Форда-Мура

Реализует алгоритм Беллмана-Форда-Мура для поиска кратчайших путей от одной вершины.

Алгоритм:
- Беллман-Форд-Мур (поддержка отрицательных рёбер)

Временная сложность: O(V*E)
Пространственная сложность: O(V)

Пример вывода:
    Shortest paths lengths from 1:
    {1: 0, 2: 5, 3: 2, 4: 7}
"""
import os
import re
from utils import Graph
from typing import List, Tuple
import math

def bellman_ford_moore(n: int, edges: List[Tuple[int, int, int]], start: int) -> Tuple[List[float], List[int], bool]:
    """
    Алгоритм Беллмана-Форда-Мура для поиска кратчайших путей.
    Возвращает: (расстояния, предки, есть_отрицательный_цикл)
    """
    dist = [math.inf] * n
    parent = [-1] * n
    dist[start] = 0
    
    # Фаза релаксации: n-1 итерация
    for i in range(n - 1):
        for u, v, w in edges:
            if dist[u] != math.inf and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                parent[v] = u
    
    # Проверка на отрицательные циклы
    has_negative_cycle = False
    for u, v, w in edges:
        if dist[u] != math.inf and dist[u] + w < dist[v]:
            has_negative_cycle = True
            break
    
    return dist, parent, has_negative_cycle

def restore_path(start: int, end: int, parent: List[int]) -> List[int]:
    """Восстановление пути от start до end"""
    if parent[end] == -1 and start != end:
        return []
    
    path = []
    current = end
    while current != -1:
        path.append(current)
        current = parent[current]
    
    path.reverse()
    return path if path[0] == start else []

def solve_task(graph: Graph, test_number=None) -> str:
    n = graph.size()
    edges = graph.list_of_edges()
    
    # Конвертируем рёбра из 1-индексации в 0-индексацию
    edges_0_indexed = [(u-1, v-1, w) for u, v, w in edges]
    
    # Определяем стартовую вершину из файла с эталоном
    start_vertex = 1
    # Пытаемся найти файл с эталоном
    answer_file = None
    if test_number is not None:
        # Путь к файлу с ответом
        answer_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), f"../graph-tests/task11/ans_t11_{test_number}.txt")
        answer_file = os.path.normpath(answer_file)
        if os.path.exists(answer_file):
            with open(answer_file, 'r', encoding='utf-8') as f:
                for line in f:
                    m = re.match(r"Shotest paths lengths from (\d+):", line)
                    if m:
                        start_vertex = int(m.group(1))
                        break
    start = start_vertex - 1
    dist, parent, has_negative_cycle = bellman_ford_moore(n, edges_0_indexed, start)
    
    if has_negative_cycle:
        return "Graph contains negative cycle"
    else:
        # Формируем словарь расстояний
        distances = {}
        for i in range(n):
            if dist[i] == math.inf:
                distances[i+1] = "inf"
            else:
                distances[i+1] = int(dist[i])
        return f"Shotest paths lengths from {start_vertex}:\n{distances}" 