import random

class QLearningSimulator:
    def __init__(
        self,
        rows: int,
        cols: int,
        barriers: list[list[int]],
        null_zone: list[list[int]],
        propagation: float,
        start: tuple[int,int],
        end: tuple[int,int]
    ):
        """
        Inicializa o simulador Q-Learning.

        Args:
            rows (int): Número de linhas do ambiente.
            cols (int): Número de colunas do ambiente.
            barriers (list[list[int]]): Lista de barreiras no formato [linha, coluna, valor].
            null_zone (list[list[int]]): Zonas nulas onde não é possível passar, formato [linha, coluna_inicial, coluna_final].
            propagation (float): Fator de propagação para o cálculo de recompensa.
        """
        self.barriers = barriers
        self.null_zone = null_zone
        self.matrix = self.create_map(rows, cols)
        self.propagation = propagation
        self.start = start
        self.end = end
        self.q_table = {}
        self.ambient_table = {}

    def create_table(self, mat: list[list[int]]) -> tuple[dict, dict]:
        """
        Cria a Q-table e a tabela de ambiente.

        Args:
            mat (list): Matriz representando o ambiente.

        Formato:
            q_table: dicionário no formato {(i, j): {"up": 0, "left": 0, "right": 0, "down": 0}}
            ambient_table: dicionário no formato {(i, j): {(x, y): 0}}
        """
        for i in range(len(mat)):
            for j in range(len(mat[0])):
                if mat[i][j] is not None:
                    self.q_table[(i, j)] = {"up": 0, "left": 0, "right": 0, "down": 0}
                    self.ambient_table[(i, j)] = {}
                    if i > 0 and mat[i - 1][j] is not None:
                        self.q_table[(i, j)]["up"] = 1
                        self.ambient_table[(i, j)][(i - 1, j)] = 0
                    if j > 0 and mat[i][j - 1] is not None:
                        self.q_table[(i, j)]["left"] = 1
                        self.ambient_table[(i, j)][(i, j - 1)] = 0
                    if i < len(mat) - 1 and mat[i + 1][j] is not None:
                        self.q_table[(i, j)]["down"] = 1
                        self.ambient_table[(i, j)][(i + 1, j)] = 0
                    if j < len(mat[0]) - 1 and mat[i][j + 1] is not None:
                        self.q_table[(i, j)]["right"] = 1
                        self.ambient_table[(i, j)][(i, j + 1)] = 0

    def create_map(self, rows: int, cols: int) -> list[list[int]]:
        """
        Cria o mapa do ambiente com as barreiras e zonas nulas.

        Args:
            rows (int): Número de linhas.
            cols (int): Número de colunas.

        Returns:
            list[list[int]]: Matriz do ambiente.
        """
        matrix = self.alloc_map(rows, cols)
        matrix = self.fill_with_barriers(matrix)
        return matrix

    def fill_with_barriers(self, matrix):
        """
        Preenche a matriz com as barreiras e zonas nulas.
        """
        for row, col, val in self.barriers:
            matrix[row][col] = val

        for row, start_col, end_col in self.null_zone:
            for col in range(start_col, end_col + 1):
                matrix[row][col] = None
        
        return matrix

    def alloc_map(self, rows: int, cols: int) -> list[list[int]]:
        """
        Aloca uma matriz com os valores iniciais.

        Args:
            rows (int): Número de linhas.
            cols (int): Número de colunas.

        Returns:
            list[list[int]]: Matriz preenchida com zeros.
        """
        return [[0 for _ in range(cols)] for _ in range(rows)]

    def options(self, position: tuple[int, int]) -> list[tuple[int, int]]:
        """
        Retorna as opções de movimento a partir de uma posição.

        Args:
            position (tuple[int, int]): Posição atual.

        Returns:
            list[tuple[int, int]]: Lista de posições vizinhas acessíveis.
        """
        options_list = []
        qtable_entry = self.q_table.get(position, {})
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
            print(f"Nenhuma opção disponível para a posição {position}.")

        return options_list

    def calculate_reward(
        self,
        position: tuple[int, int],
        options_list: list[tuple[int, int]],
        map: list[list[int]]
    ) -> float:
        """
        Calcula a recompensa de uma posição com base em suas opções.

        Args:
            position (tuple[int, int]): Posição atual.
            options_list (list[tuple[int, int]]): Vizinhos acessíveis.
            map (list[list[int]]): Mapa do ambiente.

        Returns:
            float: Valor da recompensa.
        """
        max_value = 0
        for option in options_list:
            option_value = map[option[0]][option[1]]
            if option_value > max_value:
                max_value = option_value

        return self.propagation * map[position[0]][position[1]] + max_value

    def is_qtable_stable(self, previous_qtable: dict, threshold: float = 0.01) -> bool:
        """
        Verifica se a Q-table está estável.

        Args:
            previous_qtable (dict): Q-table da iteração anterior.
            threshold (float, optional): Limite de variação aceitável. Padrão é 0.01.

        Returns:
            bool: Verdadeiro se está estável, falso caso contrário.
        """
        for position in self.q_table:
            for direction in self.q_table[position]:
                current_value = self.q_table[position][direction]
                previous_value = previous_qtable.get(position, {}).get(direction, 0)
                if abs(current_value - previous_value) > threshold:
                    return False
        return True

    def run_model(
        self,
        map: list[list[int]]
    ):
        """
        Executa o modelo Q-Learning até a convergência da Q-table.

        Args:
            map (list[list[int]]): Mapa do ambiente.
            start (tuple[int, int]): Posição inicial.
            end (tuple[int, int]): Posição final.
        """
        position = self.start
        previous_qtable = {}

        while True:
            if self.is_qtable_stable(self.q_table, previous_qtable):
                print("A Q-table estabilizou. Encerrando execução.")
                break

            previous_qtable = {pos: self.q_table[pos].copy() for pos in self.q_table}

            while position != self.end:
                options_list = self.options(position)
                if not options_list:
                    print(f"Nenhuma opção disponível para a posição {position}.")
                    break

                if random.random() < 0.3:
                    next_position = random.choice(options_list)
                else:
                    next_position = max(options_list, key=lambda opt: map[opt[0]][opt[1]])

                reward = self.calculate_reward(position, options_list, map)

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
                    self.q_table[position][direction] = reward
                    
                if next_position in self.ambient_table[position]:
                    self.ambient_table[position][next_position] = reward

                position = next_position

            position = self.start
