from utils.graph import WeightedGraph, GraphType
from typing import Dict

class BellmanFordMoore:
    def __init__(self, graph):
        self.graph = graph
        self.n = graph.size()
        self.all_distances = {}  # Храним расстояния от всех вершин
    
    def compute_all_paths(self):
        """Вычисляем пути из всех вершин сразу"""
        for start in range(1, self.n + 1):
            self.all_distances[start] = self._find_shortest_paths(start)
    
    def _find_shortest_paths(self, start: int) -> Dict[int, float]:
        distances = {v: float('inf') for v in range(1, self.n + 1)}
        distances[start] = 0
        
        # Релаксация рёбер
        for _ in range(self.n - 1):
            updated = False
            for u in range(1, self.n + 1):
                for v, weight in self.graph.adjacency_list(u).items():
                    if distances[u] + weight < distances[v]:
                        distances[v] = distances[u] + weight
                        updated = True
            if not updated:
                break
        
        # Проверка на отрицательные циклы
        for u in range(1, self.n + 1):
            for v, weight in self.graph.adjacency_list(u).items():
                if distances[u] + weight < distances[v]:
                    raise ValueError(f"Обнаружен отрицательный цикл, затрагивающий вершину {start}")
        
        return distances
    
    def get_paths_from(self, start: int) -> str:
        if not self.all_distances:
            self.compute_all_paths()
        return self._format_shortest_paths(start, self.all_distances[start])
    
    def _format_shortest_paths(self, start: int, distances: Dict[int, float]) -> str:
        sorted_distances = sorted(distances.items(), key=lambda x: x[0])
        distances_str = ", ".join(f"{k}: {int(v) if v != float('inf') else 'inf'}" 
                                for k, v in sorted_distances)
        return f"Shortest paths lengths from {start}:\n{{{distances_str}}}"

def task11(answer_basename: str,
           task_basename: str,
           type_of_graph: GraphType,
           number_of_tasks: int):
    for i in range(1, number_of_tasks + 1):
        # Форматируем номер файла с ведущими нулями
        file_number = f"{i:03d}"
        ans_file_name = f"graph-tests/task11/{answer_basename}_{file_number}.txt"
        task_file_name = f"graph-tests/task11/{task_basename}_{file_number}.txt"
        # Читаем граф из файла
        g = WeightedGraph(task_file_name, type_of_graph)
        
        # Определяем стартовую вершину из файла ответа
        with open(ans_file_name, 'r', encoding='utf-8') as ans_file:
            first_line = ans_file.readline().strip()
            start_vertex = int(first_line.split()[-1])
        
        # Вычисляем кратчайшие пути
        bfm = BellmanFordMoore(g)
        result = bfm.get_paths_from(start_vertex)
        
        # Сравниваем с эталоном
        with open(ans_file_name, 'r', encoding='utf-8') as ans_file:
            expected_result = ans_file.read().strip()
            
        is_correct = result.strip() == expected_result.strip()
        print(f'Task{i} is {"Successful" if is_correct else "Wrong"}')

if __name__ == '__main__':
    task11(
        answer_basename='ans_t11',
        task_basename='list_of_adjacency_t11',
        type_of_graph=GraphType.LIST_OF_ADJACENCY,
        number_of_tasks=18
    )