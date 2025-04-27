from typing import List, Tuple, Union, Dict
from enum import Enum

class GraphType(Enum):
    LIST_OF_EDGES = 1
    LIST_OF_ADJACENCY = 2
    MATRIX_OF_ADJACENCY = 3
class Graph:
    def __init__(self, file_path: str, file_type: int):
        """
        Конструктор класса Graph.
        
        :param file_path: путь к файлу с описанием графа
        :param file_type: тип файла (1 - список рёбер, 2 - списки смежности, 3 - матрица смежности)
        """
        self._adjacency_matrix = None  # type: List[List[Union[int, float]]]
        self._adjacency_list = None    # type: Dict[int, List[Tuple[int, Union[int, float]]]]
        self._is_directed = False      # ориентированный ли граф
        self._num_vertices = 0         # количество вершин
        
        with open(file_path, 'r') as file:
            lines = [line.strip() for line in file if line.strip()]
            self._num_vertices = int(lines[0])
            
            if file_type == GraphType.LIST_OF_EDGES:  # список рёбер
                self._parse_edge_list(lines[1:])
            elif file_type == GraphType.LIST_OF_ADJACENCY:  # списки смежности
                self._parse_adjacency_list(lines[1:])
            elif file_type == GraphType.MATRIX_OF_ADJACENCY:  # матрица смежности
                self._parse_adjacency_matrix(lines[1:])
            else:
                raise ValueError("Неверный тип файла. Допустимые значения: 1, 2, 3.")
    
    def _parse_edge_list(self, lines: List[str]):
        """Парсинг графа из списка рёбер."""
        self._adjacency_list = {v: [] for v in range(1, self._num_vertices + 1)}
        edge_set = set()  # для проверки дубликатов (если граф неориентированный)
        
        for line in lines:
            if not line:
                continue
            parts = line.split()
            if len(parts) == 2:  # если вес не указан, считаем вес = 1
                u, v = map(int, parts)
                weight = 1
            else:
                u, v, weight = map(int, parts)
            
            # Проверяем, не было ли уже такого ребра (для неориентированного графа)
            if (u, v) not in edge_set and (v, u) not in edge_set:
                self._adjacency_list[u].append((v, weight))
                if not self._is_directed and u != v:
                    self._adjacency_list[v].append((u, weight))
                edge_set.add((u, v))
            else:
                # Если ребро уже есть, возможно, это ориентированный граф
                self._is_directed = True
                self._adjacency_list[u].append((v, weight))
    
    def _parse_adjacency_list(self, lines: List[str]):
        """Парсинг графа из списков смежности."""
        self._adjacency_list = {v: [] for v in range(1, self._num_vertices + 1)}
        
        for i in range(len(lines)):
            vertex = i + 1
            edges = lines[i].split()
            for edge in edges:
                if ':' in edge:  # формат "вершина:вес"
                    v, weight = map(int, edge.split(':'))
                else:  # если вес не указан, считаем вес = 1
                    v = int(edge)
                    weight = 1
                self._adjacency_list[vertex].append((v, weight))
                
                # Проверяем, не ориентированный ли граф
                if not self._is_directed and v != vertex:
                    if (v, vertex) not in [(x, w) for x, w in self._adjacency_list[v]]:
                        self._adjacency_list[v].append((vertex, weight))
                    else:
                        self._is_directed = True

    def _parse_adjacency_matrix(self, lines: List[str]):
        """Парсинг графа из матрицы смежности."""
        self._adjacency_matrix = []
        
        for line in lines:
            row = list(map(int, line.split()))
            self._adjacency_matrix.append(row)
        
        # Проверяем, ориентированный ли граф
        for i in range(self._num_vertices):
            for j in range(self._num_vertices):
                if self._adjacency_matrix[i][j] != self._adjacency_matrix[j][i]:
                    self._is_directed = True
                    break
            if self._is_directed:
                break
    
    def size(self) -> int:
        """Возвращает количество вершин в графе."""
        return self._num_vertices
    
    def weight(self, u: int, v: int) -> Union[int, float]:
        """Возвращает вес ребра между вершинами u и v."""
        if self._adjacency_matrix:
            return self._adjacency_matrix[u - 1][v - 1]
        elif self._adjacency_list:
            for neighbor, weight in self._adjacency_list[u]:
                if neighbor == v:
                    return weight
        return 0  # если ребра нет
    
    def is_edge(self, u: int, v: int) -> bool:
        """Проверяет, существует ли ребро между u и v."""
        if self._adjacency_matrix:
            return self._adjacency_matrix[u - 1][v - 1] != 0
        elif self._adjacency_list:
            return any(neighbor == v for neighbor, _ in self._adjacency_list[u])
        return False
    
    def adjacency_matrix(self) -> List[List[Union[int, float]]]:
        """Возвращает матрицу смежности графа."""
        if not self._adjacency_matrix:
            self._adjacency_matrix = [[0] * self._num_vertices for _ in range(self._num_vertices)]
            for u in self._adjacency_list:
                for v, weight in self._adjacency_list[u]:
                    self._adjacency_matrix[u - 1][v - 1] = weight
        return self._adjacency_matrix
    
    def adjacency_list(self, u: int) -> List[int]:
        """Возвращает список смежных вершин для вершины u."""
        if not self._adjacency_list:
            self._adjacency_list = {v: [] for v in range(1, self._num_vertices + 1)}
            for i in range(self._num_vertices):
                for j in range(self._num_vertices):
                    if self._adjacency_matrix[i][j] != 0:
                        self._adjacency_list[i + 1].append((j + 1, self._adjacency_matrix[i][j]))
        return [neighbor for neighbor, _ in self._adjacency_list[u]]
    
    def list_of_edges(self, u: int = None) -> List[Tuple[int, int, Union[int, float]]]:
        """
        Возвращает список рёбер графа.
        Если указана вершина u, возвращает только инцидентные ей рёбра.
        """
        edges = []
        if self._adjacency_list:
            if u is None:
                for vertex in self._adjacency_list:
                    for neighbor, weight in self._adjacency_list[vertex]:
                        if not self._is_directed and neighbor < vertex:
                            continue  # чтобы не дублировать рёбра в неориентированном графе
                        edges.append((vertex, neighbor, weight))
            else:
                for neighbor, weight in self._adjacency_list[u]:
                    edges.append((u, neighbor, weight))
        elif self._adjacency_matrix:
            if u is None:
                for i in range(self._num_vertices):
                    for j in range(self._num_vertices):
                        if self._adjacency_matrix[i][j] != 0:
                            if not self._is_directed and j < i:
                                continue
                            edges.append((i + 1, j + 1, self._adjacency_matrix[i][j]))
            else:
                for j in range(self._num_vertices):
                    if self._adjacency_matrix[u - 1][j] != 0:
                        edges.append((u, j + 1, self._adjacency_matrix[u - 1][j]))
        return edges
    
    def is_directed(self) -> bool:
        """Возвращает True, если граф ориентированный."""
        return self._is_directed