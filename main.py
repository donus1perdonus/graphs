"""
Основной файл для запуска лабораторных работ по теории графов.
"""

import sys
import os
import argparse
import glob
from typing import Optional, Dict, Tuple, List

# Константы
MIN_TASK_NUMBER = 1
MAX_TASK_NUMBER = 15
DEFAULT_ALGORITHM = 'dfs'

# Типы файлов и их маппинг
FILE_TYPES = {
    'matrix': 'matrix',
    'adjacency_list': 'adjacency_list', 
    'list_of_edges': 'edges'
}

INPUT_TYPE_MAPPING = {
    'm': 'matrix',
    'a': 'adjacency_list',
    'e': 'list_of_edges'
}

FILE_PATTERNS = {
    'matrix': "matrix_t{task}_{num}.txt",
    'adjacency_list': "list_of_adjacency_t{task}_{num}.txt",
    'list_of_edges': "list_of_edges_t{task}_{num}.txt"
}

class TestResult:
    """Класс для хранения результатов тестирования"""
    def __init__(self, passed: bool, result: str = "", expected: str = "", error: str = ""):
        self.passed = passed
        self.result = result
        self.expected = expected
        self.error = error

def get_test_directory(task_number: int) -> str:
    """Возвращает путь к директории с тестами для заданного задания"""
    return f"graph-tests/task{task_number}"

def load_answer_file(answer_file_path: str) -> Optional[str]:
    """Загружает содержимое файла с ответом"""
    try:
        with open(answer_file_path, 'r', encoding='utf-8') as f:
            return f.read().strip()
    except FileNotFoundError:
        return None
    except Exception as e:
        print(f"Ошибка при чтении файла ответа {answer_file_path}: {e}")
        return None

def compare_results(result: str, expected: str) -> bool:
    """Сравнивает полученный результат с ожидаемым"""
    return result.strip() == expected.strip()

def print_test_header(task_number: int, test_number: str, file_path: str):
    """Выводит заголовок теста"""
    print(f"Задание {task_number}, тест {test_number}:")
    print("=" * 60)
    print(f"Используется файл: {os.path.basename(file_path)}")

def print_test_result(result: TestResult, show_result: bool = False):
    """Выводит результат теста"""
    if result.error:
        print(f"  ✗ ОШИБКА: {result.error}")
    else:
        print("  ✓ ПРОШЁЛ" if result.passed else "  ✗ НЕ ПРОШЁЛ")
        
    if show_result and not result.error:
        print("  Получено:")
        print(result.result)
        if result.expected:
            print("  Ожидалось:")
            print(result.expected)

def process_graph_task(task_number: int, test_number: str, task_module, algorithm: str, 
                      file_path: str, internal_type: str, test_dir: str, show_result: bool = False) -> TestResult:
    """Обрабатывает стандартное задание с графами"""
    try:
        from utils import Graph
        graph = Graph(file_path, internal_type)
        
        if task_number == 1:
            result = task_module.solve_task(graph, algorithm)
        elif task_number == 11:
            result = task_module.solve_task(graph, test_number)
        else:
            result = task_module.solve_task(graph)
        
        answer_file = os.path.join(test_dir, f"ans_t{task_number}_{test_number}.txt")
        expected = load_answer_file(answer_file)
        passed = expected is None or compare_results(result, expected)
        
        return TestResult(passed, result, expected or "")
        
    except Exception as e:
        return TestResult(False, error=str(e))

def process_map_task(task_number: int, test_number: str, task_module, file_path: str, 
                    test_dir: str, show_result: bool = False) -> TestResult:
    """Обрабатывает задание с картами (задание 12)"""
    try:
        from utils import Map
        answer_file = os.path.join(test_dir, f"ans_t{task_number}_{test_number}.txt")
        if not os.path.exists(answer_file):
            return TestResult(False, error=f"Файл-ответ для теста {test_number} не найден")
        
        result = task_module.solve_task(file_path, answer_file)
        expected = load_answer_file(answer_file)
        passed = expected is None or compare_results(result, expected)
        
        return TestResult(passed, result, expected or "")
        
    except Exception as e:
        return TestResult(False, error=str(e))

def process_maze_task(task_number: int, test_number: str, task_module, test_dir: str, 
                     show_result: bool = False) -> TestResult:
    """Обрабатывает задание с лабиринтами (задание 6)"""
    maze_file = os.path.join(test_dir, f"maze_t6_{test_number}.txt")
    if not os.path.exists(maze_file):
        return TestResult(False, error=f"Файл лабиринта для теста {test_number} не найден")
    
    answer_files = sorted(glob.glob(os.path.join(test_dir, f"ans_maze_t6_{test_number}_ans_*.txt")))
    if not answer_files:
        return TestResult(False, error=f"Файл-ответ для теста {test_number} не найден")
    
    try:
        result = task_module.solve_task(maze_file, answer_files[0])
        expected = load_answer_file(answer_files[0])
        
        if not expected:
            return TestResult(False, error="Не удалось загрузить ожидаемый результат")
        
        result_lines = result.strip().splitlines()
        expected_lines = expected.strip().splitlines()
        
        # Специальная логика сравнения для лабиринтов
        if len(result_lines) > 1 and any('Path:' in line for line in result_lines[:3]):
            passed = result_lines[:3] == expected_lines[:3]
        else:
            passed = result_lines[0] == expected_lines[0] if result_lines and expected_lines else False
        
        return TestResult(passed, result, expected)
        
    except Exception as e:
        return TestResult(False, error=str(e))

def process_standard_task(task_number: int, test_number: str, task_module, algorithm: str, 
                         file_path: str, internal_type: str, test_dir: str, show_result: bool = False) -> bool:
    """Обрабатывает стандартное задание"""
    print_test_header(task_number, test_number, file_path)
    
    if task_number == 12:
        result = process_map_task(task_number, test_number, task_module, file_path, test_dir, show_result)
    else:
        result = process_graph_task(task_number, test_number, task_module, algorithm, 
                                  file_path, internal_type, test_dir, show_result)
    
    print_test_result(result, show_result)
    return result.passed

def find_test_files(task_number: int, test_number: str, test_dir: str) -> Dict[str, Tuple[str, str]]:
    """Находит файлы тестов для заданного номера теста"""
    test_files = {}
    
    for file_type, internal_type in FILE_TYPES.items():
        pattern = FILE_PATTERNS[file_type]
        file_path = os.path.join(test_dir, pattern.format(task=task_number, num=test_number))
        if os.path.exists(file_path):
            test_files[file_type] = (file_path, internal_type)
    
    return test_files

def select_input_file(test_files: Dict[str, Tuple[str, str]], input_type: Optional[str] = None) -> Tuple[str, str]:
    """Выбирает входной файл на основе предпочтений пользователя"""
    if input_type and input_type in INPUT_TYPE_MAPPING:
        mapped_type = INPUT_TYPE_MAPPING[input_type]
        if mapped_type in test_files:
            return test_files[mapped_type]
    
    return list(test_files.values())[0]

def run_single_test(task_number: int, test_number: str, task_module, algorithm: str = 'dfs', 
                   input_type: Optional[str] = None, show_result: bool = False) -> bool:
    """Запускает один конкретный тест"""
    test_dir = get_test_directory(task_number)
    
    # Особая обработка для задания 6 (лабиринты)
    if task_number == 6:
        print_test_header(task_number, test_number, f"maze_t6_{test_number}.txt")
        result = process_maze_task(task_number, test_number, task_module, test_dir, show_result)
        print_test_result(result, show_result)
        return result.passed
    
    # Особая обработка для задания 12 (карты)
    if task_number == 12:
        return run_map_test(task_number, test_number, task_module, test_dir, show_result)
    
    # Обычная обработка для графов
    test_files = find_test_files(task_number, test_number, test_dir)
    if not test_files:
        print(f"Тест {test_number} для задания {task_number} не найден")
        return False
    
    file_path, internal_type = select_input_file(test_files, input_type)
    return process_standard_task(task_number, test_number, task_module, algorithm, 
                               file_path, internal_type, test_dir, show_result)

def run_map_test(task_number: int, test_number: str, task_module, test_dir: str, show_result: bool = False) -> bool:
    """Запускает тест для карт (задание 12)"""
    map_file = os.path.join(test_dir, f"map_{test_number}.txt")
    if not os.path.exists(map_file):
        print(f"Файл карты для теста {test_number} не найден")
        return False
    
    answer_files = sorted(glob.glob(os.path.join(test_dir, f"map_{test_number}_ans_*.txt")))
    if not answer_files:
        print(f"Файлы-ответы для теста {test_number} не найдены")
        return False
    
    print_test_header(task_number, test_number, f"map_{test_number}.txt")
    print(f"Найдено файлов ответов: {len(answer_files)}")
    
    passed_tests = 0
    total_tests = len(answer_files)
    
    for i, answer_file in enumerate(answer_files, 1):
        print(f"  Ответ {i}:")
        try:
            result = task_module.solve_task(map_file, answer_file)
            expected = load_answer_file(answer_file)
            passed = expected is None or compare_results(result, expected)
            
            print("    ✓ ПРОШЁЛ" if passed else "    ✗ НЕ ПРОШЁЛ")
            if passed:
                passed_tests += 1
            
            if show_result:
                print("    Получено:")
                print(result)
                print("    Ожидалось:")
                print(expected)
                
        except Exception as e:
            print(f"    ✗ ОШИБКА: {e}")
    
    print(f"\n  Итого: {passed_tests}/{total_tests} ответов прошли успешно")
    return passed_tests == total_tests

def get_test_numbers_for_task(task_number: int, test_dir: str) -> List[str]:
    """Получает список номеров тестов для заданного задания"""
    if task_number == 12:
        # Особая обработка для карт
        test_nums = set()
        for filename in os.listdir(test_dir):
            if filename.startswith("map_") and filename.endswith(".txt") and "_ans_" not in filename:
                parts = filename.split("_")
                if len(parts) >= 2 and parts[0] == "map":
                    num = parts[1].replace(".txt", "")
                    test_nums.add(num)
        return sorted(test_nums)
    
    # Обычная обработка для графов
    test_nums = set()
    for file_type in FILE_TYPES:
        pattern = FILE_PATTERNS[file_type]
        for filename in os.listdir(test_dir):
            prefix = pattern.format(task=task_number, num="")[:-4]
            if filename.startswith(prefix) and filename.endswith(".txt"):
                num = filename[len(prefix):-4]
                test_nums.add(num)
    
    return sorted(test_nums)

def run_all_tests(task_number: int, task_module, algorithm: str = 'dfs', 
                 input_type: Optional[str] = None, show_result: bool = False) -> None:
    """Запускает все тесты для заданного задания"""
    test_dir = get_test_directory(task_number)
    if not os.path.exists(test_dir):
        print(f"Папка с тестами для задания {task_number} не найдена")
        return
    
    print(f"Задание {task_number} - все тесты:")
    print("=" * 60)
    
    test_nums = get_test_numbers_for_task(task_number, test_dir)
    if not test_nums:
        print(f"Тестовые файлы для задания {task_number} не найдены")
        return
    
    passed_tests = 0
    total_tests = len(test_nums)
    
    for test_num in test_nums:
        if task_number == 12:
            # Особая обработка для карт
            passed = run_map_test(task_number, test_num, task_module, test_dir, show_result)
            if passed:
                passed_tests += 1
        else:
            # Обычная обработка для графов
            test_files = find_test_files(task_number, test_num, test_dir)
            if not test_files:
                print(f"  Файлы для теста {test_num} не найдены")
                continue
            
            file_path, internal_type = select_input_file(test_files, input_type)
            try:
                passed = process_standard_task(task_number, test_num, task_module, algorithm, 
                                            file_path, internal_type, test_dir, show_result)
                if passed:
                    passed_tests += 1
            except Exception as e:
                print(f"Тест {test_num}: ✗ ОШИБКА: {e}")
    
    print(f"\nИтого: {passed_tests}/{total_tests} тестов прошли успешно")

def run_task(task_number: int, test_number: Optional[str] = None, algorithm: str = DEFAULT_ALGORITHM, 
            input_type: Optional[str] = None, show_result: bool = False) -> None:
    """Основная функция для запуска задания"""
    task_module_name = f"tasks.task{task_number}"
    
    try:
        task_module = __import__(task_module_name, fromlist=['solve_task'])
        
        if test_number:
            run_single_test(task_number, test_number, task_module, algorithm, input_type, show_result)
        else:
            run_all_tests(task_number, task_module, algorithm, input_type, show_result)
            
    except ImportError as e:
        print(f"Ошибка: Модуль {task_module_name} не найден или не содержит функцию solve_task")
        print(f"Детали: {e}")
    except Exception as e:
        print(f"Ошибка при выполнении задания {task_number}: {e}")

def validate_task_number(task_number: int) -> bool:
    """Проверяет корректность номера задания"""
    return MIN_TASK_NUMBER <= task_number <= MAX_TASK_NUMBER

def main() -> None:
    """Главная функция программы"""
    parser = argparse.ArgumentParser(
        description="Лабораторная работа по теории графов",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Примеры использования:
  py main.py 1                    # Задание 1, все тесты
  py main.py 1 001               # Задание 1, тест 001
  py main.py 1 001 --algorithm bfs  # Задание 1, тест 001, алгоритм BFS
  py main.py 2 001               # Задание 2, тест 001
  py main.py 1 -i a --show-result  # Все тесты, только списки смежности, с выводом результатов
  py main.py 1 001 -i e  # Задание 1, тест 001, только список рёбер
        """
    )
    
    parser.add_argument('task_number', type=int, help=f'Номер задания ({MIN_TASK_NUMBER}-{MAX_TASK_NUMBER})')
    parser.add_argument('test_number', nargs='?', help='Номер конкретного теста (например, 001) или не указывать для всех тестов')
    parser.add_argument('--algorithm', choices=['dfs', 'bfs'], default=DEFAULT_ALGORITHM, 
                       help='Алгоритм для задания 1 (по умолчанию: dfs)')
    parser.add_argument('-i', '--input-type', choices=['m', 'a', 'e'], 
                       help='Тип входного файла: m (matrix), a (adjacency_list), e (list_of_edges)')
    parser.add_argument('-s', '--show-result', action='store_true', 
                       help='Показывать подробный результат и эталон')
    
    args = parser.parse_args()
    
    if not validate_task_number(args.task_number):
        print(f"Ошибка: Номер задания должен быть от {MIN_TASK_NUMBER} до {MAX_TASK_NUMBER}")
        sys.exit(1)
    
    run_task(args.task_number, args.test_number, args.algorithm, args.input_type, args.show_result)

if __name__ == "__main__":
    main()
