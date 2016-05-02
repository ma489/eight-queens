# Eight Queens - Depth-first backtracking

import copy

configurations = 0

def solve_eight_queens():
    n = 8
    row_num = 0
    initial_board = get_board_of_size_n(n)
    global configurations
    configurations = 0
    return solve(n, row_num, initial_board)

def solve(n, row_num, board):
    if row_num >= n - 1:
        last_spots = get_possibilities_from_row(board[row_num])
        if last_spots:
            last_remaining_spot = last_spots[0]
            board[row_num][last_remaining_spot] = "Que"
            print_board(board) # this should be a successful board
            global configurations
            configurations += 1
        return None
    row = board[row_num]
    possible_columns = get_possibilities_from_row(row)
    for col_num in possible_columns:
        tentative_board = replicate_board_with_focus_and_consequences_marked(board, row_num, col_num)
        solve(n, row_num + 1, tentative_board)


def get_possibilities_from_row(row):
    possibilities = []
    for i in range(0, len(row)):
        if row[i] != False and row[i] != "Que":
            possibilities.append(i)
    return possibilities


def replicate_board_with_focus_and_consequences_marked(board, row_num, col_num):
    new_board = copy.deepcopy(board)
    new_board[row_num][col_num] = "Que"
    # Mark anything in the path of new_board[row_num][col_num]
    n = len(board)
    for i in range(0, n):  # mark column
        if i != row_num:
            new_board[i][col_num] = False
    for i in range(0, n):  # mark row
        if i != col_num:
            new_board[row_num][i] = False
    for i in range(1, n):  # mark bottom-right diagonal
        if row_num + i < n and col_num + i < n:
            new_board[row_num + i][col_num + i] = False
    for i in range(1, n):  # mark bottom-left diagonal
        if row_num + i < n and col_num - i >= 0:
            new_board[row_num + i][col_num - i] = False
    for i in range(1, n):  # mark top-left diagonal
        if row_num - i >= 0 and col_num - i >= 0:
            new_board[row_num - i][col_num - i] = False
    for i in range(1, n):  # mark top-right diagonal
        if row_num - i >= 0 and col_num + i < n:
            new_board[row_num - i][col_num + i] = False
    return new_board


def get_board_of_size_n(n):
    return [[True for count in range(n)] for count in range(n)]


def print_board(board):
    if board is not None:
        print()
        print("--- BOARD ---")
        print()
        if not board:
            print([])
        else:
            print(" ---------------¬")
            for row in board:
                row_print = "["
                for cell in row:
                    if not cell:
                        cell_print = "_"
                    else:
                        cell_print = "Q"
                    row_print += str(cell_print) + "|"
                print(row_print + "]")


boards = solve_eight_queens()
print(configurations, "configurations")
