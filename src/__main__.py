from src.models.q_learning_simulator import QLearningSimulator
from src.models.q_learning_visualizer import QLearningVisualizer


def main():
    # Definição das posições com barreiras
    barriers = [
        [0, 4, -1], [0, 11, -1], [1, 1, -1], [1, 11, -1],
        [2, 0, -1], [2, 2, -1], [2, 6, -1], [2, 8, -1],
        [2, 9, -1], [3, 1, -1], [3, 8, -1], [5, 6, -1],
        [8, 6, -1],
    ]

    # Definição das zonas nulas
    null_zone = [
        [6, 0, 3], [6, 8, 11], [7, 0, 3], [7, 8, 11],
        [8, 0, 3], [8, 8, 11], [9, 0, 3], [9, 8, 11]
    ]

    inicial_position = (9, 4)
    final_postion = (5, 11)
    r = 0 # posição atual
    y = 0.5 # propagação
    rows = 10
    cols = 12
    q_learning = QLearningSimulator(rows, cols, barriers, null_zone,y,inicial_position,final_postion)
    q_viz = QLearningVisualizer(q_learning,inicial_position,final_postion)
    q_viz.start_gui()

    #q_learning.run_model(source=matrix, qtable=qtable, start=inicial_position, end=final_postion, propagation=y)

if __name__ == "__main__":
    main()