from typing import List, Tuple
import os

from utils.graph import Graph, GraphType
from utils.map import Map, PathFinder

from algorithms.BFS import find_weakly_connected_components_bfs, find_connected_components_bfs, get_bfs_spanning_tree
from algorithms.DFS import find_weakly_connected_components_dfs, find_connected_components_dfs, get_dfs_spanning_tree
from algorithms.floyd_warshall import floyd_warshall
from algorithms.bipartite import is_bipartite

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
            

"""
2.  Поиск мостов и шарниров в графе.
"""
def task2(answer_basename: str,
            task_basename: str,
            type_of_graph: GraphType,
            number_of_tasks: int
            ):
    def find_bridges_and_articulations(graph: Graph) -> Tuple[List[Tuple[int, int]], List[int]]:
        if graph.is_directed():
            raise ValueError("Граф должен быть неориентированным")
        
        adjacency = {v: [] for v in range(1, graph.size() + 1)}
        for u in range(1, graph.size() + 1):
            for v, _ in graph._adjacency_list.get(u, []):
                adjacency[u].append(v)
        
        tin = [0] * (graph.size() + 1)
        low = [0] * (graph.size() + 1)
        visited = [False] * (graph.size() + 1)
        timer = 1
        bridges = []
        articulations = set()
        
        def dfs(u: int, parent: int = -1):
            nonlocal timer
            visited[u] = True
            tin[u] = low[u] = timer
            timer += 1
            children = 0
            
            for v in adjacency[u]:
                if v == parent:
                    continue
                if visited[v]:
                    low[u] = min(low[u], tin[v])
                else:
                    dfs(v, u)
                    low[u] = min(low[u], low[v])
                    if low[v] > tin[u]:
                        bridges.append((min(u, v), max(u, v)))  # для упорядочивания
                    if low[v] >= tin[u] and parent != -1:
                        articulations.add(u)
                    children += 1
            if parent == -1 and children > 1:
                articulations.add(u)
        
        for u in range(1, graph.size() + 1):
            if not visited[u]:
                dfs(u)
        
        bridges = sorted(list(set(bridges)))  # Убираем дубликаты и сортируем
        articulations = sorted(list(articulations))
        return bridges, articulations

    for i in range(1, number_of_tasks + 1):
        # Форматируем номер файла с ведущими нулями
        file_number = f"{i:03}"  # Преобразуем номер в строку с ведущими нулями
        ans_file_name = f"graph-tests\\task2\\{answer_basename}_{file_number}.txt"
        task_file_name = f"graph-tests\\task2\\{task_basename}_{file_number}.txt"
        g = Graph(task_file_name, 
                  type_of_graph)
        with open(ans_file_name, 'r', encoding='utf-8') as ans_file:
            file_content = ans_file.read()
            bridges, articulations = find_bridges_and_articulations(g)
            result = f'Bridges:\n {bridges}\nCut vertices:\n {articulations}\n'
            # print(file_content)
            # print(result)
            print(f'Task{i} is {"Succesfull" if file_content == result else "Wrong"}')


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


"""
6.  Найти проход в лабиринте от начальной точки до конечной.
"""
def task6(answer_basename: str,
            task_basename: str,
            number_of_tasks: int
            ):
    def process_all_mazes(maze_files: List[str]):
        for maze_file in maze_files:
            if not os.path.exists(maze_file):
                print(f"Файл {maze_file} не найден, пропускаем...")
                continue
            
            print(f"\nОбработка лабиринта: {maze_file}")
            map_obj = Map(maze_file)
            
            # Находим все пути между доступными точками
            all_paths = PathFinder.find_all_paths(map_obj)
            
            # Создаем папку для результатов
            output_dir = "maze_paths"
            os.makedirs(output_dir, exist_ok=True)
            
            # Сохраняем результаты
            base_name = os.path.splitext(os.path.basename(maze_file))[0]
            output_file = os.path.join(output_dir, f"{base_name}_paths.txt")
            
            with open(output_file, 'w') as f:
                for (start, goal), path in all_paths.items():
                    f.write(f"Path from {start} to {goal} (length {len(path)-1}):\n")
                    f.write(f"Coordinates: {path}\n")
                    f.write(f"Visualization:\n{PathFinder.visualize_path(map_obj, path)}\n")
                    f.write("\n" + "="*50 + "\n")
            
            print(f"Результаты сохранены в {output_file}")

    maze_files = [f"graph-tests\\task6\\{task_basename}_{i:03}.txt" for i in range(1, number_of_tasks + 1)]
    process_all_mazes(maze_files)


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
            # print('\nOutput:\n' + result)
            # print('\nAnswer:\n' + file_content)
            print(f'Task{i} is {"Succesfull" if file_content == (result) else "Wrong"}')


if __name__ == '__main__':
    # task1(
    #     answer_basename='ans_t1', 
    #     task_basename='matrix_t1',
    #     type_of_graph = GraphType.MATRIX_OF_ADJACENCY,
    #     number_of_tasks=1
    # )
    # task2(
    #     answer_basename='ans_t2',
    #     task_basename='list_of_adjacency_t2',
    #     type_of_graph = GraphType.LIST_OF_ADJACENCY,
    #     number_of_tasks=16
    # )
    # task3(
    #     answer_basename='ans_t3',
    #     task_basename='list_of_adjacency_t3',
    #     type_of_graph = GraphType.LIST_OF_ADJACENCY,
    #     number_of_tasks=1
    # )
    # task4(
    #     answer_basename='ans_t4',
    #     task_basename='list_of_adjacency_t4',
    #     type_of_graph = GraphType.LIST_OF_ADJACENCY,
    #     number_of_tasks=12
    # )
    # task5(
    #     answer_basename='ans_t5',
    #     task_basename='matrix_t5',
    #     type_of_graph = GraphType.MATRIX_OF_ADJACENCY,
    #     number_of_tasks=11
    # )
    # task6(
    #     answer_basename='puk',
    #     task_basename='maze_t6',
    #     number_of_tasks=1
    # )
    task7(
        answer_basename='ans_t7',
        task_basename='list_of_adjacency_t7',
        number_of_tasks=1
    )