# heuristic_ab.py
from game import get_empty_cells, check_winner, is_terminal

call_count = 0
def heuristic_eval(board):
    lines = [
        (0,1,2),(3,4,5),(6,7,8),
        (0,3,6),(1,4,7),(2,5,8),
        (0,4,8),(2,4,6)
    ]
    score = 0
    for a, b, c in lines:
        row = [board[a], board[b], board[c]]
        x_count = row.count('X')
        o_count = row.count('O')
        if o_count == 0:
            score += x_count  
        if x_count == 0:
            score -= o_count  
    return score

def heuristic_ab(board, depth, is_maximizing, alpha, beta, max_depth):
    global call_count
    call_count += 1

    winner = check_winner(board)
    if winner == 'X':
        return 100
    if winner == 'O':
        return -100
    if ' ' not in board:
        return 0
    if depth >= max_depth:
        return heuristic_eval(board)  

    empty = get_empty_cells(board)

    if is_maximizing:
        best = -999
        for cell in empty:
            board[cell] = 'X'
            score = heuristic_ab(board, depth+1, False, alpha, beta, max_depth)
            board[cell] = ' '
            best = max(best, score)
            alpha = max(alpha, best)
            if beta <= alpha:
                break
        return best
    else:
        best = 999
        for cell in empty:
            board[cell] = 'O'
            score = heuristic_ab(board, depth+1, True, alpha, beta, max_depth)
            board[cell] = ' '
            best = min(best, score)
            beta = min(beta, best)
            if beta <= alpha:
                break
        return best

def best_move_heuristic(board, max_depth=4):
    global call_count
    call_count = 0
    best_score = -999
    move = None
    for cell in get_empty_cells(board):
        board[cell] = 'X'
        score = heuristic_ab(board, 0, False, -999, 999, max_depth)
        board[cell] = ' '
        if score > best_score:
            best_score = score
            move = cell
    print(f"[Heuristic AB, depth={max_depth}] Nodes explored: {call_count}")
    return move
