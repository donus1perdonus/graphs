"""
Задание 15: Задача коммивояжёра (Traveling Salesman Problem)

Реализует алгоритм муравьиной колонии (Ant Colony Optimization, ACO)
для решения задачи коммивояжёра - поиска кратчайшего гамильтонова цикла.

Алгоритм:
1. Инициализация феромонов на всех рёбрах
2. Для каждой итерации:
   - Каждый муравей строит путь, выбирая следующую вершину
   - Вероятность выбора зависит от феромона и расстояния
   - Обновление феромонов: испарение + добавление нового
3. Возврат лучшего найденного пути

Временная сложность: O(I * A * V^2), где I - итерации, A - муравьи, V - вершины
Пространственная сложность: O(V^2)

Параметры алгоритма:
- alpha: влияние феромона (1.0)
- beta: влияние расстояния (5.0)
- evaporation: коэффициент испарения (0.5)
- Q: количество феромона (100)
- num_ants: количество муравьёв (max(10, V))
- num_iterations: количество итераций (200)
"""

from utils import Graph
import random
import math


def solve_task(graph: Graph) -> str:
    """
    Решает задачу коммивояжёра с помощью алгоритма муравьиной колонии.
    
    Алгоритм муравьиной колонии - это метаэвристический алгоритм, основанный
    на поведении муравьёв при поиске пищи. Муравьи оставляют феромон на пути,
    что помогает другим муравьям найти оптимальный маршрут.
    
    Args:
        graph: полный взвешенный граф (все вершины соединены рёбрами)
        
    Returns:
        Строка с результатом в формате:
        "Length of shortest traveling salesman path is: <длина>.\nPath:\n<путь>"
    """
    n = graph.size()
    matrix = graph.adjacency_matrix()
    
    # Проверяем, что граф полный (все вершины соединены)
    for i in range(n):
        for j in range(n):
            if i != j and matrix[i][j] == 0:
                raise ValueError("Граф должен быть полным (все вершины соединены рёбрами)")
    
    # Параметры алгоритма муравьиной колонии
    alpha = 1.0      # Влияние феромона (важность феромона)
    beta = 5.0       # Влияние расстояния (жадность)
    evaporation = 0.5  # Коэффициент испарения феромона
    Q = 100          # Количество феромона, выделяемого муравьём
    num_ants = max(10, n)  # Количество муравьёв (зависит от размера графа)
    num_iterations = 200   # Количество итераций алгоритма

    # Инициализация феромонов на всех рёбрах
    pheromone = [[1.0 for _ in range(n)] for _ in range(n)]
    best_length = float('inf')
    best_path = None

    def path_length(path):
        """
        Вычисляет длину гамильтонова цикла.
        
        Args:
            path: список вершин в порядке обхода
            
        Returns:
            общая длина цикла
        """
        return sum(matrix[path[i]][path[i+1]] for i in range(n-1)) + matrix[path[-1]][path[0]]

    # Основной цикл алгоритма муравьиной колонии
    for iteration in range(num_iterations):
        all_paths = []
        all_lengths = []
        
        # Каждый муравей строит путь
        for ant in range(num_ants):
            unvisited = set(range(n))
            path = []
            
            # Случайный выбор стартовой вершины
            current = random.randint(0, n-1)
            path.append(current)
            unvisited.remove(current)
            
            # Построение пути муравьём
            while unvisited:
                probabilities = []
                denom = 0.0
                
                # Вычисляем знаменатель для вероятностей
                for j in unvisited:
                    tau = pheromone[current][j] ** alpha  # Уровень феромона
                    eta = (1.0 / matrix[current][j]) ** beta if matrix[current][j] > 0 else 0  # Привлекательность
                    denom += tau * eta
                
                # Вычисляем вероятности для каждой непосещённой вершины
                for j in unvisited:
                    tau = pheromone[current][j] ** alpha
                    eta = (1.0 / matrix[current][j]) ** beta if matrix[current][j] > 0 else 0
                    prob = (tau * eta) / denom if denom > 0 else 0
                    probabilities.append((j, prob))
                
                # Выбор следующей вершины методом рулетки
                r = random.random()
                acc = 0.0
                next_city = probabilities[-1][0]  # По умолчанию последняя
                
                for j, prob in probabilities:
                    acc += prob
                    if r <= acc:
                        next_city = j
                        break
                
                path.append(next_city)
                unvisited.remove(next_city)
                current = next_city
            
            all_paths.append(path)
            length = path_length(path)
            all_lengths.append(length)
            
            # Обновляем лучший путь
            if length < best_length:
                best_length = length
                best_path = path[:]
        
        # Испарение феромона на всех рёбрах
        for i in range(n):
            for j in range(n):
                pheromone[i][j] *= (1 - evaporation)
        
        # Добавление феромона на рёбрах, по которым прошли муравьи
        for path, length in zip(all_paths, all_lengths):
            for i in range(n):
                a = path[i]
                b = path[(i+1)%n]
                # Количество феромона обратно пропорционально длине пути
                pheromone[a][b] += Q / length
                pheromone[b][a] += Q / length  # Граф неориентированный
    
    # Проверяем, что найден путь
    if best_path is None:
        return "Не удалось найти путь."
    
    # Формируем результат в требуемом формате
    result = f"Length of shortest traveling salesman path is: {best_length}.\nPath:\n"
    for i in range(n):
        u = best_path[i] + 1      # Переводим в 1-индексацию для вывода
        v = best_path[(i+1)%n] + 1
        w = matrix[best_path[i]][best_path[(i+1)%n]]
        result += f"{u}-{v} : {w}\n"
    
    return result.strip() 