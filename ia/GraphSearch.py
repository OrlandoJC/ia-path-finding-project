import numpy as np
import random
from concurrent import futures
import multiprocessing, time, concurrent

obstacles = [(5, 19, 18), (10, 23, 13), (2, 10, 10)]

def get_path(inicio_bot, fin_objetivo, obstacl, a, g, e, ep):
    # Definición de hiperparámetros
    alpha = a
    gamma = g
    epsilon = e
    num_episodes = ep

    grid = np.zeros((24, 24))
    grid [0, :] = 1
    grid [-1, :] = 1
    grid [:, 0] = 1
    grid [:, -1] = 1


    for obstacle in obstacl:
        grid[obstacle[0]:obstacle[1], obstacle[2]] = 1

    # esquinas
    grid[1, 23] = 1
    grid[3, 23] = 1
    grid[5, 23] = 1
    grid[7, 23] = 1
    grid[9, 23] = 1
    grid[11, 23] = 1
    grid[13, 23] = 1
    grid[15, 23] = 1
    grid[17, 23] = 1

    grid[fin_objetivo[0] -1, 10] = 1
    grid[fin_objetivo[0] +1, 10] = 1

    recompensa = 0

    # Definición de acciones
    actions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    # Función para obtener las acciones válidas desde un estado
    def get_valid_actions(state):
        valid_actions = []
        for action in actions:
            next_row = state[0] + action[0]
            next_col = state[1] + action[1]
            if 0 <= next_row < 24 and 0 <= next_col < 24 and grid[next_row][next_col] != 1:
                valid_actions.append(action)
        return valid_actions

    # Función para obtener el siguiente estado dado un estado y una acción
    def get_next_state(state, action):
        next_row = state[0] + action[0]
        next_col = state[1] + action[1]
        return next_row, next_col

    # Inicialización de la tabla Q
    Q_table = {(state, action): 0 for state in np.ndindex((24, 24))
               for action in actions}

    # Definición del estado inicial
    inicio = inicio_bot
    # Definición del estado final
    goal_state = fin_objetivo

    # Entrenamiento del agente
    for episode in range(num_episodes):
        state = inicio
        while state != goal_state:
            if random.uniform(0, 1) < epsilon:
                action = random.choice(get_valid_actions(state))
            else:
                best_actions = [a for a in get_valid_actions(state) if Q_table[(
                    state, a)] == max(Q_table[(state, a)] for a in get_valid_actions(state))]
                action = random.choice(best_actions)
            next_state = get_next_state(state, action)
            reward = -1 if next_state != goal_state else 0
            Q_next = max(Q_table[(next_state, a)] for a in get_valid_actions(
                next_state)) if next_state != goal_state else 0
            Q_table[(state, action)] += alpha * (reward +
                                                 gamma * Q_next - Q_table[(state, action)])
            state = next_state

    # Evaluación del agente entrenado
    state = inicio
    path = [state]
    while state != goal_state:
        best_actions = [a for a in get_valid_actions(state) if Q_table[(
            state, a)] == max(Q_table[(state, a)] for a in get_valid_actions(state))]
        action = random.choice(best_actions)
        next_state = get_next_state(state, action)
        path.append(next_state)
        state = next_state
        recompensa = recompensa + Q_table[(state, action)]

    # Impresión de la ruta encontrada por el agente
    # print("----------------------")

    # for i in range(24):
    #     for j in range(24):
    #         if (i, j) in path:
    #             print("* ", end="")
    #         elif grid[i][j] == 1:
    #             print("█ ", end="")
    #         else:
    #             print(". ", end="")
    #     print()


    return [abs(recompensa), path]


# print(get_path((2, 23), (15,10)))
n_veces = 8

# Función para generar argumentos diferentes para cada llamada a get_path()

def generar_argumentos(goal_selected, obstacles, a, g, e, ep):
    # Lista de argumentos para arg1 y arg2
    args_list = [((2, 23),  goal_selected, obstacles, a, g, e, ep),
                 ((4, 23),  goal_selected, obstacles, a, g, e, ep),
                 ((6, 23),  goal_selected, obstacles, a, g, e, ep),
                 ((8, 23),  goal_selected, obstacles, a, g, e, ep),
                 ((10, 23), goal_selected, obstacles, a, g, e, ep),
                 ((12, 23), goal_selected, obstacles, a, g, e, ep),
                 ((14, 23), goal_selected, obstacles, a, g, e, ep),
                 ((16, 23), goal_selected, obstacles, a, g, e, ep)]

    # Obtener n_veces argumentos diferentes de forma aleatoria
    argumentos = []

    for _ in range(n_veces):
        argumento = args_list.pop(0)
        argumentos.append(argumento)

    return argumentos

# Función para ejecutar get_path en paralelo con argumentos diferentes
def ejecutar_en_paralelo(goal_selected, obstacles, a, g, e, ep):
    # Crear un Pool de procesos en paralelo
    with multiprocessing.Pool() as pool:
        # Obtener argumentos diferentes para cada llamada
        argumentos = generar_argumentos(goal_selected, obstacles, a, g, e, ep)

        # Usar pool.starmap_async para ejecutar la función asincrónicamente con los argumentos generados
        resultados = pool.starmap_async(get_path, argumentos)

        # Obtener los objetos MapResult
        resultados = resultados.get()

        # Retornar los resultados obtenidos
        return resultados

# Inicio de la ejecución en paralelo
if __name__ == '__main__':

    inicio = time.time()

    # Llamar a la función para ejecutar en paralelo
    resultados = ejecutar_en_paralelo()

    # Tiempo total de ejecución
    tiempo_total = time.time() - inicio

    print(f"Tiempo total: {tiempo_total} segundos")

    # Imprimir los resultados obtenidos
    print("Resultados:")

    recompensas = []

    for resultado in resultados:
        recompensas.append(resultado)

    print(max(recompensas))
