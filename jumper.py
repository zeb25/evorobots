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

    def Evolve_With_Fitness_Type(self, fitness_type):
        """
        Evolves the population using the specified fitness type.
        Args:
            fitness_type (str): The type of fitness function ("long_jump" or "high_jump").
        """
        for key in self.parents:
            self.parents[key].Set_Fitness_Type(fitness_type)

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
        print("Spawning new children...")
        self.children = {}
        for key in self.parents:
            child = copy.deepcopy(self.parents[key])
            child.Set_ID(self.nextAvailableID)
            self.children[key] = child
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
        for key in solutions:
            solutions[key].Start_Simulation(mode)

        for key in solutions:
            print(f"Waiting for simulation to finish for solution ID: {key}")
            solutions[key].Wait_For_Simulation_To_End()
            print(f"Simulation finished for solution ID: {key}, fitness: {solutions[key].fitness}")

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
        If a child's fitness is better (higher), it replaces the parent.
        """
        print("Selecting the best solutions...")
        for key in self.children:
            print(f"Parent fitness: {self.parents[key].fitness}, Child fitness: {self.children[key].fitness}")
            if self.children[key].fitness > self.parents[key].fitness:
                print(f"Replacing parent with child for solution ID: {key}")
                self.parents[key] = self.children[key]
        print("Selection process completed.")

    def Show_Best(self):
        """
        Identifies the best solution in the population and re-runs its simulation in GUI mode for visualization.
        """
         # Find the parent with the best (lowest) fitness
        bestKey = None
        bestFitness = -1000.0  # Change the initial value to a very low number
        for key in self.parents:
            fitness = self.parents[key].fitness
            if fitness > bestFitness: 
                bestFitness = fitness
                bestKey = key

        print(f"Best solution is at index {bestKey} with fitness {bestFitness}")
        self.parents[bestKey].Start_Simulation("GUI")  # Re-run the best solution in GUI mode
