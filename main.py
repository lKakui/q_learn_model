import matriz as m

inicial_position = {
    (9, 4): {
        "up": 0,
        "down": 0,
        "left": 0,
        "right": 0,
        "value": 0
    }
}
final_postion = {
    (5, 11): {
        "up": 0,
        "down": 0,
        "left": 0,
        "right": 0,
        "value": 0
    }
}
r = 0 # posição atual
y = 0.5 # propagação


#qtable = dict{key(tuple), value{dict{key(string), value(int)}}} 


def main():
    matrix = m.create_map()

    m.run_model(source=matrix, qtable=qtable, start=inicial_position, end=final_postion, propagation=y)

