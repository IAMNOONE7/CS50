"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    x_count = sum(cell == X for row in board for cell in row)
    o_count = sum(cell == O for row in board for cell in row)
    return X if x_count == o_count else O

def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    _actions = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] is EMPTY:
                _actions.add((i,j))
    return _actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if action is None:
        raise Exception("Action cannot be None.")
    (i,j) = action
    if not (0<= i <3 and 0<=j<3):
        raise Exception("Action out of bounds")
    if terminal(board):
        raise Exception("Game is already over")
    if board[i][j] is not EMPTY:
        raise Exception("Cell is not empty")

    copy_board = copy.deepcopy(board)
    copy_board[i][j] = player(board)
    return copy_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    lines=[]

    for x in range(3):
        lines.append(board[x])
        lines.append([board[0][x], board[1][x], board[2][x]])

    lines.append([board[0][0], board[1][1], board[2][2]])
    lines.append([board[0][2], board[1][1], board[2][0]])

    for line in lines:
        if line[0] is not EMPTY and line.count(line[0]) == 3:
            return line[0]
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) is not None:
        return True

    return not any(cell is EMPTY for row in board for cell in row)



def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    w = winner(board)
    if w == X:
        return 1
    if w == O:
        return -1
    return 0

def board_key(board):
    return tuple(tuple(row) for row in board)

_minimax_cache={}


def max_value(board):
    key = (board_key(board), "MAX")
    if key in _minimax_cache:
        return _minimax_cache[key]

    if terminal(board):
        val = utility(board)
        _minimax_cache[key] = (val, None)
        return val, None

    v = -math.inf
    best_action = None
    for a in actions(board):
        mv, _ = min_value(result(board,a))
        if mv > v:
            v = mv
            best_action = a
            if v == 1:
                break

    _minimax_cache[key] = (v,best_action)
    return v, best_action

def min_value(board):
    key = (board_key(board), "MIN")
    if key in _minimax_cache:
        return _minimax_cache[key]

    if terminal(board):
        val = utility(board)
        _minimax_cache[key] = (val, None)
        return val, None

    v = math.inf
    best_action = None
    for a in actions(board):
        mv, _ = max_value(result(board,a))
        if mv < v:
            v = mv
            best_action = a
            if v == -1:
                break

    _minimax_cache[key] = (v,best_action)
    return v, best_action


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None

    turn = player(board)

    if turn == X:
        _,act = max_value(board)

    else:
        _,act = min_value(board)
        
    return act


