from typing import List, Tuple

from utils.graph import Graph, GraphType

"""
2.  Поиск мостов и шарниров в графе.
"""
def task2(answer_basename: str,
            task_basename: str,
            type_of_graph: GraphType,
            number_of_tasks: int
            ):
    def find_bridges_and_articulations(graph: Graph):
        if graph.is_directed():
            raise ValueError("Граф должен быть неориентированным")
        
        adjacency = {u: graph.adjacency_list(u) for u in range(1, graph.size() + 1)}
        
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



if __name__ == '__main__':
    task2(
        answer_basename='ans_t2',
        task_basename='list_of_adjacency_t2',
        type_of_graph = GraphType.LIST_OF_ADJACENCY,
        number_of_tasks=16
    )