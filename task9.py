from utils.graph import WeightedGraph, GraphType

import heapq

def find_min_spanning_tree(graph: WeightedGraph):
    if graph.is_directed():
        ValueError("Граф не должен быть ориентированным для поиска MST")
        return None
    
    num_vertices = graph.size()
    if num_vertices == 0:
        return []
    
    # Начинаем с вершины 1 (можно выбрать любую)
    start_vertex = 1
    mst_edges = []
    visited = set([start_vertex])
    edges = []
    
    # Добавляем все рёбра из начальной вершины в кучу
    for neighbor, weight in graph.adjacency_list(start_vertex).items():
        heapq.heappush(edges, (weight, start_vertex, neighbor))
    
    while edges and len(visited) < num_vertices:
        weight, u, v = heapq.heappop(edges)
        if v not in visited:
            visited.add(v)
            mst_edges.append((u, v, weight))
            # Добавляем все рёбра из новой вершины в кучу
            for neighbor, new_weight in graph.adjacency_list(v).items():
                if neighbor not in visited:
                    heapq.heappush(edges, (new_weight, v, neighbor))
    
    if len(visited) != num_vertices:
        raise ValueError("Граф несвязный, невозможно построить MST")
    
    return mst_edges

def format_mst(mst_edges) -> str:
    if mst_edges is None:
        return 'Graph is not connected'
    lines = ["Minimal spanning tree:"]
    for edge in sorted(mst_edges, key=lambda x: (x[1], x[0])):
        lines.append(f"{edge[0]}-{edge[1]}: {edge[2]}")
    return '\n'.join(lines)

"""
9.  Поиск минимального остовного дерева.
"""
def task9(answer_basename: str,
        task_basename: str,
        type_of_graph: GraphType,
        number_of_tasks: int
        ):
    for i in range(1, number_of_tasks + 1):
        # Форматируем номер файла с ведущими нулями
        file_number = f"{i:03}"  # Преобразуем номер в строку с ведущими нулями
        ans_file_name = f"graph-tests\\task9\\{answer_basename}_{file_number}.txt"
        task_file_name = f"graph-tests\\task9\\{task_basename}_{file_number}.txt"
        g = WeightedGraph(task_file_name, 
                  type_of_graph)
        with open(ans_file_name, 'r', encoding='utf-8') as ans_file:
            file_content = ans_file.read()
            mst = find_min_spanning_tree(g)
            result = format_mst(mst)
            # print('\nOutput:\n' + result)
            # print('\nAnswer:\n' + file_content)
            print(f'Task{i} is {"Succesfull" if file_content == (result) else "Wrong"}')


if __name__ == '__main__':
    task9(
        answer_basename='ans_t9',
        task_basename='list_of_adjacency_t9',
        type_of_graph=GraphType.LIST_OF_ADJACENCY,
        number_of_tasks=14
    )