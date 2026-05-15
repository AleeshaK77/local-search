import random

class Board:
    def __init__(self, n, state=None):
        self.n = n
        if state is None:
            self.state = [random.randint(0, n - 1) for _ in range(n)] #random initial state, each row gets a queen in a random column
        else:
            self.state = list(state)

    def get_conflicts(self):
        """
        Calculates the total number of pairs of queens attacking each other.
        This is the cost function we want to minimize (aiming for 0).
        """
        conflicts = 0
        for i in range(self.n):
            for j in range(i + 1, self.n):
                if self.state[i] == self.state[j]: #same column
                    conflicts += 1
                elif abs(i - j) == abs(self.state[i] - self.state[j]): #same diagonal: distance in rows == distance in columns
                    conflicts += 1
        return conflicts

    def get_neighbors(self):
        """
        Generates all possible next states by moving one queen 
        within its own row to a different column.
        """
        neighbors = []
        for row in range(self.n):
            for column in range(self.n):
                if self.state[row] != column:
                    new_state = list(self.state)
                    new_state[row] = column
                    neighbors.append(Board(self.n, new_state))
        return neighbors

    def display(self):
        """
        Renders the 1D state into a 2D grid for the terminal.
        """
        print(f"\nCurrent Board (Conflicts: {self.get_conflicts()})")
        bar = "+---" * self.n + " +"
        print(bar)
        for row in range(self.n):
            row_string = " | "
            for column in range(self.n):
                if self.state[row] == column:
                    row_string += "Q | "
                else:
                    row_string += ". | "
            print(row_string)
            print(bar)

    def __lt__(self, other):
        """Helper for priority queues or sorting based on fitness."""
        return self.get_conflicts() < other.get_conflicts()