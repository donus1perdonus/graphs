from utils import Graph
import random
import math


def solve_task(graph: Graph) -> str:
    n = graph.size()
    matrix = graph.adjacency_matrix()
    
    # Параметры алгоритма муравьиной колонии
    alpha = 1.0  # Влияние феромона
    beta = 5.0   # Влияние расстояния
    evaporation = 0.5  # Коэффициент испарения
    Q = 100      # Количество феромона, выделяемого муравьём
    num_ants = max(10, n)  # Количество муравьёв
    num_iterations = 200   # Количество итераций

    # Инициализация феромонов
    pheromone = [[1.0 for _ in range(n)] for _ in range(n)]
    best_length = float('inf')
    best_path = None

    def path_length(path):
        return sum(matrix[path[i]][path[i+1]] for i in range(n-1)) + matrix[path[-1]][path[0]]

    for iteration in range(num_iterations):
        all_paths = []
        all_lengths = []
        for ant in range(num_ants):
            unvisited = set(range(n))
            path = []
            current = random.randint(0, n-1)
            path.append(current)
            unvisited.remove(current)
            while unvisited:
                probabilities = []
                denom = 0.0
                for j in unvisited:
                    tau = pheromone[current][j] ** alpha
                    eta = (1.0 / matrix[current][j]) ** beta if matrix[current][j] > 0 else 0
                    denom += tau * eta
                for j in unvisited:
                    tau = pheromone[current][j] ** alpha
                    eta = (1.0 / matrix[current][j]) ** beta if matrix[current][j] > 0 else 0
                    prob = (tau * eta) / denom if denom > 0 else 0
                    probabilities.append((j, prob))
                # Рулетка
                r = random.random()
                acc = 0.0
                for j, prob in probabilities:
                    acc += prob
                    if r <= acc:
                        next_city = j
                        break
                else:
                    next_city = probabilities[-1][0]
                path.append(next_city)
                unvisited.remove(next_city)
                current = next_city
            all_paths.append(path)
            length = path_length(path)
            all_lengths.append(length)
            if length < best_length:
                best_length = length
                best_path = path[:]
        # Испарение феромона
        for i in range(n):
            for j in range(n):
                pheromone[i][j] *= (1 - evaporation)
        # Добавление феромона
        for path, length in zip(all_paths, all_lengths):
            for i in range(n):
                a = path[i]
                b = path[(i+1)%n]
                pheromone[a][b] += Q / length
                pheromone[b][a] += Q / length
    # Формируем результат
    if best_path is None:
        return "Не удалось найти путь."
    result = f"Length of shortest traveling salesman path is: {best_length}.\nPath:\n"
    for i in range(n):
        u = best_path[i] + 1
        v = best_path[(i+1)%n] + 1
        w = matrix[best_path[i]][best_path[(i+1)%n]]
        result += f"{u}-{v} : {w}\n"
    return result.strip() 