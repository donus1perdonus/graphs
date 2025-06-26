from utils import Graph
from typing import List, Set, Tuple


def find_bridges_and_cut_vertices(graph: Graph) -> Tuple[List[Tuple[int, int]], List[int]]:
    """
    Алгоритм Тарьяна для поиска мостов и шарниров в графе.
    
    Args:
        graph: Граф для анализа
        
    Returns:
        Кортеж (мосты, шарниры), где мосты - список рёбер, шарниры - список вершин
    """
    n = graph.size()
    
    # Массивы для алгоритма Тарьяна
    disc = [-1] * n  # Время обнаружения вершины
    low = [-1] * n   # Минимальное время достижимости
    parent = [-1] * n  # Родитель в дереве обхода
    visited = [False] * n
    time = 0
    
    bridges = []
    cut_vertices = set()
    
    def dfs(u: int):
        nonlocal time
        visited[u] = True
        disc[u] = low[u] = time
        time += 1
        
        children = 0  # Количество детей в дереве обхода
        
        for v in graph.adjacency_list(u + 1):
            v_idx = v - 1  # Переводим в 0-индексацию
            
            if not visited[v_idx]:
                children += 1
                parent[v_idx] = u
                dfs(v_idx)
                
                # Обновляем low[u]
                low[u] = min(low[u], low[v_idx])
                
                # Проверяем на мост
                if low[v_idx] > disc[u]:
                    bridges.append((min(u + 1, v), max(u + 1, v)))
                
                # Проверяем на шарнир
                if parent[u] == -1 and children > 1:
                    # Корень с несколькими детьми
                    cut_vertices.add(u + 1)
                elif parent[u] != -1 and low[v_idx] >= disc[u]:
                    # Не корень, но есть ребёнок с low[v] >= disc[u]
                    cut_vertices.add(u + 1)
                    
            elif v_idx != parent[u]:
                # Обратное ребро
                low[u] = min(low[u], disc[v_idx])
    
    # Запускаем DFS для всех компонент связности
    for u in range(n):
        if not visited[u]:
            dfs(u)
    
    # Не сортируем bridges, только cut_vertices
    return bridges, sorted(list(cut_vertices))


def solve_task(graph: Graph) -> str:
    """
    Решает задачу поиска мостов и шарниров в графе.
    
    Args:
        graph: Граф для анализа
        
    Returns:
        Строка с результатом анализа
    """
    bridges, cut_vertices = find_bridges_and_cut_vertices(graph)
    
    result = "Bridges:\n"
    if bridges:
        result += " " + str(bridges) + "\n"
    else:
        result += " []\n"
    
    result += "Cut vertices:\n"
    if cut_vertices:
        result += " " + str(cut_vertices) + "\n"
    else:
        result += " []\n"
    
    return result.strip() 