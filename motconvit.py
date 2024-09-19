import tkinter as tk
import random
from tkinter import messagebox

class Game2048:
    def __init__(self, root):
        self.root = root
        self.root.title("Game 2048 Hahiduong vs anchuu")
        self.grid_size = 4
        self.grid = [[0] * self.grid_size for _ in range(self.grid_size)]
        self.score = 0
        self.high_score = 0
        self.setup_ui()
        self.start_game()

    def setup_ui(self):
        self.frame = tk.Frame(self.root)
        self.frame.grid()
        
        self.score_label = tk.Label(self.frame, text="Score: 0", font=("Arial", 14))
        self.score_label.grid(row=0, column=0, columnspan=self.grid_size, pady=10)
        
        self.high_score_label = tk.Label(self.frame, text="High Score: 0", font=("Arial", 14))
        self.high_score_label.grid(row=1, column=0, columnspan=self.grid_size, pady=5)
        
        self.cells = [[tk.Label(self.frame, text="", width=4, height=2, borderwidth=1, relief="solid")
                      for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        for r in range(self.grid_size):
            for c in range(self.grid_size):
                self.cells[r][c].grid(row=r + 2, column=c, padx=5, pady=5)

        self.update_ui()
        self.root.bind("<Key>", self.key_press)

    def start_game(self):
        self.grid = [[0] * self.grid_size for _ in range(self.grid_size)]
        self.score = 0
        self.add_random_tile()
        self.add_random_tile()
        self.update_ui()

    def add_random_tile(self):
        empty_cells = [(r, c) for r in range(self.grid_size) for c in range(self.grid_size) if self.grid[r][c] == 0]
        if empty_cells:
            r, c = random.choice(empty_cells)
            self.grid[r][c] = 2 if random.random() < 0.9 else 4

    def update_ui(self):
        for r in range(self.grid_size):
            for c in range(self.grid_size):
                value = self.grid[r][c]
                self.cells[r][c].config(text=str(value) if value else "", bg=self.get_color(value))
        
        self.score_label.config(text=f"Score: {self.score}")
        self.high_score_label.config(text=f"High Score: {self.high_score}")

    def get_color(self, value):
        colors = {
            2: "#eee4da", 4: "#ede0c8", 8: "#f2b179", 16: "#f59563",
            32: "#f67c5f", 64: "#f65e3b", 128: "#edcf72", 256: "#edcc61",
            512: "#edc850", 1024: "#edc53f", 2048: "#edc22e"
        }
        return colors.get(value, "#cdc1b4")

    def key_press(self, event):
        moved = False
        if event.keysym == 'Up':
            moved = self.move_up()
        elif event.keysym == 'Down':
            moved = self.move_down()
        elif event.keysym == 'Left':
            moved = self.move_left()
        elif event.keysym == 'Right':
            moved = self.move_right()

        if moved:
            self.add_random_tile()
            self.update_ui()
            if not self.can_move():
                self.show_game_over()

    def move_up(self):
        moved = False
        for c in range(self.grid_size):
            column = [self.grid[r][c] for r in range(self.grid_size)]
            new_column, column_moved = self.merge_list(column)
            if column_moved:
                moved = True
            for r in range(self.grid_size):
                self.grid[r][c] = new_column[r]
        return moved

    def move_down(self):
        moved = False
        for c in range(self.grid_size):
            column = [self.grid[r][c] for r in range(self.grid_size)]
            new_column, column_moved = self.merge_list(column[::-1])
            if column_moved:
                moved = True
            for r in range(self.grid_size):
                self.grid[r][c] = new_column[::-1][r]
        return moved

    def move_left(self):
        moved = False
        for r in range(self.grid_size):
            row = self.grid[r]
            new_row, row_moved = self.merge_list(row)
            if row_moved:
                moved = True
            self.grid[r] = new_row
        return moved

    def move_right(self):
        moved = False
        for r in range(self.grid_size):
            row = self.grid[r]
            new_row, row_moved = self.merge_list(row[::-1])
            if row_moved:
                moved = True
            self.grid[r] = new_row[::-1]
        return moved

    def merge_list(self, lst):
        new_list = [0] * self.grid_size
        last = -1
        pos = 0
        moved = False
        for i in range(self.grid_size):
            if lst[i] != 0:
                if last == lst[i]:
                    new_list[pos - 1] *= 2
                    self.score += new_list[pos - 1]
                    last = -1
                    moved = True
                else:
                    new_list[pos] = lst[i]
                    last = lst[i]
                    pos += 1
        return new_list, moved

    def can_move(self):
        for r in range(self.grid_size):
            for c in range(self.grid_size):
                if self.grid[r][c] == 0:
                    return True
                if c < self.grid_size - 1 and self.grid[r][c] == self.grid[r][c + 1]:
                    return True
                if r < self.grid_size - 1 and self.grid[r][c] == self.grid[r + 1][c]:
                    return True
        return False

    def show_game_over(self):
        if self.score > self.high_score:
            self.high_score = self.score
        messagebox.showinfo("Game Over", f"Game Over! Your score is {self.score}")
        self.start_game()

if __name__ == "__main__":
    root = tk.Tk()
    game = Game2048(root)
    root.mainloop()

