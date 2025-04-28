import heapq
import math
from typing import List, Tuple, Dict, Callable, Optional

class Map:
    def __init__(self, file_path: str):
        with open(file_path, 'r') as file:
            rows, cols = map(int, file.readline().split())
            self._data = []
            for _ in range(rows):
                row = list(map(int, file.readline().split()))
                self._data.append(row)
    
    def __getitem__(self, indices: Tuple[int, int]) -> int:
        i, j = indices
        return self._data[i][j]
    
    def size(self) -> Tuple[int, int]:
        return (len(self._data), len(self._data[0]) if self._data else 0)
    
    def neighbors(self, i: int, j: int) -> List[Tuple[int, int]]:
        rows, cols = self.size()
        neighbors = []
        for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            ni, nj = i + di, j + dj
            if 0 <= ni < rows and 0 <= nj < cols and self._data[ni][nj] != 0:
                neighbors.append((ni, nj))
        return neighbors

class PathFinder:
    @staticmethod
    def manhattan_distance(ij: Tuple[int, int], sp: Tuple[int, int]) -> float:
        return abs(sp[0] - ij[0]) + abs(sp[1] - ij[1])
    
    @staticmethod
    def transition_cost(ij: Tuple[int, int], kl: Tuple[int, int], map_obj: Map) -> float:
        i, j = ij
        k, l = kl
        a_ij = map_obj[ij]
        a_kl = map_obj[kl]
        return abs(k - i) + abs(l - j) + abs(a_kl - a_ij)
    
    @staticmethod
    def reconstruct_path(came_from: Dict[Tuple[int, int], Tuple[int, int]], 
                        current: Tuple[int, int]) -> List[Tuple[int, int]]:
        path = [current]
        while current in came_from:
            current = came_from[current]
            path.append(current)
        path.reverse()
        return path
    
    @staticmethod
    def a_star(map_obj: Map, start: Tuple[int, int], goal: Tuple[int, int]) -> Optional[Tuple[List[Tuple[int, int]], float]]:
        open_set = []
        heapq.heappush(open_set, (0, start))
        
        came_from = {}
        g_score = {start: 0}
        f_score = {start: PathFinder.manhattan_distance(start, goal)}
        open_set_hash = {start}
        
        while open_set:
            current = heapq.heappop(open_set)[1]
            open_set_hash.remove(current)
            
            if current == goal:
                path = PathFinder.reconstruct_path(came_from, current)
                return path, g_score[current]
            
            for neighbor in map_obj.neighbors(*current):
                tentative_g_score = g_score[current] + PathFinder.transition_cost(current, neighbor, map_obj)
                
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score[neighbor] = tentative_g_score + PathFinder.manhattan_distance(neighbor, goal)
                    if neighbor not in open_set_hash:
                        heapq.heappush(open_set, (f_score[neighbor], neighbor))
                        open_set_hash.add(neighbor)
        return None
    
    @staticmethod
    def find_all_paths(map_obj: Map) -> Dict[Tuple[Tuple[int, int], Tuple[int, int]], List[Tuple[int, int]]]:
        rows, cols = map_obj.size()
        paths = {}
        accessible = []
        
        # Собираем все доступные точки
        for i in range(rows):
            for j in range(cols):
                if map_obj[(i, j)] != 0:
                    accessible.append((i, j))
        
        # Находим пути между всеми парами точек
        for i, start in enumerate(accessible):
            for goal in accessible[i+1:]:
                result = PathFinder.a_star(map_obj, start, goal)
                if result:
                    path, _ = result
                    paths[(start, goal)] = path
        return paths
    
    @staticmethod
    def visualize_path(map_obj: Map, path: List[Tuple[int, int]]) -> str:
        rows, cols = map_obj.size()
        visualization = []
        path_set = set(path)
        start = path[0]
        goal = path[-1]
        
        for i in range(rows):
            row_str = []
            for j in range(cols):
                if (i, j) == start:
                    row_str.append('>')
                elif (i, j) == goal:
                    row_str.append('x')
                elif (i, j) in path_set:
                    row_str.append('*')
                elif map_obj[(i, j)] == 0:
                    row_str.append('8')
                else:
                    row_str.append(' ')
            visualization.append(''.join(row_str))
        return '\n'.join(visualization)