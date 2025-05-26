from collections import defaultdict
from typing import List, Tuple, Union, Dict
from enum import Enum

class GraphType(Enum):
    LIST_OF_EDGES = 1
    LIST_OF_ADJACENCY = 2
    MATRIX_OF_ADJACENCY = 3

class Graph:
    def __init__(self, file_path: str, file_type: GraphType):
        self._adjacency_list = defaultdict(list)
        self._num_vertices = 0
        self._is_directed = False
        
        with open(file_path, 'r') as file:
            lines = [line.strip() for line in file if line.strip()]
            self._num_vertices = int(lines[0])
            
            if file_type == GraphType.LIST_OF_EDGES:
                self._parse_edge_list(lines[1:])
            elif file_type == GraphType.LIST_OF_ADJACENCY:
                self._parse_adjacency_list(lines[1:])
            elif file_type == GraphType.MATRIX_OF_ADJACENCY:
                self._parse_adjacency_matrix(lines[1:])
            else:
                raise ValueError("Неверный тип файла")
        
        self._determine_directed()

    def _parse_edge_list(self, lines: List[str]):
        for line in lines:
            if not line:
                continue
            u, v = map(int, line.split())
            self._adjacency_list[u].append(v)

    def _parse_adjacency_list(self, lines: List[str]):
        for i in range(len(lines)):
            u = i + 1
            if not lines[i].strip():
                continue
            neighbors = list(map(int, lines[i].strip().split()))
            self._adjacency_list[u] = neighbors

    def _parse_adjacency_matrix(self, lines: List[str]):
        for i in range(len(lines)):
            u = i + 1
            row = list(map(int, lines[i].strip().split()))
            for j in range(len(row)):
                if row[j] != 0:
                    self._adjacency_list[u].append(j + 1)

    def _determine_directed(self):
        """Автоматическое определение ориентированности графа"""
        for u in self._adjacency_list:
            for v in self._adjacency_list[u]:
                if u not in self._adjacency_list.get(v, []):
                    self._is_directed = True
                    return
        self._is_directed = False

    def adjacency_list(self, u: int) -> List[int]:
        """Возвращает список смежных вершин (без весов)"""
        return self._adjacency_list.get(u, [])

    def is_directed(self) -> bool:
        return self._is_directed

    def size(self) -> int:
        return self._num_vertices
    
class WeightedGraph:
    def __init__(self, file_path: str, file_type: int):
        self._adjacency_list = defaultdict(dict)  # Храним как {u: {v: weight}}
        self._num_vertices = 0
        self._is_directed = False
        
        with open(file_path, 'r') as file:
            lines = [line.strip() for line in file if line.strip()]
            self._num_vertices = int(lines[0])
            
            if file_type == GraphType.LIST_OF_EDGES:
                self._parse_edge_list(lines[1:])
            elif file_type == GraphType.LIST_OF_ADJACENCY:
                self._parse_adjacency_list(lines[1:])
            elif file_type == GraphType.MATRIX_OF_ADJACENCY:
                self._parse_adjacency_matrix(lines[1:])
            else:
                raise ValueError("Неверный тип файла")
        
        self._determine_directed()

    def _parse_edge_list(self, lines: List[str]):
        for line in lines:
            if not line:
                continue
            parts = line.split()
            if len(parts) != 3:
                raise ValueError("Некорректный формат списка рёбер")
            u, v, weight = map(int, parts)
            self._adjacency_list[u][v] = weight
            # Для неориентированного графа добавим обратное ребро, если оно есть в данных

    def _parse_adjacency_list(self, lines: List[str]):
        for i in range(len(lines)):
            u = i + 1
            if not lines[i].strip():
                continue
            parts = lines[i].strip().split()
            for part in parts:
                if ':' not in part:
                    raise ValueError("Некорректный формат списка смежности")
                v, weight = map(int, part.split(':'))
                self._adjacency_list[u][v] = weight

    def _parse_adjacency_matrix(self, lines: List[str]):
        for i in range(len(lines)):
            u = i + 1
            row = list(map(int, lines[i].strip().split()))
            for j in range(len(row)):
                if row[j] != 0:
                    self._adjacency_list[u][j+1] = row[j]

    def _determine_directed(self):
        """Автоматическое определение ориентированности графа"""
        for u in self._adjacency_list:
            for v, weight in self._adjacency_list[u].items():
                if self._adjacency_list.get(v, {}).get(u) != weight:
                    self._is_directed = True
                    return
        self._is_directed = False

    def adjacency_list(self, u: int) -> Dict[int, int]:
        """Возвращает словарь смежных вершин и весов рёбер {v: weight}"""
        return self._adjacency_list.get(u, {})

    def is_directed(self) -> bool:
        return self._is_directed

    def size(self) -> int:
        return self._num_vertices

    def edges(self) -> List[Tuple[int, int, int]]:
        """Возвращает список всех рёбер в виде кортежей (u, v, weight)"""
        edges = []
        for u in self._adjacency_list:
            for v, weight in self._adjacency_list[u].items():
                edges.append((u, v, weight))
        return edges

    def adjacency_matrix(self) -> List[List[int]]:
        """Возвращает матрицу смежности"""
        matrix = [[0] * (self._num_vertices + 1) for _ in range(self._num_vertices + 1)]
        for u in self._adjacency_list:
            for v, weight in self._adjacency_list[u].items():
                matrix[u][v] = weight
        return matrix