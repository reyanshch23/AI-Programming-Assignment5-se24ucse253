# mcts.py
# Monte Carlo Tree Search

import math
import random
import copy
from game import get_empty_cells, check_winner, is_terminal

class Node:
    def __init__(self, board, parent=None, move=None, player='X'):
        self.board = board[:]
        self.parent = parent
        self.move = move          # which cell led to this node
        self.player = player      # whose turn it is at this node
        self.children = []
        self.wins = 0
        self.visits = 0
        self.untried = get_empty_cells(board)

    def is_fully_expanded(self):
        return len(self.untried) == 0

    def ucb1(self, c=1.41):
        if self.visits == 0:
            return float('inf')
        return (self.wins / self.visits) + c * math.sqrt(math.log(self.parent.visits) / self.visits)

    def best_child(self):
        return max(self.children, key=lambda n: n.ucb1())

    def expand(self):
        move = self.untried.pop()
        new_board = self.board[:]
        new_board[move] = self.player
        next_player = 'O' if self.player == 'X' else 'X'
        child = Node(new_board, parent=self, move=move, player=next_player)
        self.children.append(child)
        return child

def simulate(board, current_player):
    # random rollout from this point
    b = board[:]
    p = current_player
    while not is_terminal(b):
        moves = get_empty_cells(b)
        if not moves:
            break
        b[random.choice(moves)] = p
        p = 'O' if p == 'X' else 'X'
    winner = check_winner(b)
    if winner == 'X':
        return 1
    elif winner == 'O':
        return -1
    return 0

def backprop(node, result):
    while node is not None:
        node.visits += 1
        # from X's perspective
        if node.player == 'O':  # this node was made by X
            node.wins += result
        else:
            node.wins -= result
        node = node.parent

def mcts(board, iterations=1000):
    root = Node(board, player='X')

    for _ in range(iterations):
        node = root

        # selection
        while node.is_fully_expanded() and node.children:
            node = node.best_child()

        # expansion
        if not is_terminal(node.board) and not node.is_fully_expanded():
            node = node.expand()

        # simulation
        result = simulate(node.board, node.player)

        # backpropagation
        backprop(node, result)

    # pick child with most visits
    best = max(root.children, key=lambda n: n.visits)
    print(f"[MCTS, {iterations} iters] Best move: {best.move}, visits: {best.visits}, wins: {best.wins}")
    return best.move