import random

# Definição das posições com barreiras
positions = [
    [0, 4, -1], [0, 11, -1], [1, 1, -1], [1, 11, -1],
    [2, 0, -1], [2, 2, -1], [2, 6, -1], [2, 8, -1],
    [2, 9, -1], [3, 1, -1], [3, 8, -1], [5, 6, -1],
    [8, 6, -1],
]

# Definição das zonas nulas
null_zone = [
    [6, 0, 3], [6, 8, 11], [9, 0, 3], [9, 8, 11]
]

# Formato da matriz (exemplo visual)
"""
    Formato da matriz:
    (0,0), (0,1), (0,2), (0,3), (0,4), (0,5), (0,6), (0,7), (0,8), (0,9), (0,10), (0,11)
    (1,0), (1,1), (1,2), (1,3), (1,4), (1,5), (1,6), (1,7), (1,8), (1,9), (1,10), (1,11)
    ...
"""

def create_table(mat):
    """
    Cria a Q-table e a tabela de ambiente.
    Args:
        mat (list): Matriz do ambiente.

    Returns:
        tuple: Q-table e tabela de ambiente.
    """
    q_table = {}
    ambient_table = {}

    for i in range(len(mat)):
        for j in range(len(mat[0])):
            if mat[i][j] is not None:
                q_table[(i, j)] = {"up": 0, "left": 0, "right": 0, "down": 0}
                ambient_table[(i, j)] = {}

                # Verifica conexões válidas
                if i > 0 and mat[i - 1][j] is not None:
                    q_table[(i, j)]["up"] = 1
                    ambient_table[(i, j)][(i - 1, j)] = 0
                if j > 0 and mat[i][j - 1] is not None:
                    q_table[(i, j)]["left"] = 1
                    ambient_table[(i, j)][(i, j - 1)] = 0
                if i < len(mat) - 1 and mat[i + 1][j] is not None:
                    q_table[(i, j)]["down"] = 1
                    ambient_table[(i, j)][(i + 1, j)] = 0
                if j < len(mat[0]) - 1 and mat[i][j + 1] is not None:
                    q_table[(i, j)]["right"] = 1
                    ambient_table[(i, j)][(i, j + 1)] = 0

    return q_table, ambient_table

def create_map():
    matrix = alloc_map()
    fill_with_barriers(matrix)
    return matrix

def fill_with_barriers(matrix):
    for row, col, val in positions:
        matrix[row][col] = val

    for row, start_col, end_col in null_zone:
        for col in range(start_col, end_col + 1):
            matrix[row][col] = None

def alloc_map():
    matrix = []
    for i in range(10):
        aux = []
        for j in range(12):
            aux.append(0)
        matrix.append(aux)
    return matrix

def options(position, qtable):
    options_list = []

    qtable_entry = qtable.get(position, {})
    north, south, west, east = qtable_entry.get("up", 0), qtable_entry.get("down", 0), qtable_entry.get("left", 0), qtable_entry.get("right", 0)

    if north > 0:
        options_list.append((position[0] - 1, position[1]))
    if south > 0:
        options_list.append((position[0] + 1, position[1]))
    if west > 0:
        options_list.append((position[0], position[1] - 1))
    if east > 0:
        options_list.append((position[0], position[1] + 1))

    if not options_list:
        print(f"No options available for position {position}.")
    return options_list

def calculate_reward(position, options_list, propagation, map):
    max_value = 0
    for option in options_list:
        option_value = map[option[0]][option[1]]
        if option_value > max_value:
            max_value = option_value

    value = propagation * map[position[0]][position[1]] + max_value
    return value

def is_qtable_stable(qtable, previous_qtable, threshold=0.01):
    for position in qtable:
        for direction in qtable[position]:
            current_value = qtable[position][direction]
            previous_value = previous_qtable.get(position, {}).get(direction, 0)
            if abs(current_value - previous_value) > threshold:
                return False
    return True

def run_model(map, qtable, start, end, propagation):
    position = start
    previous_qtable = {}

    while True:
        if is_qtable_stable(qtable, previous_qtable):
            print("Q-table has stabilized. Stopping execution.")
            break

        previous_qtable = {pos: qtable[pos].copy() for pos in qtable}

        while position != end:
            options_list = options(position, qtable)
            if not options_list:
                print(f"No options available for position {position}.")
                break

            if random.random() < 0.3:
                next_position = random.choice(options_list)
            else:
                next_position = max(options_list, key=lambda opt: map[opt[0]][opt[1]])

            reward = calculate_reward(position, options_list, propagation, map)

            direction = None
            if next_position == (position[0] - 1, position[1]):
                direction = "up"
            elif next_position == (position[0] + 1, position[1]):
                direction = "down"
            elif next_position == (position[0], position[1] - 1):
                direction = "left"
            elif next_position == (position[0], position[1] + 1):
                direction = "right"

            if direction:
                qtable[position][direction] = reward

            position = next_position

        position = start