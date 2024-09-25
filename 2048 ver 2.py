import tkinter as tk
import random
from tkinter import messagebox

# Lớp Tile đại diện cho từng ô trên bảng
class Tile:
    def __init__(self, value=0):
        self.value = value

    def set_value(self, value):
        self.value = value

    def get_value(self):
        return self.value


# Lớp Board xử lý các thao tác trên bảng 2048
class Board:
    def __init__(self):
        self.grid = [[Tile() for _ in range(4)] for _ in range(4)]
        self.add_new_tile()
        self.add_new_tile()

    def add_new_tile(self):
        empty_cells = [(i, j) for i in range(4) for j in range(4) if self.grid[i][j].get_value() == 0]
        if empty_cells:
            i, j = random.choice(empty_cells)
            self.grid[i][j].set_value(2)

    def get_grid_values(self):
        return [[self.grid[i][j].get_value() for j in range(4)] for i in range(4)]

    def compress(self):
        changed = False
        new_grid = [[Tile() for _ in range(4)] for _ in range(4)]
        for i in range(4):
            pos = 0
            for j in range(4):
                if self.grid[i][j].get_value() != 0:
                    new_grid[i][pos].set_value(self.grid[i][j].get_value())
                    if j != pos:
                        changed = True
                    pos += 1
        self.grid = new_grid
        return changed

    def merge(self):
        changed = False
        for i in range(4):
            for j in range(3):
                if self.grid[i][j].get_value() == self.grid[i][j + 1].get_value() and self.grid[i][j].get_value() != 0:
                    self.grid[i][j].set_value(self.grid[i][j].get_value() * 2)
                    self.grid[i][j + 1].set_value(0)
                    changed = True
        return changed

    def reverse(self):
        for i in range(4):
            self.grid[i] = self.grid[i][::-1]

    def transpose(self):
        self.grid = [list(row) for row in zip(*self.grid)]

    def move_left(self):
        changed1 = self.compress()
        changed2 = self.merge()
        self.compress()
        return changed1 or changed2

    def move_right(self):
        self.reverse()
        changed = self.move_left()
        self.reverse()
        return changed

    def move_up(self):
        self.transpose()
        changed = self.move_left()
        self.transpose()
        return changed

    def move_down(self):
        self.transpose()
        changed = self.move_right()
        self.transpose()
        return changed

    def check_state(self):
        for i in range(4):
            for j in range(4):
                if self.grid[i][j].get_value() == 2048:
                    return 'WON'
        for i in range(4):
            for j in range(4):
                if self.grid[i][j].get_value() == 0:
                    return 'GAME NOT OVER'
        for i in range(3):
            for j in range(3):
                if self.grid[i][j].get_value() == self.grid[i + 1][j].get_value() or self.grid[i][j].get_value() == self.grid[i][j + 1].get_value():
                    return 'GAME NOT OVER'
        for j in range(3):
            if self.grid[3][j].get_value() == self.grid[3][j + 1].get_value():
                return 'GAME NOT OVER'
        for i in range(3):
            if self.grid[i][3].get_value() == self.grid[i + 1][3].get_value():
                return 'GAME NOT OVER'
        return 'LOST'


# Lớp Game2048 quản lý giao diện và luồng trò chơi
class Game2048:
    def __init__(self, root):
        self.root = root
        self.root.title("2048")
        self.root.geometry("400x400")
        self.board = Board()
        self.create_widgets()
        self.update_grid_ui()

    def create_widgets(self):
        self.frame = tk.Frame(self.root, bg="#bbada0")
        self.frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        self.tiles = [[tk.Label(self.frame, text="", width=4, height=2, bg="#cdc1b4", font=('Arial', 24, 'bold'), anchor='center') for _ in range(4)] for _ in range(4)]
        for i in range(4):
            for j in range(4):
                self.tiles[i][j].grid(row=i, column=j, padx=5, pady=5, sticky='nsew')
        for i in range(4):
            self.frame.grid_columnconfigure(i, weight=1)
            self.frame.grid_rowconfigure(i, weight=1)
        self.root.bind("<Key>", self.key_pressed)

    def update_grid_ui(self):
        grid_values = self.board.get_grid_values()
        for i in range(4):
            for j in range(4):
                value = grid_values[i][j]
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
            changed = self.board.move_up()
        elif event.keysym == 'Down':
            changed = self.board.move_down()
        elif event.keysym == 'Left':
            changed = self.board.move_left()
        elif event.keysym == 'Right':
            changed = self.board.move_right()
        else:
            return
        if changed:
            self.board.add_new_tile()
        self.update_grid_ui()
        state = self.board.check_state()
        if state == 'WON':
            messagebox.showinfo("2048", "Chúc mừng! Bạn đã thắng!")
            self.root.quit()
        elif state == 'LOST':
            messagebox.showinfo("2048", "Game Over! Bạn đã thua!")
            self.root.quit()


if __name__ == "__main__":
    root = tk.Tk()
    game = Game2048(root)
    root.mainloop()
