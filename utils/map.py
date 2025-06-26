from typing import List, Tuple, Optional
import os


class Map:
    """
    Класс для работы с лабиринтами и картами.
    Поддерживает поиск пути между точками с различными эвристиками.
    """
    
    def __init__(self, file_path: str):
        """
        Конструктор класса.
        
        Args:
            file_path: путь к файлу с данными лабиринта/карты
        """
        self._matrix = []
        self._rows = 0
        self._cols = 0
        
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Файл {file_path} не найден")
        
        self._load_from_file(file_path)
    
    def _load_from_file(self, file_path: str):
        """Загружает лабиринт/карту из файла."""
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = [line for line in file if line.strip()]
        if not lines:
            raise ValueError("Файл пуст")
        # Попробуем считать размеры из первой строки
        try:
            self._rows, self._cols = map(int, lines[0].strip().split())
            # Старый формат: размеры заданы явно
            data_lines = lines[1:]
        except ValueError:
            # Новый формат: размеры по количеству строк и столбцов
            self._rows = len(lines)
            self._cols = len(lines[0].strip().split())
            data_lines = lines
        self._matrix = []
        for i, line in enumerate(data_lines):
            row = [int(x) for x in line.strip().split()]
            if len(row) != self._cols:
                raise ValueError(f"Количество элементов в строке {i+1} не соответствует количеству столбцов")
            self._matrix.append(row)
        if len(self._matrix) != self._rows:
            raise ValueError("Количество строк не соответствует указанному")
    
    def __getitem__(self, key: Tuple[int, int]) -> int:
        """
        Индексатор для получения значения высоты в точке.
        
        Args:
            key: кортеж (строка, столбец)
            
        Returns:
            значение высоты в точке
        """
        row, col = key
        if row < 0 or row >= self._rows or col < 0 or col >= self._cols:
            raise IndexError("Координаты выходят за границы карты")
        return self._matrix[row][col]
    
    def size(self) -> Tuple[int, int]:
        """
        Возвращает размеры карты.
        
        Returns:
            кортеж (количество строк, количество столбцов)
        """
        return self._rows, self._cols
    
    def neighbors(self, row: int, col: int) -> List[Tuple[int, int]]:
        """
        Возвращает список соседних клеток.
        
        Args:
            row: номер строки
            col: номер столбца
            
        Returns:
            список координат соседних клеток [(row, col), ...]
        """
        if row < 0 or row >= self._rows or col < 0 or col >= self._cols:
            return []
        
        neighbors = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # вверх, вниз, влево, вправо
        
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            if (0 <= new_row < self._rows and 
                0 <= new_col < self._cols and 
                self._matrix[new_row][new_col] > 0):  # проходимая клетка
                neighbors.append((new_row, new_col))
        
        return neighbors
    
    def distance(self, pos1: Tuple[int, int], pos2: Tuple[int, int]) -> int:
        """
        Вычисляет расстояние между двумя клетками.
        
        Args:
            pos1: координаты первой клетки (row, col)
            pos2: координаты второй клетки (row, col)
            
        Returns:
            расстояние между клетками
        """
        row1, col1 = pos1
        row2, col2 = pos2
        height1 = self._matrix[row1][col1]
        height2 = self._matrix[row2][col2]
        
        return abs(row2 - row1) + abs(col2 - col1) + abs(height2 - height1)
    
    def manhattan_distance(self, pos: Tuple[int, int], goal: Tuple[int, int]) -> int:
        """Манхэттенское расстояние."""
        row, col = pos
        goal_row, goal_col = goal
        return abs(goal_row - row) + abs(goal_col - col)
    
    def chebyshev_distance(self, pos: Tuple[int, int], goal: Tuple[int, int]) -> int:
        """Расстояние Чебышева."""
        row, col = pos
        goal_row, goal_col = goal
        return max(abs(goal_row - row), abs(goal_col - col))
    
    def euclidean_distance(self, pos: Tuple[int, int], goal: Tuple[int, int]) -> float:
        """Евклидово расстояние."""
        row, col = pos
        goal_row, goal_col = goal
        return ((goal_row - row) ** 2 + (goal_col - col) ** 2) ** 0.5
    
    def get_matrix(self) -> List[List[int]]:
        """Возвращает копию матрицы карты."""
        return [row[:] for row in self._matrix] 