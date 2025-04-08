import os
from solution import SOLUTION
from constants import populationSize, numberOfGenerations
import copy

class JUMPER:
    """
    The JUMPER class implements a parallel hill-climbing algorithm.
    It manages a population of solutions, evaluates their fitness, and evolves them over generations to optimize fitness.
    """

    def __init__(self):
        """
        Initializes the parallel hill climber by creating an initial population of solutions
        and cleaning up any leftover files from previous runs.
        """
        # Remove any leftover brain and fitness files from previous runs
        os.system("rm brain*.nndf")
        os.system("rm fitness*.txt")

        # Initialize the population of parent solutions
        self.nextAvailableID = 0  # Counter to assign unique IDs to solutions

        self.parents = {}  # Dictionary to store parent solutions


        for i in range(populationSize): 
            self.parents[self.nextAvailableID] = SOLUTION(self.nextAvailableID) # Create a new solution
            self.nextAvailableID += 1 # Increment the ID for the next solution

    def Evolve(self):
        """
        Evolves the population of solutions over multiple generations.
        Each generation involves spawning children, mutating them, evaluating their fitness,
        and selecting the best solutions to survive.
        """
        # Evaluate the initial population of parents
        self.Evaluate(self.parents, "DIRECT")

        # Perform evolution over a specified number of generations
        for gen in range(numberOfGenerations):
            self.Spawn()           # Create children from the parent solutions
            self.Mutate()          # Mutate the children
            self.Evaluate(self.children, "DIRECT")  # Evaluate the children
            self.Print()           # Print the fitness of parents and children
            self.Select()          # Select the best solutions to survive

        # Re-run the best solution in GUI mode for visualization
        self.Show_Best()

    def Spawn(self):
        """
        Creates a new generation of children by copying and assigning unique IDs to the parents.
        """
        self.children = {}  # Dictionary to store child solutions
        for key in self.parents:
            # Create a deep copy of each parent
            child = copy.deepcopy(self.parents[key])
            # Assign a new unique ID to the child
            child.Set_ID(self.nextAvailableID)
            self.children[key] = child  # Store the child in the dictionary
            self.nextAvailableID += 1

    def Mutate(self):
        """
        Mutates each child solution to introduce variation.
        """
        for key in self.children:
            self.children[key].Mutate()

    def Evaluate(self, solutions, mode):
        """
        Evaluates the fitness of a set of solutions by running their simulations.

        Args:
            solutions (dict): A dictionary of solutions to evaluate.
            mode (str): The simulation mode ("DIRECT" or "GUI").
        """
        # Start simulations for all solutions
        for key in solutions:
            solutions[key].Start_Simulation(mode)

        # Wait for all simulations to finish and retrieve fitness values
        for key in solutions:
            solutions[key].Wait_For_Simulation_To_End()

    def Print(self):
        """
        Prints the fitness of the parent and child solutions for each generation.
        """
        print("")  # Print an empty line for readability
        for key in self.parents:
            parentFitness = self.parents[key].fitness
            childFitness = self.children[key].fitness if key in self.children else None
            print(f"Index {key} | Parent fitness: {parentFitness} | Child fitness: {childFitness}")
        print("")  # Print an empty line for readability

    def Select(self):
        """
        Selects the best solutions to survive by comparing the fitness of parents and children.
        If a child's fitness is better (lower), it replaces the parent.
        """
        for key in self.children:
            if self.children[key].fitness > self.parents[key].fitness:
                self.parents[key] = self.children[key]

    def Show_Best(self):
        """
        Identifies the best solution in the population and re-runs its simulation in GUI mode for visualization.
        """
         # Find the parent with the best (lowest) fitness
        bestKey = None
        bestFitness = -1000.0  # Change the initial value to a very low number
        for key in self.parents:
            fitness = self.parents[key].fitness
            if fitness > bestFitness:  # Change < to >
                bestFitness = fitness
                bestKey = key

        print(f"Best solution is at index {bestKey} with fitness {bestFitness}")
        self.parents[bestKey].Start_Simulation("GUI")  # Re-run the best solution in GUI mode
