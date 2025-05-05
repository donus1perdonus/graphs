from typing import List

from utils.graph import Graph, GraphType
from algorithms.BFS import find_weakly_connected_components_bfs, find_connected_components_bfs, get_bfs_spanning_tree
from algorithms.DFS import find_weakly_connected_components_dfs, find_connected_components_dfs, get_dfs_spanning_tree

"""
1.  Алгоритм: DFS/BFS: поиск компонент связности графа и слабой связности в орграфе.
"""
def task1(answer_basename: str,
            task_basename: str,
            type_of_graph: GraphType,
            number_of_tasks: int
            ):
    def get_components_string(components: List[List[int]], g: Graph) -> str:
        result = []
        if len(components) == 1:
            result.append(f"{'Diraph' if g.is_directed() else 'Graph'} is connected")
        else:
            result.append(f"{'Diraph' if g.is_directed() else 'Graph'} is not connected")
        
        result.append("\nConnected components:")
        
        # Сортируем вершины внутри каждой компоненты
        components_sorted = [sorted(comp) for comp in components]
        # Сортируем сами компоненты по первому элементу, чтобы одиночные вершины шли первыми
        components_sorted.sort(key=lambda x: (len(x), x[0]))
        
        for component in components_sorted:
            result.append(str(component))
        
        return '\n'.join(result)

    for i in range(1, number_of_tasks + 1):
        # Форматируем номер файла с ведущими нулями
        file_number = f"{i:03}"  # Преобразуем номер в строку с ведущими нулями
        ans_file_name = f"graph-tests\\task1\\{answer_basename}_{file_number}.txt"
        task_file_name = f"graph-tests\\task1\\{task_basename}_{file_number}.txt"
        g = Graph(task_file_name, 
                  type_of_graph)
        with open(ans_file_name, 'r', encoding='utf-8') as ans_file:
            file_content = ans_file.read()
            components = find_connected_components_bfs(g)
            result = get_components_string(components, g)
            # print(file_content)
            # print(result)
            print(f'Task{i} is {"Succesfull" if file_content == result else "Wrong"}')
   

if __name__ == '__main__':
    task1(
        answer_basename='ans_t1', 
        task_basename='matrix_t1',
        type_of_graph = GraphType.MATRIX_OF_ADJACENCY,
        number_of_tasks=50
    )