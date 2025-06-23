from typing import List, Tuple, Optional
import os


class Graph:
    """
    Класс для работы с графами и орграфами.
    Поддерживает два типа внутреннего представления: матрица смежности и списки смежности.
    """
    
    def __init__(self, file_path: str, file_type: str):
        """
        Конструктор класса.
        
        Args:
            file_path: путь к файлу с данными графа
            file_type: тип файла ('matrix', 'adjacency_list', 'edges')
        """
        self._vertices_count = 0
        self._adjacency_matrix = []
        self._adjacency_lists = []
        self._is_directed = False
        self._file_type = file_type
        
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Файл {file_path} не найден")
        
        self._load_from_file(file_path, file_type)
    
    def _load_from_file(self, file_path: str, file_type: str):
        """Загружает граф из файла в зависимости от типа файла."""
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        
        if not lines:
            raise ValueError("Файл пуст")
        
        # Первая строка содержит количество вершин
        try:
            self._vertices_count = int(lines[0].strip())
        except ValueError:
            raise ValueError("Первая строка должна содержать количество вершин")
        
        if file_type == 'matrix':
            self._load_matrix(lines[1:])
        elif file_type == 'adjacency_list':
            self._load_adjacency_list(lines[1:])
        elif file_type == 'edges':
            self._load_edges(lines[1:])
        else:
            raise ValueError(f"Неизвестный тип файла: {file_type}")
    
    def _load_matrix(self, lines: List[str]):
        """Загружает граф из матрицы смежности."""
        self._adjacency_matrix = []
        for line in lines:
            if line.strip():
                row = [int(x) for x in line.strip().split()]
                if len(row) != self._vertices_count:
                    raise ValueError("Количество элементов в строке не соответствует количеству вершин")
                self._adjacency_matrix.append(row)
        
        if len(self._adjacency_matrix) != self._vertices_count:
            raise ValueError("Количество строк не соответствует количеству вершин")
        
        # Определяем, является ли граф ориентированным
        self._is_directed = not self._is_symmetric()
        
        # Создаем списки смежности
        self._create_adjacency_lists()
    
    def _load_adjacency_list(self, lines: List[str]):
        """Загружает граф из списков смежности."""
        self._adjacency_lists = [[] for _ in range(self._vertices_count)]
        
        for i, line in enumerate(lines):
            if i >= self._vertices_count:
                break
            if line.strip():
                # Парсим строку вида "2 5" или "2:1 5:3"
                parts = line.strip().split()
                for part in parts:
                    if ':' in part:
                        # Формат "вершина:вес"
                        vertex, weight = part.split(':')
                        self._adjacency_lists[i].append((int(vertex), int(weight)))
                    else:
                        # Формат "вершина" (вес по умолчанию 1)
                        self._adjacency_lists[i].append((int(part), 1))
        
        # Создаем матрицу смежности
        self._create_adjacency_matrix()
        
        # Определяем, является ли граф ориентированным
        self._is_directed = not self._is_symmetric()
    
    def _load_edges(self, lines: List[str]):
        """Загружает граф из списка рёбер."""
        edges = []
        for line in lines:
            if line.strip():
                parts = line.strip().split()
                if len(parts) >= 2:
                    from_vertex = int(parts[0]) - 1  # Переводим в 0-индексацию
                    to_vertex = int(parts[1]) - 1
                    weight = int(parts[2]) if len(parts) > 2 else 1
                    edges.append((from_vertex, to_vertex, weight))
        
        # Создаем матрицу смежности
        self._adjacency_matrix = [[0] * self._vertices_count for _ in range(self._vertices_count)]
        for from_v, to_v, weight in edges:
            self._adjacency_matrix[from_v][to_v] = weight
        
        # Определяем, является ли граф ориентированным
        self._is_directed = not self._is_symmetric()
        
        # Создаем списки смежности
        self._create_adjacency_lists()
    
    def _create_adjacency_matrix(self):
        """Создает матрицу смежности из списков смежности."""
        self._adjacency_matrix = [[0] * self._vertices_count for _ in range(self._vertices_count)]
        for i, adj_list in enumerate(self._adjacency_lists):
            for vertex, weight in adj_list:
                self._adjacency_matrix[i][vertex - 1] = weight  # Переводим в 0-индексацию
    
    def _create_adjacency_lists(self):
        """Создает списки смежности из матрицы смежности."""
        self._adjacency_lists = [[] for _ in range(self._vertices_count)]
        for i in range(self._vertices_count):
            for j in range(self._vertices_count):
                if self._adjacency_matrix[i][j] > 0:
                    self._adjacency_lists[i].append((j + 1, self._adjacency_matrix[i][j]))  # Переводим в 1-индексацию
    
    def _is_symmetric(self) -> bool:
        """Проверяет, является ли матрица смежности симметричной."""
        for i in range(self._vertices_count):
            for j in range(i + 1, self._vertices_count):
                if self._adjacency_matrix[i][j] != self._adjacency_matrix[j][i]:
                    return False
        return True
    
    def size(self) -> int:
        """Возвращает количество вершин в графе/орграфе."""
        return self._vertices_count
    
    def weight(self, vertex1: int, vertex2: int) -> int:
        """Возвращает вес ребра/дуги между двумя вершинами."""
        if vertex1 < 1 or vertex1 > self._vertices_count or vertex2 < 1 or vertex2 > self._vertices_count:
            raise ValueError("Номер вершины должен быть в диапазоне [1, size]")
        return self._adjacency_matrix[vertex1 - 1][vertex2 - 1]
    
    def is_edge(self, vertex1: int, vertex2: int) -> bool:
        """Проверяет наличие ребра/дуги между двумя вершинами."""
        return self.weight(vertex1, vertex2) > 0
    
    def adjacency_matrix(self) -> List[List[int]]:
        """Возвращает матрицу смежности графа/орграфа."""
        return [row[:] for row in self._adjacency_matrix]
    
    def adjacency_list(self, vertex: int) -> List[int]:
        """Возвращает список смежных вершин для данной вершины."""
        if vertex < 1 or vertex > self._vertices_count:
            raise ValueError("Номер вершины должен быть в диапазоне [1, size]")
        return [v for v, _ in self._adjacency_lists[vertex - 1]]
    
    def list_of_edges(self, vertex: Optional[int] = None) -> List[Tuple[int, int, int]]:
        """Возвращает список рёбер графа."""
        if vertex is None:
            # Возвращаем все рёбра
            edges = []
            for i in range(self._vertices_count):
                for j in range(self._vertices_count):
                    if self._adjacency_matrix[i][j] > 0:
                        edges.append((i + 1, j + 1, self._adjacency_matrix[i][j]))
            return edges
        else:
            # Возвращаем рёбра, инцидентные данной вершине
            if vertex < 1 or vertex > self._vertices_count:
                raise ValueError("Номер вершины должен быть в диапазоне [1, size]")
            return [(vertex, v, w) for v, w in self._adjacency_lists[vertex - 1]]
    
    def is_directed(self) -> bool:
        """Возвращает True, если граф ориентированный, False, если простой."""
        return self._is_directed 