from game import get_empty_cells, check_winner

call_count = 0

def alpha_beta(board, is_maximizing, alpha, beta):
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
            score = alpha_beta(board, False, alpha, beta)
            board[cell] = ' '
            best = max(best, score)
            alpha = max(alpha, best)
            if beta <= alpha:
                break  # beta cutoff
        return best
    else:
        best = 999
        for cell in empty:
            board[cell] = 'O'
            score = alpha_beta(board, True, alpha, beta)
            board[cell] = ' '
            best = min(best, score)
            beta = min(beta, best)
            if beta <= alpha:
                break  # alpha cutoff
        return best

def best_move_alpha_beta(board):
    global call_count
    call_count = 0
    best_score = -999
    move = None
    for cell in get_empty_cells(board):
        board[cell] = 'X'
        score = alpha_beta(board, False, -999, 999)
        board[cell] = ' '
        if score > best_score:
            best_score = score
            move = cell
    print(f"[Alpha-Beta] Nodes explored: {call_count}")
    return move
