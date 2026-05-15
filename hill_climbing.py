import random
from board import Board # type: ignore

def hill_climbing(initial_board):
    current = initial_board
    history = [current.get_conflicts()]

    while True:
        neighbors = current.get_neighbors()
        if not neighbors:
            break
            
        neighbor = min(neighbors, key = lambda b: b.get_conflicts()) #find best neighbor (fewest conflicts)
        
        if neighbor.get_conflicts() >= current.get_conflicts(): #if best neighbour isn't better than current position, we've hit local max or plateau
            break
            
        current = neighbor
        
    return current, history

def hill_climbing_random_restart(n, max_attempts = 100):
    for i in range(max_attempts):
        print(f"\n--- Attempt {i+1} ---")
        board = Board(n)
        result = hill_climbing(board)
        
        if result.get_conflicts() == 0:
            print(f"Goal reached on attempt {i + 1}!")
            return result
    return None

