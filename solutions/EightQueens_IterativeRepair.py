# Eight Queens - Iterative repair with min-conflicts heuristic (hill-climbing)
# Unlike DF Backtracking approach, this does not guarantee a solution, as it may get stuck in a local optimum
#   -> in which case, restart with a different initial configuration
#   -> However, this heuristic-based approach does often solve the big cases quickly

import sys
from random import shuffle, randrange


class EightQueensSolver:
    def __init__(self, n=8):
        self.n = n
        self.queen_positions = {}
        for i in range(0, self.n):
            self.queen_positions.update({i: (randrange(0,self.n), i)})
        self.board = [[0 for count in range(self.n)] for count in range(self.n)]
        for queen_pos in self.queen_positions.values():
            self.calculate_conflicts(queen_pos, operand=1)
        # print("Initial board", self.board)
        print("Initial queen positions", self.queen_positions)

    def calculate_conflicts(self, queen_pos, operand):
        row_num = queen_pos[0]
        col_num = queen_pos[1]
        for i in range(0, self.n):  # mark column
            if i != row_num:
                self.board[i][col_num] += operand
        for i in range(0, self.n):  # mark row
            if i != col_num:
                self.board[row_num][i] += operand
        for i in range(1, self.n):  # mark bottom-right diagonal
            if row_num + i < self.n and col_num + i < self.n:
                self.board[row_num + i][col_num + i] += operand
        for i in range(1, self.n):  # mark bottom-left diagonal
            if row_num + i < self.n and col_num - i >= 0:
                self.board[row_num + i][col_num - i] += operand
        for i in range(1, self.n):  # mark top-left diagonal
            if row_num - i >= 0 and col_num - i >= 0:
                self.board[row_num - i][col_num - i] += operand
        for i in range(1, self.n):  # mark top-right diagonal
            if row_num - i >= 0 and col_num + i < self.n:
                self.board[row_num - i][col_num + i] += operand

    def is_solution(self):
        for queen_pos in self.queen_positions.values():
            if self.board[queen_pos[0]][queen_pos[1]] > 0:
                return False
        return True

    def find_most_conflicted_queen(self):
        most_conflicted = None
        max_conflicts = 0
        qps = list(self.queen_positions.items())
        shuffle(qps)
        for (queen, queen_pos) in qps:
            conflicts = self.board[queen_pos[0]][queen_pos[1]]
            if conflicts > max_conflicts:
                max_conflicts = conflicts
                most_conflicted = queen
        return most_conflicted

    def find_least_conflicted_square_in_column(self, column):
        min_conflicts = sys.maxsize
        min_conflicted_row_num = None
        for row in range(0,self.n):
            value = self.board[row][column]
            unoccupied_cell = (row,column) not in self.queen_positions.values()
            if (value < min_conflicts) and unoccupied_cell:
                min_conflicts = value
                min_conflicted_row_num = row
        return min_conflicted_row_num

    def move_to_least_conflicted_square_in_column(self, queen):
        original_position = self.queen_positions.get(queen)
        row_num = self.find_least_conflicted_square_in_column(original_position[1])
        self.calculate_conflicts(original_position, operand=-1)
        new_position = (row_num, original_position[1])
        self.queen_positions.update({queen: new_position})
        self.calculate_conflicts(new_position, operand=1)

    def solve(self, timeout):
        iterations = 0
        while not self.is_solution():
            if iterations == timeout:
                return (False, iterations)
            most_conflicted_queen = self.find_most_conflicted_queen()
            self.move_to_least_conflicted_square_in_column(most_conflicted_queen)
            iterations += 1
        return True, iterations


solver = EightQueensSolver(8)
solved, iterations = solver.solve(timeout=100000)
if solved:
    print("Found a solution in", iterations, "iterations.")
    print("Queen positions:", solver.queen_positions)
    # print("Board:", solver.board)
else:
    print("Failed to solve. 'Timed out' after", iterations, "iterations")
    print("Board with last conflict counts:", solver.board)
    # print("Queens", solver.queen_positions)