positions = [
    [0, 4, -1],
    [0, 11, -1],
    [1, 1, -1],
    [1, 11, -1],
    [2, 0, -1],
    [2, 2, -1],
    [2, 6, -1],
    [2, 8, -1],
    [2, 9, -1],
    [3, 1, -1],
    [3, 8, -1],
    [5, 6, -1],
    [8, 6, -1],
]

#TODO, tkinter

null_zone = [
    [6, 0, 3],
    [6, 8, 11],
    [9, 0, 3],
    [9, 8, 11]
]

def create_map():
    matrix = alloc_map()
    fill_with_barriers(matrix)
    return matrix

def fill_with_barriers(matrix):
    for row, col, val in positions:
        matrix[row][col] = val

    for row, start_col, end_col in null_zone:
        for col in range(start_col, end_col + 1):
            matrix[row][col] = -1

def alloc_map():
    matrix = []
    for i in range(10):
        aux = []
        for j in range(12):
            aux.append(0)
        matrix.append(aux)
    return matrix

def options(position, qtable):
    return qtable.get(position, []) # return a list dict{key(tuple), value(key(string), value(int))}

def calculate_reward(position, qtable, options_list, propagation):
    value = 0
    max_value = 0
    for option in options_list:
        if option in qtable:
            option_value = qtable.get(option, 0)
            if option_value > max_value:
                max_value = option_value
    value = propagation * position["value"] + max_value
    return value

def run_model(qtable, start, end, propagation):
    position = start
    while True: #TODO, revisar
        options_list = options(position, qtable)
        if not options_list:
            print(f"No options available for position {position}.")
            break
        value = calculate_reward(position, qtable, options_list, propagation)
        qtable.set(position, value)
        
        
        position = options_list[0]
        print(f"Moving to position {position}.")

