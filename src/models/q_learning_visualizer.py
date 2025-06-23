import tkinter as tk
from tkinter import ttk

class QLearningVisualizer:
    def __init__(self, simulator,start,final):
        """
        Visualizador gráfico para o Q-Learning.

        Args:
            simulator (QLearningSimulator): Instância do simulador Q-Learning já configurado.
            start (tuple[int, int]): Posição inicial do agente no ambiente (linha, coluna).
            final (tuple[int, int]): Posição final (objetivo) no ambiente (linha, coluna).
        """
        self.simulator = simulator
        self.rows = len(simulator.matrix)
        self.cols = len(simulator.matrix[0])
        self.cell_size = 40
        self.root = tk.Tk()
        self.root.title("Visualizador Q-Learning")
        self.canvas = tk.Canvas(self.root, width=self.cols * self.cell_size,
                                          height=self.rows * self.cell_size)
        self.canvas.pack()
        frame = ttk.Frame(self.root)
        frame.pack(pady=10)

        self.btn_run = ttk.Button(frame, text="Executar Modelo", command=self.run_simulation)
        self.btn_run.pack(side=tk.LEFT)

        self.episode_label = ttk.Label(frame, text=f"Total de episódios: {self.simulator.episode}")
        self.episode_label.pack(side=tk.LEFT, padx=20)
        self.start = start
        self.end = final
        self.draw_map()

    def draw_map(self):
        """Desenha o ambiente atual na tela."""
        self.canvas.delete("all")
        for i in range(self.rows):
            for j in range(self.cols):
                x1 = j * self.cell_size
                y1 = i * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size

                value = self.simulator.matrix[i][j]
                if (i, j) == self.start:
                    color = "green"
                elif (i, j) == self.end:
                    color = "red"
                elif value is None:
                    color = "gray"
                elif value == -1:
                    color = "black"
                else:
                    color = "white"

                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")

                # Escrever valor da ambient_table (média das direções)
                if (i, j) in self.simulator.ambient_table:
                    avg_value = 0
                    count = 0
                    for val in self.simulator.ambient_table[(i, j)].values():
                        avg_value += val
                        count += 1
                    if count > 0:
                        avg_value /= count
                        self.canvas.create_text(
                            x1 + self.cell_size / 2,
                            y1 + self.cell_size / 2,
                            text=f"{avg_value:.1f}",
                            font=("Arial", 10),
                            fill="black"
                        )

    def draw_ia(self, position):
        x = position[1] * self.cell_size + self.cell_size / 2
        y = position[0] * self.cell_size + self.cell_size / 2
        radius = self.cell_size / 4
        self.canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill="blue")

            
    def run_simulation(self):
        def step_callback(pos):
            self.draw_map()
            self.draw_ia(pos)
            self.root.update()
            self.root.after(1)

        self.simulator.run_model(self.simulator.matrix, step_callback=step_callback)
        self.draw_map()
        self.draw_ia(self.end)
        
        self.episode_label.config(text=f"Total de episódios: {self.simulator.episode}")


    def start_gui(self):
        self.root.mainloop()
        print("end")
