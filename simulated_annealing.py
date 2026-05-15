import math
import random
from board import Board

def simulated_annealing(board, max_steps = 50000):
    current = board
    history = []
    
    for t in range(1, max_steps):
        T = max(0.0001, 100 - (0.005 * t)) #linear cooling
        current_conflicts = current.get_conflicts()
        history.append(current_conflicts)
        if current_conflicts == 0:
            return current, history
        
        row = random.randint(0, board.n - 1) #for efficiency, pick one random neighbour directly
        column = random.randint(0, board.n - 1)
        
        neighbor_state = list(current.state) #manual creation of new state to avoid get_neighbours() overhead
        neighbor_state[row] = column
        neighbor_board = Board(board.n, neighbor_state)
        neighbor_conflicts = neighbor_board.get_conflicts()
        
        delta_e = current_conflicts - neighbor_conflicts
        
        if delta_e > 0 or random.random() < math.exp(delta_e / T): #accept if better, or with probability based on T
            current = neighbor_board
            
    return current, history