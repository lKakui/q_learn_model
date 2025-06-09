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
    [4, 11, 100],
    [5, 6, -1],
    [8, 6, -1],
]

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
    for pos in positions:
        row, col, val = pos
        matrix[row][col] = val

    for area in null_zone:
        row = area[0]
        start_col = area[1]
        end_col = area[2]

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


