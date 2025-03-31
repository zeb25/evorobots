from solution import SOLUTION
import constants as c
import copy

class HILL_CLIMBER():
    """
    The HILL_CLIMBER class implements a simple hill-climbing algorithm.
    It evolves a single solution over multiple generations by mutating it and selecting the better solution.
    """

    def __init__(self):
        """
        Initializes the hill climber by creating an initial parent solution.
        """
        self.parent = SOLUTION()  # Create the initial parent solution

    def Evolve(self):
        """
        Evolves the solution over multiple generations.

        The parent solution is evaluated in GUI mode initially, and then the evolution process
        is carried out for a specified number of generations.
        """
        self.parent.Evaluate("GUI")  # Evaluate the initial parent solution in GUI mode

        # Perform evolution for the specified number of generations
        for currentGeneration in range(c.numberOfGenerations):
            self.Evolve_For_One_Generation()

    def Evolve_For_One_Generation(self):
        """
        Evolves the solution for one generation.

        This involves spawning a child solution, mutating it, evaluating its fitness,
        printing the fitness values, and selecting the better solution to survive.
        """
        self.Spawn()  # Create a child solution by copying the parent
        self.Mutate()  # Mutate the child solution
        self.child.Evaluate("DIRECT")  # Evaluate the child solution in DIRECT mode
        self.Print()  # Print the fitness of the parent and child
        self.Select()  # Select the better solution to survive

    def Spawn(self):
        """
        Creates a child solution by making a deep copy of the parent solution.
        """
        self.child = copy.deepcopy(self.parent)

    def Mutate(self):
        """
        Mutates the child solution to introduce variation.
        """
        self.child.Mutate()

    def Select(self):
        """
        Selects the better solution to survive.

        If the child's fitness is better (lower) than the parent's fitness,
        the child replaces the parent.
        """
        if self.parent.fitness < self.child.fitness:
            self.parent = self.child

    def Print(self):
        """
        Prints the fitness of the parent and child solutions for the current generation.
        """
        print("\n Parent Fitness: " + str(self.parent.fitness) + 
              "; Child Fitness: " + str(self.child.fitness))

    def Show_Best(self):
        """
        Displays the best solution by re-evaluating the parent solution in GUI mode.
        """
        self.parent.Evaluate("GUI")