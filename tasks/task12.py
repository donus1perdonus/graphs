from utils import Map
import heapq
import math
import re

def heuristic(a, b, type='manhattan'):
    if type == 'manhattan':
        return abs(a[0] - b[0]) + abs(a[1] - b[1])
    elif type == 'chebyshev':
        return max(abs(a[0] - b[0]), abs(a[1] - b[1]))
    elif type == 'euclidean':
        return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)
    else:
        raise ValueError('Unknown heuristic type')

def astar_search(map_obj: Map, start, goal, heuristic_type='manhattan'):
    rows, cols = map_obj.size()
    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal, heuristic_type)}
    while open_set:
        _, current = heapq.heappop(open_set)
        if current == goal:
            # Восстановление пути
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()
            return path, g_score[goal]
        for neighbor in map_obj.neighbors(*current):
            step_cost = abs(neighbor[0] - current[0]) + abs(neighbor[1] - current[1]) + abs(map_obj[neighbor[0], neighbor[1]] - map_obj[current[0], current[1]])
            tentative_g = g_score[current] + step_cost
            if neighbor not in g_score or tentative_g < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score[neighbor] = tentative_g + heuristic(neighbor, goal, heuristic_type)
                heapq.heappush(open_set, (f_score[neighbor], neighbor))
    return [], 0

def parse_points_from_answer(answer_file: str):
    with open(answer_file, 'r', encoding='utf-8') as f:
        first_line = f.readline()
    m = re.match(r"(\d+) - length of path between \((\d+), (\d+)\) and \((\d+), (\d+)\) points\.", first_line)
    if not m:
        raise ValueError("Не удалось распарсить координаты из файла-ответа")
    start = (int(m.group(2)), int(m.group(3)))
    goal = (int(m.group(4)), int(m.group(5)))
    return start, goal

def solve_task(map_file, answer_file, heuristic_type='manhattan'):
    map_obj = Map(map_file)
    start, goal = parse_points_from_answer(answer_file)
    path, length = astar_search(map_obj, start, goal, heuristic_type)
    # Формируем вывод строго по эталону
    result = f"{length} - length of path between {start} and {goal} points.\n"
    result += "Path:\n"
    result += str(path)
    return result 