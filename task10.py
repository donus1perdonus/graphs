from utils.graph import WeightedGraph, GraphType

class FloydWarshall:
    def __init__(self, graph):
        self.n = graph.size()
        self.graph = graph  # Сохраняем исходный граф
        self.adj_matrix = [[float('inf')] * (self.n + 1) for _ in range(self.n + 1)]
        self.next_node = [[-1] * (self.n + 1) for _ in range(self.n + 1)]
        
        # Инициализация матрицы расстояний
        for u in range(1, self.n + 1):
            self.adj_matrix[u][u] = 0
            for v, weight in graph.adjacency_list(u).items():
                self.adj_matrix[u][v] = weight
                self.next_node[u][v] = v
        
        # Алгоритм Флойда-Уоршелла
        for k in range(1, self.n + 1):
            for i in range(1, self.n + 1):
                for j in range(1, self.n + 1):
                    if self.adj_matrix[i][j] > self.adj_matrix[i][k] + self.adj_matrix[k][j]:
                        self.adj_matrix[i][j] = self.adj_matrix[i][k] + self.adj_matrix[k][j]
                        self.next_node[i][j] = self.next_node[i][k]

    def get_path(self, u, v):
        if self.next_node[u][v] == -1:
            return []
        path = [u]
        while u != v:
            u = self.next_node[u][v]
            path.append(u)
        return path

    def analyze_components(self):
        # Степени вершин (только непосредственные соседи)
        degrees = [0] * (self.n + 1)
        for u in range(1, self.n + 1):
            degrees[u] = len(self.graph.adjacency_list(u))
        
        # Эксцентриситеты вершин
        eccentricity = [0.0] * (self.n + 1)
        for u in range(1, self.n + 1):
            max_dist = 0.0
            for v in range(1, self.n + 1):
                if u != v and self.adj_matrix[u][v] < float('inf'):
                    max_dist = max(max_dist, self.adj_matrix[u][v])
            eccentricity[u] = max_dist if max_dist != 0 else float('inf')
        
        # Радиус и центральные вершины
        radius = min(eccentricity[1:self.n + 1])
        central_verts = [u for u in range(1, self.n + 1) if eccentricity[u] == radius]
        
        # Диаметр и периферийные вершины
        diameter = max(eccentricity[1:self.n + 1])
        peripherial_verts = [u for u in range(1, self.n + 1) if eccentricity[u] == diameter]
        
        return {
            'degrees': degrees[1:],
            'eccentricity': eccentricity[1:],
            'radius': radius,
            'central_vertices': central_verts,
            'diameter': diameter,
            'peripherial_vertices': peripherial_verts
        }

def format_analysis_result(analysis):
    lines = [
        "Vertices degrees:",
        str(analysis['degrees']),
        "Eccentricity:",
        str([float(x) if x != float('inf') else x for x in analysis['eccentricity']]),
        f"R = {float(analysis['radius'])}",
        "Central vertices:",
        str(analysis['central_vertices']),
        f"D = {float(analysis['diameter'])}",
        "Peripherial vertices:",
        str(analysis['peripherial_vertices'])
    ]
    return '\n'.join(lines)

"""
10. Алгоритм Флойда-Уоршелла: 
a)  восстановление пути для выбранной пары вершин, 
b)  характеристики каждой компоненты связности графа.
"""
def task10(answer_basename: str,
        task_basename: str,
        type_of_graph: GraphType,
        number_of_tasks: int
        ):
    for i in range(1, number_of_tasks + 1):
        # Форматируем номер файла с ведущими нулями
        file_number = f"{i:03}"  # Преобразуем номер в строку с ведущими нулями
        ans_file_name = f"graph-tests\\task10\\{answer_basename}_{file_number}.txt"
        task_file_name = f"graph-tests\\task10\\{task_basename}_{file_number}.txt"
        g = WeightedGraph(task_file_name, 
                  type_of_graph)
        with open(ans_file_name, 'r', encoding='utf-8') as ans_file:
            file_content = ans_file.read()
            fw = FloydWarshall(g)
            # Анализируем компоненты связности
            analysis = fw.analyze_components()
            # Форматируем результат
            result = format_analysis_result(analysis)
            # print('\nOutput:\n' + result)
            # print('\nAnswer:\n' + file_content)
            print(f'Task{i} is {"Succesfull" if file_content == (result) else "Wrong"}')


if __name__ == '__main__':
    task10(
        answer_basename='ans_t10',
        task_basename='list_of_adjacency_t10',
        type_of_graph=GraphType.LIST_OF_ADJACENCY,
        number_of_tasks=18
    )