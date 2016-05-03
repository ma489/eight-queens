# Eight Queens - Simulated Annealing


from random import randrange, random

import math


class EightQueensSolver:
    def __init__(self, n=8):
        self.n = n
        self.queen_positions = {}
        for i in range(0, self.n):
            self.queen_positions.update({i: (randrange(0,self.n), i)})
        self.board = [[0 for count in range(self.n)] for count in range(self.n)]
        for queen_pos in self.queen_positions.values():
            self.calculate_conflicts(queen_pos, operand=1)
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

    def evaluate(self):
        total_conflicts = 0
        for (queen, queen_pos) in self.queen_positions.items():
            conflicts = self.board[queen_pos[0]][queen_pos[1]]
            total_conflicts += conflicts
        return total_conflicts

    def try_new_configuration(self):
        random_queen = randrange(0, self.n)
        old_pos = self.queen_positions.get(random_queen)
        self.calculate_conflicts(old_pos, -1)
        new_pos = (randrange(0,self.n), randrange(0,self.n))
        while new_pos in self.queen_positions.values():
            new_pos = (randrange(0, self.n), randrange(0, self.n))
        self.queen_positions.update({random_queen: new_pos})
        self.calculate_conflicts(new_pos, 1)
        return random_queen, old_pos, new_pos

    def revert_state(self, random_queen, old_pos, new_pos):
        self.calculate_conflicts(new_pos, -1)
        self.queen_positions.update({random_queen: old_pos})
        self.calculate_conflicts(old_pos, 1)
        pass

    def solve(self, timeout, starting_temperature, cooling_factor):
        t = 0
        temperature = starting_temperature
        while not self.is_solution():
            self.progress(t, timeout)
            if t == timeout:
                return (False, t)
            temperature = temperature - cooling_factor #stabilizing factor?
            if temperature == 0:
                return False, t
            current_value = self.evaluate()
            random_queen, old_pos, new_pos = self.try_new_configuration()
            new_value = self.evaluate()
            delta = new_value - current_value
            probability = math.exp(-delta / temperature)
            acceptable_solution = (delta < 0) or (probability > random())
            if not acceptable_solution:
                self.revert_state(random_queen, old_pos, new_pos)
            t += 1
        return True, t

    def progress(self, t, timeout):
        if t == timeout / 20:
            print("5%")
        elif t == timeout / 10:
            print("10%")
        elif t == timeout/4:
            print("25%")
        elif t == timeout / 2:
            print("50%")
        elif t == (timeout / 4)*3:
            print("75%")


# solver = EightQueensSolver(4) ✓
# solver = EightQueensSolver(5) ✓
# solver = EightQueensSolver(6) ✓
# solver = EightQueensSolver(7) ✓
solver = EightQueensSolver(8) # ! Found a solution in 6,920,787 iterations
solved, iterations = solver.solve(timeout=100000000, starting_temperature=35000, cooling_factor=0.05)
if solved:
    print("Found a solution in", iterations, "iterations.")
    print("Queen positions:", solver.queen_positions)
else:
    print("Failed to solve. 'Timed out' after", iterations, "iterations")
    print("Board with last conflict counts:", solver.board)
