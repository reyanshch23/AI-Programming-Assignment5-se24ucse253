# minimax.py

from game import get_empty_cells, check_winner, is_terminal

call_count = 0  # track how many nodes are visited

def minimax(board, is_maximizing):
    global call_count
    call_count += 1

    winner = check_winner(board)
    if winner == 'X':
        return 1
    if winner == 'O':
        return -1
    if ' ' not in board:
        return 0

    empty = get_empty_cells(board)

    if is_maximizing:
        best = -999
        for cell in empty:
            board[cell] = 'X'
            score = minimax(board, False)
            board[cell] = ' '
            best = max(best, score)
        return best
    else:
        best = 999
        for cell in empty:
            board[cell] = 'O'
            score = minimax(board, True)
            board[cell] = ' '
            best = min(best, score)
        return best

def best_move_minimax(board):
    global call_count
    call_count = 0
    best_score = -999
    move = None
    for cell in get_empty_cells(board):
        board[cell] = 'X'
        score = minimax(board, False)
        board[cell] = ' '
        if score > best_score:
            best_score = score
            move = cell
    print(f"[Minimax] Nodes explored: {call_count}")
    return move