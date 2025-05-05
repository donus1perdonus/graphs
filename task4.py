from utils.graph import Graph, GraphType
from algorithms.floyd_warshall import floyd_warshall

"""
4.  Алгоритм Флойда-Уоршелла: 
a)  вектор степеней вершин, 
b)  эксцентриситеты, 
c)  диаметр, множество периферийных вершин, 
d)  радиус, множество центральных вершин.
"""
def task4(answer_basename: str,
            task_basename: str,
            type_of_graph: GraphType,
            number_of_tasks: int
            ):
    def print_graph_analysis(graph: Graph) -> str:
        _, degrees, eccentricity, diameter, peripheral, radius, central = floyd_warshall(graph)
        
        output = [
            "Vertices degrees:",
            str(degrees),
            "Eccentricity:",
            str(eccentricity),
            f"R = {radius}",
            f"Central vertices:",
            str(central),
            f"D = {diameter}",
            f"Peripherial vertices:",
            str(peripheral)
        ]
        
        return '\n'.join(output)
    for i in range(1, number_of_tasks + 1):
        # Форматируем номер файла с ведущими нулями
        file_number = f"{i:03}"  # Преобразуем номер в строку с ведущими нулями
        ans_file_name = f"graph-tests\\task4\\{answer_basename}_{file_number}.txt"
        task_file_name = f"graph-tests\\task4\\{task_basename}_{file_number}.txt"
        g = Graph(task_file_name, 
                  type_of_graph)
        with open(ans_file_name, 'r', encoding='utf-8') as ans_file:
            file_content = ans_file.read()
            result = print_graph_analysis(g)
            # print('\nOutput:\n' + result)
            # print('\nAnswer:\n' + file_content)
            print(f'Task{i} is {"Succesfull" if file_content == (result + '\n') else "Wrong"}')


if __name__ == '__main__':
    task4(
        answer_basename='ans_t4',
        task_basename='list_of_adjacency_t4',
        type_of_graph = GraphType.LIST_OF_ADJACENCY,
        number_of_tasks=14
    )