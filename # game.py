# game.py
# Tic-Tac-Toe board logic shared by all algorithms

import math
import random
import copy
import time

def make_board():
    return [' '] * 9

def print_board(board):
    print()
    for i in range(0, 9, 3):
        print(f" {board[i]} | {board[i+1]} | {board[i+2]} ")
        if i < 6:
            print("---|---|---")
    print()

def get_empty_cells(board):
    return [i for i, v in enumerate(board) if v == ' ']

def check_winner(board):
    wins = [
        (0,1,2),(3,4,5),(6,7,8),  # rows
        (0,3,6),(1,4,7),(2,5,8),  # cols
        (0,4,8),(2,4,6)           # diagonals
    ]
    for a, b, c in wins:
        if board[a] == board[b] == board[c] != ' ':
            return board[a]
    return None

def is_terminal(board):
    return check_winner(board) is not None or ' ' not in boardpython test_algorithms.py