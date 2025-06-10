import matriz as m

inicial_position = (9, 4)
final_postion = (5, 11)
r = 0 # posição atual
y = 0.5 # propagação

def main():
    matrix = m.create_map()
    qtable = m.create_table(matrix)

    m.run_model(source=matrix, qtable=qtable, start=inicial_position, end=final_postion, propagation=y)

