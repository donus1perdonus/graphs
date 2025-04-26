from typing import List

from utils.graph import Graph, LIST_OF_EDGES, LIST_OF_ADJACENCY, MATRIX_OF_ADJACENCY

from algorithms.BFS import find_weakly_connected_components_bfs, find_connected_components_bfs
from algorithms.DFS import find_weakly_connected_components_dfs, find_connected_components_dfs


# # Пример 1: Загрузка из списка рёбер
# g_adj_list = Graph("graph-tests\\task1\\list_of_edges_t1_001.txt",
#                     LIST_OF_EDGES)
# print("\nСписки смежности:")
# print("Количество вершин:", g_adj_list.size())
# print("Рёбра из вершины 1:", g_adj_list.list_of_edges(1))
# print("Матрица смежности (первые 5 строк):")
# for row in g_adj_list.adjacency_matrix()[:5]:
#     print(row[:5])  # выводим урезанную матрицу для наглядности

# # Пример 2: Загрузка из списков смежности
# g_edges = Graph("graph-tests\\task1\\list_of_adjacency_t1_001.txt", 
#                 LIST_OF_ADJACENCY)
# print("\nСписок рёбер:")
# print(g_edges.list_of_edges())
# print("Смежные вершины для 2:", g_edges.adjacency_list(2))
# print("Ориентированный?", g_edges.is_directed())

# # Пример 3: Загрузка из матрицы смежности
# g_matrix = Graph("graph-tests\\task1\\matrix_t1_001.txt", 
#                  MATRIX_OF_ADJACENCY)
# print("Матрица смежности:")
# print(g_matrix.adjacency_matrix())
# print("Рёбра графа:", g_matrix.list_of_edges())
# print("Смежные вершины для 2:", g_matrix.adjacency_list(2))
# print("Вес ребра (2, 3):", g_matrix.weight(2, 3))
# print("Ориентированный?", g_matrix.is_directed())

"""
1.  Алгоритм: DFS/BFS: поиск компонент связности графа и слабой связности в орграфе.
"""

def print_components(components: List[List[int]]) -> None:
    if len(components) == 1:
        print("Graph is connected")
    else:
        print("Graph is not connected")
    
    print("\nConnected components:")
    components_sorted = [sorted(comp) for comp in components]
    for component in components_sorted:
        print(component)

g = Graph("graph-tests\\task1\\matrix_t1_001.txt",
          MATRIX_OF_ADJACENCY)
components_dfs = find_connected_components_dfs(g)
components_bfs = find_connected_components_bfs(g)
print_components(components_dfs)
print_components(components_bfs)

# Пример 2: Ориентированный граф (список рёбер)
g_directed = Graph("graph-tests\\task1\\list_of_edges_t1_001.txt", 
                   LIST_OF_EDGES)
week_components_dfs = find_weakly_connected_components_dfs(g_directed)
week_components_bfs = find_weakly_connected_components_bfs(g_directed)
print_components(week_components_dfs)
print_components(week_components_bfs)