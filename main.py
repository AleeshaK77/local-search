import time
import matplotlib.pyplot as plt
import numpy as np
from board import Board
from hill_climbing import hill_climbing 
from simulated_annealing import simulated_annealing # type: ignore 
from genetic_algorithm import genetic_algorithm # type: ignore 

def run_suite(n = 8, trials = 20):
    stats = {
        'Hill Climbing': {'success': 0, 'times': [], 'histories': []},
        'Simulated Annealing': {'success': 0, 'times': [], 'histories': []},
        'Genetic Algorithm': {'success': 0, 'times': [], 'histories': []}
    }

    print(f"Running {trials} trials for each algorithm (N={n})...\n")

    for _ in range(trials):
        start = time.time() #hill climbing
        result, history = hill_climbing(Board(n)) 
        stats['Hill Climbing']['times'].append(time.time() - start)
        stats['Hill Climbing']['histories'].append(history)
        if result.get_conflicts() == 0: stats['Hill Climbing']['success'] += 1

        start = time.time() #simulated annealing
        result, history = simulated_annealing(Board(n))
        stats['Simulated Annealing']['times'].append(time.time() - start)
        stats['Simulated Annealing']['histories'].append(history)
        if result.get_conflicts() == 0: stats['Simulated Annealing']['success'] += 1

        start = time.time() #genetic algorithm
        result, history = genetic_algorithm(100, n)
        stats['Genetic Algorithm']['times'].append(time.time() - start)
        stats['Genetic Algorithm']['histories'].append(history)
        if result.get_conflicts() == 0: stats['Genetic Algorithm']['success'] += 1

    print("="*65) #table
    print(f"{'Algorithm':<20} | {'Success Rate':<15} | {'Avg Time (s)':<12}")
    print("-" * 65)
    for algo, data in stats.items():
        success_pct = (data['success'] / trials) * 100
        avg_time = sum(data['times']) / trials
        print(f"{algo:<20} | {success_pct:>11.1f}% | {avg_time:>10.4f}")
    print("="*65)

    plot_energy_landscapes(stats)

def plot_energy_landscapes(stats):
    plt.figure(figsize=(12, 6))
    
    for algo, data in stats.items():
        history = data['histories'][0]
        x = np.arange(len(history))
        
        if algo == 'Simulated Annealing' and len(history) > 100:
            window = 50
            smoothed = np.convolve(history, np.ones(window)/window, mode='valid') #smooth the curve
            plt.plot(x[:len(smoothed)], smoothed, label=f"{algo} (Smoothed)", linewidth=2)
        else:
            plt.plot(x, history, label=algo, linewidth=2)

    plt.xscale('log') #for scale
    plt.xlabel('Iterations (Log Scale)')
    plt.ylabel('Number of Conflicts')
    plt.title('Algorithm Convergence Comparison')
    plt.legend()
    plt.grid(True, which="both", ls="-", alpha=0.2)
    plt.show()

if __name__ == "__main__":
    run_suite(n=8, trials=50)