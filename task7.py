from utils.graph import Graph, GraphType

from typing import List, Set
from collections import defaultdict

def kosaraju_scc(graph: Graph) -> List[Set[int]]:
    if not graph.is_directed():
        raise ValueError("Алгоритм требует ориентированного графа")
    
    # Первый проход DFS
    visited = set()
    order = []
    
    def dfs(u):
        stack = [(u, False)]
        while stack:
            v, processed = stack.pop()
            if processed:
                order.append(v)
                continue
            if v in visited:
                continue
            visited.add(v)
            stack.append((v, True))
            for neighbor in graph._adjacency_list.get(v, []):
                if neighbor not in visited:
                    stack.append((neighbor, False))
    
    for u in range(1, graph._num_vertices + 1):
        if u not in visited:
            dfs(u)
    
    # Транспонируем граф
    transposed = defaultdict(list)
    for u in graph._adjacency_list:
        for v in graph._adjacency_list[u]:
            transposed[v].append(u)
    
    # Второй проход DFS
    visited = set()
    components = []
    
    for u in reversed(order):
        if u not in visited:
            stack = [u]
            visited.add(u)
            component = set()
            while stack:
                v = stack.pop()
                component.add(v)
                for neighbor in transposed.get(v, []):
                    if neighbor not in visited:
                        visited.add(neighbor)
                        stack.append(neighbor)
            components.append(component)
    
    return components

def print_scc_results(graph: Graph) -> str:
    if not graph.is_directed():
        return "Graph is not directed (algorithm requires digraph)"
    
    components = kosaraju_scc(graph)
    output = []
    
    if len(components) == 1:
        output.append("Digraph is strongly connected")
    else:
        output.append("Digraph is not strongly connected")
    
    output.append("\nStrongly connected components:")
    for component in sorted(components, key=lambda x: min(x)):
        output.append(f"{sorted(component)}")
    
    return '\n'.join(output)

"""
7.  Определить компоненты сильной связности в орграфе.
"""
def task7(answer_basename: str,
        task_basename: str,
        type_of_graph: GraphType,
        number_of_tasks: int
        ):
    for i in range(1, number_of_tasks + 1):
        # Форматируем номер файла с ведущими нулями
        file_number = f"{i:03}"  # Преобразуем номер в строку с ведущими нулями
        ans_file_name = f"graph-tests\\task7\\{answer_basename}_{file_number}.txt"
        task_file_name = f"graph-tests\\task7\\{task_basename}_{file_number}.txt"
        g = Graph(task_file_name, 
                  type_of_graph)
        with open(ans_file_name, 'r', encoding='utf-8') as ans_file:
            file_content = ans_file.read()
            result = print_scc_results(g)
            print('\nOutput:\n' + result)
            print('\nAnswer:\n' + file_content)
            print(f'Task{i} is {"Succesfull" if file_content == (result) else "Wrong"}')


if __name__ == '__main__':
    task7(
        answer_basename='ans_t7',
        task_basename='list_of_edges_t7',
        type_of_graph=GraphType.LIST_OF_EDGES,
        number_of_tasks=1
    )