# test_algorithms.py
# Test cases to verify all 4 algorithms

from game import make_board, print_board
from minimax import best_move_minimax
from alpha_beta import best_move_alpha_beta
from heuristic_ab import best_move_heuristic
from mcts import mcts

def test_win_detection():
    """X should pick the winning move immediately"""
    print("=== TEST: Win in one move ===")
    # X X _
    # O O _
    # _ _ _
    board = ['X','X',' ','O','O',' ',' ',' ',' ']
    print_board(board)

    for name, fn in [
        ("Minimax", best_move_minimax),
        ("Alpha-Beta", best_move_alpha_beta),
        ("Heuristic AB", best_move_heuristic),
    ]:
        move = fn(board[:])
        assert move == 2, f"{name} failed: got {move}, expected 2"
        print(f"{name}: chose cell {move} (correct)")

    move = mcts(board[:], iterations=500)
    print(f"MCTS: chose cell {move}")
    print()

def test_block_opponent():
    """X should block O from winning"""
    print("=== TEST: Block opponent win ===")
    # _ _ _
    # O O _
    # X _ X
    board = [' ',' ',' ','O','O',' ','X',' ','X']
    print_board(board)

    for name, fn in [
        ("Minimax", best_move_minimax),
        ("Alpha-Beta", best_move_alpha_beta),
        ("Heuristic AB", best_move_heuristic),
    ]:
        move = fn(board[:])
        assert move == 5, f"{name} failed: got {move}, expected 5"
        print(f"{name}: chose cell {move} (correct)")

    move = mcts(board[:], iterations=1000)
    print(f"MCTS: chose cell {move}")
    print()

def test_empty_board():
    """On empty board, center (4) or corner is standard best move"""
    print("=== TEST: Empty board ===")
    board = make_board()
    print_board(board)

    for name, fn in [
        ("Minimax", best_move_minimax),
        ("Alpha-Beta", best_move_alpha_beta),
        ("Heuristic AB", best_move_heuristic),
    ]:
        move = fn(board[:])
        print(f"{name}: chose cell {move}")

    move = mcts(board[:], iterations=2000)
    print(f"MCTS: chose cell {move}")
    print()

def test_near_draw():
    """Late game, no winning move, should not crash"""
    print("=== TEST: Near-draw position ===")
    # X O X
    # X O O
    # O X _
    board = ['X','O','X','X','O','O','O','X',' ']
    print_board(board)

    for name, fn in [
        ("Minimax", best_move_minimax),
        ("Alpha-Beta", best_move_alpha_beta),
        ("Heuristic AB", best_move_heuristic),
    ]:
        move = fn(board[:])
        assert move == 8, f"{name} failed: got {move}, expected 8"
        print(f"{name}: chose cell {move} (only move)")

    move = mcts(board[:], iterations=200)
    print(f"MCTS: chose cell {move}")
    print()

def compare_node_counts():
    """Show how alpha-beta prunes compared to minimax"""
    print("=== COMPARISON: Node counts on empty board ===")
    import minimax as mm
    import alpha_beta as ab

    board = make_board()
    mm.call_count = 0
    ab.call_count = 0

    mm.best_move_minimax(board[:])
    ab.best_move_alpha_beta(board[:])

    print(f"Minimax nodes:    {mm.call_count}")
    print(f"Alpha-Beta nodes: {ab.call_count}")
    reduction = (1 - ab.call_count / mm.call_count) * 100
    print(f"Reduction:        {reduction:.1f}%")
    print()

if __name__ == '__main__':
    test_win_detection()
    test_block_opponent()
    test_empty_board()
    test_near_draw()
    compare_node_counts()
    print("All tests done.")