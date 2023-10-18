import tkinter as tk
import random

class TetrisGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Tetris")

        self.canvas = tk.Canvas(root, width=300, height=600, bg='black')
        self.canvas.pack()

        self.board = [[0] * 10 for _ in range(20)]

        self.current_piece = None
        self.spawn_piece()

        self.root.bind("<Left>", self.move_left)
        self.root.bind("<Right>", self.move_right)
        self.root.bind("<Down>", self.move_down)

        self.update()

    def draw_board(self):
        self.canvas.delete("all")
        for row in range(20):
            for col in range(10):
                if self.board[row][col]:
                    self.canvas.create_rectangle(col * 30, row * 30, (col + 1) * 30, (row + 1) * 30, fill='cyan')

    def spawn_piece(self):
        self.current_piece = Tetromino()
        self.current_piece.x = 4
        self.current_piece.y = 0

    def move_left(self, event):
        self.current_piece.move(-1, 0, self.board)
        self.draw_board()

    def move_right(self, event):
        self.current_piece.move(1, 0, self.board)
        self.draw_board()

    def move_down(self, event):
        if not self.current_piece.move(0, 1, self.board):
            self.merge_piece()
            self.spawn_piece()
        self.draw_board()

    def merge_piece(self):
        for row in range(4):
            for col in range(4):
                if self.current_piece.shape[row][col]:
                    self.board[self.current_piece.y + row][self.current_piece.x + col] = 1

    def update(self):
        self.move_down(None)
        self.root.after(500, self.update)

class Tetromino:
    shapes = [
        [[1, 1, 1, 1]],
        [[1, 1], [1, 1]],
        [[1, 1, 0], [0, 1, 1]],
        [[0, 1, 1], [1, 1, 0]],
        [[1, 1, 1], [0, 1, 0]],
        [[1, 1, 1], [1, 0, 0]],
        [[1, 1, 1], [0, 0, 1]]
    ]

    def __init__(self):
        self.shape = random.choice(self.shapes)
        self.x = 0
        self.y = 0

    def move(self, dx, dy, board):
        new_x = self.x + dx
        new_y = self.y + dy
        if self.valid_position(new_x, new_y, board):
            self.x = new_x
            self.y = new_y
            return True
        return False

    def valid_position(self, x, y, board):
        for row in range(len(self.shape)):
            for col in range(len(self.shape[row])):
                if self.shape[row][col]:
                    if x + col < 0 or x + col >= 10 or y + row >= 20 or board[y + row][x + col]:
                        return False
        return True

root = tk.Tk()
game = TetrisGame(root)
root.mainloop()
