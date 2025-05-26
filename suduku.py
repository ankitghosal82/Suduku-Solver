import random
import copy

class SudokuSolver:
    def __init__(self, board):
        self.board = board
        self.steps = []
        self.recursive_calls = 0
        self.backtracks = 0

    def is_valid(self, num, row, col):
        for i in range(9):
            if self.board[row][i] == num or self.board[i][col] == num:
                return False
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(3):
            for j in range(3):
                if self.board[start_row + i][start_col + j] == num:
                    return False
        return True

    def solve(self):
        self.recursive_calls += 1
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0:
                    for num in range(1, 10):
                        if self.is_valid(num, i, j):
                            self.board[i][j] = num
                            self.steps.append(copy.deepcopy(self.board))
                            if self.solve():
                                return True
                            self.board[i][j] = 0
                            self.backtracks += 1
                    return False
        return True

def generate_full_board():
    board = [[0 for _ in range(9)] for _ in range(9)]
    solver = SudokuSolver(board)
    nums = list(range(1, 10))
    for i in range(9):
        for j in range(9):
            random.shuffle(nums)
            for num in nums:
                if solver.is_valid(num, i, j):
                    board[i][j] = num
                    if SudokuSolver(copy.deepcopy(board)).solve():
                        break
                    board[i][j] = 0
            if board[i][j] == 0:
                return generate_full_board()
    return board

def remove_cells(board, difficulty="easy"):
    difficulty_map = {
        "easy": 35,
        "medium": 45,
        "hard": 55
    }
    cells_to_remove = difficulty_map.get(difficulty, 35)
    puzzle = copy.deepcopy(board)
    removed = 0
    while removed < cells_to_remove:
        i = random.randint(0, 8)
        j = random.randint(0, 8)
        if puzzle[i][j] != 0:
            puzzle[i][j] = 0
            removed += 1
    return puzzle

def estimate_difficulty(steps_count):
    if steps_count < 50:
        return "Easy"
    elif steps_count < 150:
        return "Medium"
    else:
        return "Hard"
