from utils.graph import Graph, GraphType
from algorithms.DFS import get_dfs_spanning_tree
from algorithms.BFS import get_bfs_spanning_tree

""""
3.  Построение остовного дерева графа: DFS или BFS.
"""
def task3(answer_basename: str,
            task_basename: str,
            type_of_graph: GraphType,
            number_of_tasks: int
            ):
    for i in range(1, number_of_tasks + 1):
        # Форматируем номер файла с ведущими нулями
        file_number = f"{i:03}"  # Преобразуем номер в строку с ведущими нулями
        ans_file_name = f"graph-tests\\task3\\{answer_basename}_{file_number}.txt"
        task_file_name = f"graph-tests\\task3\\{task_basename}_{file_number}.txt"
        g = Graph(task_file_name, 
                  type_of_graph)
        with open(ans_file_name, 'r', encoding='utf-8') as ans_file:
            file_content = ans_file.read()
            result = get_dfs_spanning_tree(g)
            print('\nOutput:\n' + result)
            print('\nAnswer:' + file_content)


if __name__ == '__main__':
    task3(
        answer_basename='ans_t3',
        task_basename='list_of_adjacency_t3',
        type_of_graph = GraphType.LIST_OF_ADJACENCY,
        number_of_tasks=1
    )