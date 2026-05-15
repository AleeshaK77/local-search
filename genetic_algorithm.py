import random
from board import Board

def get_fitness(board):
    max_conflicts = (board.n * (board.n - 1)) / 2 #max conflicts for nqeens: n*(n-1)/2
    return max_conflicts - board.get_conflicts()

def reproduce(parent_x, parent_y):
    n = parent_x.n
    c = random.randint(0, n - 1) #crossover point
    child_state = parent_x.state[:c] + parent_y.state[c:] #take prefix from x suffix from y
    return Board(n, child_state)

def mutate(board):
    n = board.n
    new_state = list(board.state)
    row = random.randint(0, n - 1) #random row random column
    new_column = random.randint(0, n - 1)
    new_state[row] = new_column
    return Board(n, new_state)

def genetic_algorithm(population_size, n, mutation_prob=0.1):
    population = [Board(n) for _ in range(population_size)] #initialise random population
    history = []

    generation = 0
    while True:
        best_individual = max(population, key = get_fitness) 
        current_best_conflicts = best_individual.get_conflicts()
        history.append(current_best_conflicts)
        if current_best_conflicts == 0 or generation > 2000: #check if solution
            return best_individual, history
            
        new_population = []
        
        weights = [get_fitness(ind) for ind in population] #selection based on fitness
        
        for _ in range(population_size):
            parent_1, parent_2 = random.choices(population, weights = weights, k = 2) #select 2 parents
            
            child = reproduce(parent_1, parent_2) #crossover
            
            if random.random() < mutation_prob: #introduce mutation
                child = mutate(child)
                
            new_population.append(child)
            
        population = new_population
        generation += 1
        
