import tkinter as tk
from tkinter import ttk

class QLearningVisualizer:
    def __init__(self, simulator,start,final):
        self.simulator = simulator
        self.rows = len(simulator.matrix)
        self.cols = len(simulator.matrix[0])
        self.cell_size = 40
        self.root = tk.Tk()
        self.root.title("Visualizador Q-Learning")
        self.canvas = tk.Canvas(self.root, width=self.cols * self.cell_size,
                                          height=self.rows * self.cell_size)
        self.canvas.pack()
        self.btn_run = ttk.Button(self.root, text="Executar Modelo", command=self.run_simulation)
        self.btn_run.pack(pady=10)
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
        self.simulator.run_model(self.simulator.matrix)
        self.draw_map()
        self.draw_ia(self.end)


    def start_gui(self):
        self.root.mainloop()
