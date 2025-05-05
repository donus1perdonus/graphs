from utils.graph import Graph, GraphType
from algorithms.bipartite import is_bipartite

"""
5.  Определить, является ли граф двудольным, вывести состав долей. 
"""
def task5(answer_basename: str,
            task_basename: str,
            type_of_graph: GraphType,
            number_of_tasks: int
            ):
    def check_bipartite(graph: Graph) -> str:
        is_bip, parts = is_bipartite(graph)
        
        if not is_bip:
            return "Graph is not bipartite."
        else:
            part1, part2 = sorted(parts[0]), sorted(parts[1])
            output = [
                "First set:",
                "\t{" + ", ".join(map(str, part1)) + "},",
                "Second set:",
                "\t{" + ", ".join(map(str, part2)) + "}."
            ]
            return '\n'.join(output)
    for i in range(1, number_of_tasks + 1):
        # Форматируем номер файла с ведущими нулями
        file_number = f"{i:03}"  # Преобразуем номер в строку с ведущими нулями
        ans_file_name = f"graph-tests\\task5\\{answer_basename}_{file_number}.txt"
        task_file_name = f"graph-tests\\task5\\{task_basename}_{file_number}.txt"
        g = Graph(task_file_name, 
                  type_of_graph)
        with open(ans_file_name, 'r', encoding='utf-8') as ans_file:
            file_content = ans_file.read()
            result = check_bipartite(g)
            # print('\nOutput:\n' + result)
            # print('\nAnswer:\n' + file_content)
            print(f'Task{i} is {"Succesfull" if file_content == (result) else "Wrong"}')


if __name__ == '__main__':
    task5(
        answer_basename='ans_t5',
        task_basename='matrix_t5',
        type_of_graph = GraphType.MATRIX_OF_ADJACENCY,
        number_of_tasks=11
    )