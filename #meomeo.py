#meomeo
import tkinter as tk
import random
from tkinter import messagebox

class Game2048:
    def __init__(self, root):
        self.root = root
        self.root.title("2048")
        self.root.geometry("400x400")
        self.grid = [[0] * 4 for _ in range(4)]
        self.create_widgets()
        self.add_new_2()
        self.add_new_2()
        self.update_grid_ui()

    def create_widgets(self):
        self.frame = tk.Frame(self.root, bg="#bbada0")
        self.frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        self.tiles = [[tk.Label(self.frame, text="", width=4, height=2, bg="#cdc1b4", font=('Arial', 24, 'bold'), 
                                anchor='center') for _ in range(4)] for _ in range(4)]
        for i in range(4):
            for j in range(4):
                self.tiles[i][j].grid(row=i, column=j, padx=5, pady=5, sticky='nsew')
        for i in range(4):
            self.frame.grid_columnconfigure(i, weight=1)
            self.frame.grid_rowconfigure(i, weight=1)
        self.root.bind("<Key>", self.key_pressed)

    def add_new_2(self):
        empty_cells = [(i, j) for i in range(4) for j in range(4) if self.grid[i][j] == 0]
        if empty_cells:
            i, j = random.choice(empty_cells)
            self.grid[i][j] = 2

    def update_grid_ui(self):
        for i in range(4):
            for j in range(4):
                value = self.grid[i][j]
                color = self.get_color(value)
                text = str(value) if value != 0 else ''
                self.tiles[i][j].config(text=text, bg=color)
                
    def get_color(self, value):
        colors = {
            2: '#fdd0dc', 4: '#fcb3c2', 8: '#f8a2b7',
            16: '#f7819f', 32: '#f76c7c', 64: '#f64d65',
            128: '#f64d6f', 256: '#f65f6f', 512: '#f67272',
            1024: '#f67d7d', 2048: '#f68888'
        }
        return colors.get(value, '#faf8ef')

    def key_pressed(self, event):
        if event.keysym == 'Up':
            self.grid, changed = self.move_up(self.grid)
        elif event.keysym == 'Down':
            self.grid, changed = self.move_down(self.grid)
        elif event.keysym == 'Left':
            self.grid, changed = self.move_left(self.grid)
        elif event.keysym == 'Right':
            self.grid, changed = self.move_right(self.grid)
        else:
            return
        if changed:
            self.add_new_2()
        self.update_grid_ui()
        state = self.get_current_state(self.grid)
        if state == 'WON':
            messagebox.showinfo("2048", "Congratulations! You won!")
            self.root.quit()
        elif state == 'LOST':
            messagebox.showinfo("2048", "Game Over! You lost!")
            self.root.quit()

    def compress(self, mat):
        changed = False
        new_mat = [[0] * 4 for _ in range(4)]
        for i in range(4):
            pos = 0
            for j in range(4):
                if mat[i][j] != 0:
                    new_mat[i][pos] = mat[i][j]
                    if j != pos:
                        changed = True
                    pos += 1
        return new_mat, changed

    def merge(self, mat):
        changed = False
        for i in range(4):
            for j in range(3):
                if mat[i][j] == mat[i][j + 1] and mat[i][j] != 0:
                    mat[i][j] *= 2
                    mat[i][j + 1] = 0
                    changed = True
        return mat, changed

    def reverse(self, mat):
        return [row[::-1] for row in mat]

    def transpose(self, mat):
        return [list(row) for row in zip(*mat)]

    def move_left(self, grid):
        new_grid, changed1 = self.compress(grid)
        new_grid, changed2 = self.merge(new_grid)
        new_grid, _ = self.compress(new_grid)
        return new_grid, changed1 or changed2

    def move_right(self, grid):
        new_grid = self.reverse(grid)
        new_grid, changed = self.move_left(new_grid)
        new_grid = self.reverse(new_grid)
        return new_grid, changed

    def move_up(self, grid):
        new_grid = self.transpose(grid)
        new_grid, changed = self.move_left(new_grid)
        new_grid = self.transpose(new_grid)
        return new_grid, changed

    def move_down(self, grid):
        new_grid = self.transpose(grid)
        new_grid, changed = self.move_right(new_grid)
        new_grid = self.transpose(new_grid)
        return new_grid, changed

    def get_current_state(self, mat):
        for i in range(4):
            for j in range(4):
                if mat[i][j] == 2048:
                    return 'WON'
        for i in range(4):
            for j in range(4):
                if mat[i][j] == 0:
                    return 'GAME NOT OVER'
        for i in range(3):
            for j in range(3):
                if mat[i][j] == mat[i + 1][j] or mat[i][j] == mat[i][j + 1]:
                    return 'GAME NOT OVER'
        for j in range(3):
            if mat[3][j] == mat[3][j + 1]:
                return 'GAME NOT OVER'
        for i in range(3):
            if mat[i][3] == mat[i + 1][3]:
                return 'GAME NOT OVER'
        return 'LOST'

if __name__ == "__main__":
    root = tk.Tk()
    game = Game2048(root)
    root.mainloop()
