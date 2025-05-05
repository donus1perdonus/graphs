from typing import List
import os

from utils.map import Map, PathFinder

"""
6.  Найти проход в лабиринте от начальной точки до конечной.
"""
def task6(answer_basename: str,
            task_basename: str,
            number_of_tasks: int
            ):
    def process_all_mazes(maze_files: List[str]):
        for maze_file in maze_files:
            if not os.path.exists(maze_file):
                print(f"Файл {maze_file} не найден, пропускаем...")
                continue
            
            print(f"\nОбработка лабиринта: {maze_file}")
            map_obj = Map(maze_file)
            
            # Находим все пути между доступными точками
            all_paths = PathFinder.find_all_paths(map_obj)
            
            # Создаем папку для результатов
            output_dir = "maze_paths"
            os.makedirs(output_dir, exist_ok=True)
            
            # Сохраняем результаты
            base_name = os.path.splitext(os.path.basename(maze_file))[0]
            output_file = os.path.join(output_dir, f"{base_name}_paths.txt")
            
            with open(output_file, 'w') as f:
                for (start, goal), path in all_paths.items():
                    f.write(f"Path from {start} to {goal} (length {len(path)-1}):\n")
                    f.write(f"Coordinates: {path}\n")
                    f.write(f"Visualization:\n{PathFinder.visualize_path(map_obj, path)}\n")
                    f.write("\n" + "="*50 + "\n")
            
            print(f"Результаты сохранены в {output_file}")

    maze_files = [f"graph-tests\\task6\\{task_basename}_{i:03}.txt" for i in range(1, number_of_tasks + 1)]
    process_all_mazes(maze_files)


if __name__ == '__main__':
    task6(
        answer_basename='puk',
        task_basename='maze_t6',
        number_of_tasks=1
    )