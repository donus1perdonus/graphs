from utils.graph import Graph, GraphType

from typing import List, Tuple

def find_bridges_and_cut_vertices(graph: Graph) -> Tuple[List[Tuple[int, int]], List[int]]:
    if graph.is_directed():
        raise ValueError("Граф должен быть неориентированным")
    
    n = graph.size()
    visited = [False] * (n + 1)
    tin = [0] * (n + 1)
    low = [0] * (n + 1)
    timer = 1
    bridges = []
    cut_vertices = set()
    
    def dfs(u: int, parent: int = -1):
        nonlocal timer
        visited[u] = True
        tin[u] = low[u] = timer
        timer += 1
        children = 0
        
        for v in graph.adjacency_list(u):
            if v == parent:
                continue
            if visited[v]:
                low[u] = min(low[u], tin[v])
            else:
                dfs(v, u)
                low[u] = min(low[u], low[v])
                if low[v] > tin[u]:
                    bridges.append((min(u, v), max(u, v)))  # Сохраняем ребро упорядоченным
                if low[v] >= tin[u] and parent != -1:
                    cut_vertices.add(u)
                children += 1
        if parent == -1 and children > 1:
            cut_vertices.add(u)
    
    for u in range(1, n + 1):
        if not visited[u]:
            dfs(u)
    
    return sorted(bridges), sorted(cut_vertices)

def print_bridges_and_cut_vertices(graph: Graph) -> str:
    bridges, cut_vertices = find_bridges_and_cut_vertices(graph)
    
    output = [
        "Bridges:",
        str(bridges),
        "Cut vertices:",
        str(cut_vertices)
    ]
    
    return '\n'.join(output)

"""
8.  Поиск мостов и шарниров в графе за линейное (по количеству рёбер) время.
"""
def task8(answer_basename: str,
        task_basename: str,
        type_of_graph: GraphType,
        number_of_tasks: int
        ):
    for i in range(1, number_of_tasks + 1):
        # Форматируем номер файла с ведущими нулями
        file_number = f"{i:03}"  # Преобразуем номер в строку с ведущими нулями
        ans_file_name = f"graph-tests\\task8\\{answer_basename}_{file_number}.txt"
        task_file_name = f"graph-tests\\task8\\{task_basename}_{file_number}.txt"
        g = Graph(task_file_name, 
                  type_of_graph)
        with open(ans_file_name, 'r', encoding='utf-8') as ans_file:
            file_content = ans_file.read()
            result = print_bridges_and_cut_vertices(g)
            print('\nOutput:\n' + result)
            print('\nAnswer:\n' + file_content)
            print(f'Task{i} is {"Succesfull" if file_content == (result) else "Wrong"}')


if __name__ == '__main__':
    task8(
        answer_basename='ans_t8',
        task_basename='list_of_adjacency_t8',
        type_of_graph=GraphType.LIST_OF_ADJACENCY,
        number_of_tasks=16
    )