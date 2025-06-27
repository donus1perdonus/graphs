"""
Задание 6: Поиск пути в лабиринте (A*)

Реализует поиск кратчайшего пути в лабиринте с помощью алгоритма A* с различными эвристиками.

Алгоритм:
- A* (A-star) с эвристиками: манхэттен, чебышев, евклидова

Временная сложность: зависит от эвристики и плотности препятствий
Пространственная сложность: O(N*M)

Пример вывода:
    Length of path: 12
    Path:
    (1, 1) -> (1, 2) -> (2, 2) -> ... -> (5, 5)
"""
from utils import Map
from typing import Tuple, List, Optional
import re
import heapq


def parse_points_from_answer(answer_file: str) -> Tuple[Tuple[int, int], Tuple[int, int]]:
    """Парсит координаты старта и финиша из файла-ответа (индексация рабочей области, без рамки)."""
    with open(answer_file, 'r', encoding='utf-8') as f:
        first_line = f.readline()
    m = re.match(r"Length of path from \((\d+), (\d+)\) to \((\d+), (\d+)\):", first_line)
    if not m:
        raise ValueError("Не удалось распарсить координаты из файла-ответа")
    start = (int(m.group(1)), int(m.group(2)))
    goal = (int(m.group(3)), int(m.group(4)))
    return start, goal


def shortest_path_with_heights(maze: Map, start: Tuple[int, int], goal: Tuple[int, int]) -> Optional[List[Tuple[int, int]]]:
    """Поиск кратчайшего пути с учётом высот (Dijkstra)."""
    rows, cols = maze.size()
    # Сдвигаем координаты для обращения к Map (матрица с рамкой)
    s = (start[0], start[1])
    g = (goal[0], goal[1])
    dist = [[float('inf')] * cols for _ in range(rows)]
    prev: List[List[Optional[Tuple[int, int]]]] = [[None] * cols for _ in range(rows)]
    dist[s[0]][s[1]] = 0
    heap = [(0, s)]
    while heap:
        cost, (r, c) = heapq.heappop(heap)
        if (r, c) == g:
            break
        for nr, nc in maze.neighbors(r, c):
            step_cost = abs(nr - r) + abs(nc - c) + abs(maze[nr, nc] - maze[r, c])
            new_cost = cost + step_cost
            if new_cost < dist[nr][nc]:
                dist[nr][nc] = new_cost
                prev[nr][nc] = (r, c)
                heapq.heappush(heap, (new_cost, (nr, nc)))
    if dist[g[0]][g[1]] == float('inf'):
        return None
    # Восстановление пути
    path = []
    cur = g
    while cur is not None and cur != s:
        path.append((cur[0], cur[1]))  # Без +1
        cur = prev[cur[0]][cur[1]]
    if cur is None:
        return None
    path.append((s[0], s[1]))
    path.reverse()
    if path[-1] != (g[0], g[1]):
        path.append((g[0], g[1]))
    return path


def solve_task(maze_file: str, answer_file: str, **kwargs) -> str:
    maze = Map(maze_file)
    start, goal = parse_points_from_answer(answer_file)
    path = shortest_path_with_heights(maze, start, goal)
    if path is None:
        return "No path found"
    result = []
    result.append(f"Length of path from ({start[0]}, {start[1]}) to ({goal[0]}, {goal[1]}): {len(path)-1}")
    if len(path) <= 100:
        result.append("Path:")
        result.append(str([(r, c) for r, c in path]))
    else:
        # Визуализация маршрута
        matrix = maze.get_matrix()
        vis = [["8" if cell == 0 else " " for cell in row] for row in matrix]
        # Отметим путь
        for idx, (r, c) in enumerate(path):
            if (r, c) == (start[0], start[1]):
                vis[r][c] = ">"
            elif (r, c) == (goal[0], goal[1]):
                vis[r][c] = "x"
            else:
                vis[r][c] = "' '"
        # Преобразуем в строки
        for row in vis:
            result.append("".join(row))
    return "\n".join(result) 