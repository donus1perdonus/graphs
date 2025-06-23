#!/usr/bin/env python3
"""
Основной файл для запуска лабораторных работ по теории графов.
"""

import sys
import os
import argparse
from typing import List, Optional

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

# Сопоставление коротких ключей с возможными шаблонами имён файлов
FILE_PATTERNS = {
    'matrix':      ["matrix_t{task}_{num}.txt", "adjacency_matrix_t{task}_{num}.txt"],
    'adjacency_list': ["adjacency_list_t{task}_{num}.txt", "list_of_adjacency_t{task}_{num}.txt"],
    'list_of_edges':  ["list_of_edges_t{task}_{num}.txt", "edges_t{task}_{num}.txt"]
}


def run_task(task_number: int, test_number: Optional[str] = None, algorithm: str = 'dfs', input_type: Optional[str] = None, show_result: bool = False):
    """
    Запускает указанное задание.
    """
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


def run_single_test(task_number: int, test_number: str, task_module, algorithm: str = 'dfs', input_type: Optional[str] = None, show_result: bool = False):
    test_dir = f"graph-tests/task{task_number}"
    test_files = {}
    for file_type, internal_type in FILE_TYPES.items():
        for pattern in FILE_PATTERNS[file_type]:
            file_path = os.path.join(test_dir, pattern.format(task=task_number, num=test_number))
            if os.path.exists(file_path):
                test_files[file_type] = (file_path, internal_type)
                break
    if not test_files:
        print(f"Тест {test_number} для задания {task_number} не найден")
        return
    # Выбор файла по input_type или первого найденного
    if input_type and input_type in INPUT_TYPE_MAPPING:
        mapped_type = INPUT_TYPE_MAPPING[input_type]
        if mapped_type in test_files:
            file_path, internal_type = test_files[mapped_type]
        else:
            file_path, internal_type = list(test_files.values())[0]
    else:
        file_path, internal_type = list(test_files.values())[0]
    print(f"Задание {task_number}, тест {test_number}:")
    print("=" * 60)
    print(f"Используется файл: {os.path.basename(file_path)}")
    try:
        from utils import Graph
        graph = Graph(file_path, internal_type)
        if task_number == 1:
            result = task_module.solve_task(graph, algorithm)
        else:
            result = task_module.solve_task(graph)
        answer_file = os.path.join(test_dir, f"ans_t{task_number}_{test_number}.txt")
        passed = False
        expected = None
        if os.path.exists(answer_file):
            with open(answer_file, 'r', encoding='utf-8') as f:
                expected = f.read().strip()
            passed = (result.strip() == expected)
        else:
            passed = True  # Нет эталона — считаем тест пройденным
        if passed:
            print("  ✓ ПРОШЁЛ")
        else:
            print("  ✗ НЕ ПРОШЁЛ")
        if show_result:
            print("\nРезультат:")
            print(result)
            if expected is not None:
                print(f"\nОжидаемый результат:\n{expected}")
    except Exception as e:
        print(f"Ошибка при выполнении теста: {e}")


def run_all_tests(task_number: int, task_module, algorithm: str = 'dfs', input_type: Optional[str] = None, show_result: bool = False):
    test_dir = f"graph-tests/task{task_number}"
    if not os.path.exists(test_dir):
        print(f"Папка с тестами для задания {task_number} не найдена")
        return
    print(f"Задание {task_number} - все тесты:")
    print("=" * 60)
    # Собираем все тесты по всем шаблонам имён файлов
    test_nums = set()
    for file_type in FILE_TYPES:
        for filename in os.listdir(test_dir):
            for pattern in FILE_PATTERNS[file_type]:
                prefix = pattern.format(task=task_number, num="")[:-4]  # убираем .txt
                if filename.startswith(prefix) and filename.endswith(".txt"):
                    num = filename[len(prefix):-4]
                    test_nums.add(num)
    if not test_nums:
        print(f"Тестовые файлы для задания {task_number} не найдены")
        return
    passed_tests = 0
    total_tests = len(test_nums)
    for test_num in sorted(test_nums):
        test_files = {}
        for file_type, internal_type in FILE_TYPES.items():
            for pattern in FILE_PATTERNS[file_type]:
                file_path = os.path.join(test_dir, pattern.format(task=task_number, num=test_num))
                if os.path.exists(file_path):
                    test_files[file_type] = (file_path, internal_type)
                    break
        if not test_files:
            print(f"  Файлы для теста {test_num} не найдены")
            continue
        # Выбор файла по input_type или первого найденного
        if input_type and input_type in INPUT_TYPE_MAPPING:
            mapped_type = INPUT_TYPE_MAPPING[input_type]
            if mapped_type in test_files:
                file_path, internal_type = test_files[mapped_type]
            else:
                file_path, internal_type = list(test_files.values())[0]
        else:
            file_path, internal_type = list(test_files.values())[0]
        try:
            from utils import Graph
            graph = Graph(file_path, internal_type)
            if task_number == 1:
                result = task_module.solve_task(graph, algorithm)
            else:
                result = task_module.solve_task(graph)
            answer_file = os.path.join(test_dir, f"ans_t{task_number}_{test_num}.txt")
            passed = False
            expected = None
            if os.path.exists(answer_file):
                with open(answer_file, 'r', encoding='utf-8') as f:
                    expected = f.read().strip()
                passed = (result.strip() == expected)
            else:
                passed = True
            if passed:
                print(f"Тест {test_num}: ✓ ПРОШЁЛ")
                passed_tests += 1
            else:
                print(f"Тест {test_num}: ✗ НЕ ПРОШЁЛ")
            if show_result:
                print("\nРезультат:")
                print(result)
                if expected is not None:
                    print(f"\nОжидаемый результат:\n{expected}")
        except Exception as e:
            print(f"Тест {test_num}: ✗ ОШИБКА: {e}")
    print(f"\nИтого: {passed_tests}/{total_tests} тестов прошли успешно")


def main():
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
    parser.add_argument(
        'task_number',
        type=int,
        help='Номер задания (1-20)'
    )
    parser.add_argument(
        'test_number',
        nargs='?',
        help='Номер конкретного теста (например, 001) или не указывать для всех тестов'
    )
    parser.add_argument(
        '--algorithm',
        choices=['dfs', 'bfs'],
        default='dfs',
        help='Алгоритм для задания 1 (по умолчанию: dfs)'
    )
    parser.add_argument(
        '-i', '--input-type',
        choices=['m', 'a', 'e'],
        help='Тип входного файла: m (matrix), a (adjacency_list), e (list_of_edges)'
    )
    parser.add_argument(
        '-s', '--show-result',
        action='store_true',
        help='Показывать подробный результат и эталон'
    )
    args = parser.parse_args()
    if args.task_number < 1 or args.task_number > 20:
        print("Ошибка: Номер задания должен быть от 1 до 20")
        sys.exit(1)
    run_task(args.task_number, args.test_number, args.algorithm, args.input_type, args.show_result)


if __name__ == "__main__":
    main()
