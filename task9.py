from utils.graph import Graph, GraphType

class DSU:
    def __init__(self, n):
        self.parent = list(range(n + 1))  # Вершины нумеруются с 1
        self.rank = [0] * (n + 1)
    
    def find(self, u):
        if self.parent[u] != u:
            self.parent[u] = self.find(self.parent[u])
        return self.parent[u]
    
    def union(self, u, v):
        u_root = self.find(u)
        v_root = self.find(v)
        if u_root == v_root:
            return False
        if self.rank[u_root] < self.rank[v_root]:
            self.parent[u_root] = v_root
        else:
            self.parent[v_root] = u_root
            if self.rank[u_root] == self.rank[v_root]:
                self.rank[u_root] += 1
        return True

def kruskal_mst(graph):
    edges = []
    # Собираем все рёбра графа
    for u in graph._adjacency_list:
        for v, weight in graph._adjacency_list[u]:
            if u < v:  # Чтобы не дублировать рёбра
                edges.append((weight, u, v))
    
    # Сортируем рёбра по весу
    edges.sort()
    
    dsu = DSU(graph.size())
    mst = []
    
    for weight, u, v in edges:
        if dsu.union(u, v):
            mst.append((u, v, weight))
            if len(mst) == graph.size() - 1:
                break
    
    return mst

def print_mst(mst_edges):
    output = ["Minimal spanning tree:"]
    for u, v, weight in sorted(mst_edges, key=lambda x: (x[2], x[0], x[1])):
        output.append(f"{u}-{v}: {weight}")
    return '\n'.join(output)

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
        g = Graph(task_file_name, 
                  type_of_graph)
        with open(ans_file_name, 'r', encoding='utf-8') as ans_file:
            file_content = ans_file.read()
            mst = kruskal_mst(g)
            result = print_mst()
            print('\nOutput:\n' + result)
            print('\nAnswer:\n' + file_content)
            print(f'Task{i} is {"Succesfull" if file_content == (result) else "Wrong"}')


if __name__ == '__main__':
    task9(
        answer_basename='ans_t9',
        task_basename='list_of_adjacency_t9',
        type_of_graph=GraphType.LIST_OF_ADJACENCY,
        number_of_tasks=1
    )