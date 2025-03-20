# parallelHillClimber.py
import os  # NEW: For file management
from solution import SOLUTION  # NEW:
from constants import populationSize, numberOfGenerations  # NEW:
import copy  # NEW:

class PARALLEL_HILL_CLIMBER:  # NEW: Renamed class
    def __init__(self):
        # Delete any remnant brain and fitness files at startup
        os.system("rm brain*.nndf")  # Use "del brain*.nndf" on Windows
        os.system("rm fitness*.txt")  # Use "del fitness*.txt" on Windows
        self.nextAvailableID = 0  # NEW: Initialize unique ID counter
        self.parents = {}  # NEW: Dictionary for parents
        for i in range(populationSize):  # NEW:
            self.parents[self.nextAvailableID] = SOLUTION(self.nextAvailableID)  # NEW: Create parent with unique ID
            self.nextAvailableID += 1  # NEW:
        # (Optional debug print – remove after verifying)
        # print("Initial parents:", self.parents)
    
    def Evolve(self):
        # First, evaluate all parents in parallel using GUI mode.
        self.Evaluate(self.parents, "DIRECT")  # NEW:
        # Now evolve for a number of generations.
        for gen in range(numberOfGenerations):  # NEW:
            self.Spawn()           # NEW:
            self.Mutate()          # NEW:
            self.Evaluate(self.children, "DIRECT")  # NEW: Evaluate children in DIRECT mode (fast)
            self.Print()           # NEW: Print fitness of parents and children together
            self.Select()          # NEW: Compete children against parents
        # Finally, re-run the best parent's simulation in GUI mode.
        self.Show_Best()  # NEW:
    
    def Spawn(self):
        self.children = {}  # NEW: Create an empty dictionary for children
        for key in self.parents:  # NEW:
            # Create a deep copy of each parent.
            child = copy.deepcopy(self.parents[key])
            # Assign a new unique ID to this child.
            child.Set_ID(self.nextAvailableID)  # NEW:
            self.children[key] = child  # NEW: Use the same key for correspondence.
            self.nextAvailableID += 1  # NEW:
        # (Optional: For debugging, print self.children and exit() here)
        # for key in self.children:
        #     print("Child", key, ":", self.children[key])
        # exit()  # NEW: Remove after verifying.
    
    def Mutate(self):
        # Iterate through each child and mutate it.
        for key in self.children:
            self.children[key].Mutate()  # NEW:
    
    def Evaluate(self, solutions, mode):
        # Start all simulations in parallel.
        for key in solutions:
            solutions[key].Start_Simulation(mode)  # NEW:
        # Then, wait for all fitness files to appear and read fitness values.
        for key in solutions:
            solutions[key].Wait_For_Simulation_To_End()  # NEW:
    
    def Print(self):
        print("")  # NEW: Print an empty line at the start
        for key in self.parents:
            parentFitness = self.parents[key].fitness
            # For the corresponding child (if present), get its fitness.
            childFitness = self.children[key].fitness if key in self.children else None
            print("Index", key, "| Parent fitness:", parentFitness, "| Child fitness:", childFitness)  # NEW:
        print("")  # NEW: Empty line at the end
    
    def Select(self):
        # For each key, if the child's fitness is lower (better) than its parent's, replace the parent.
        for key in self.children:
            if self.children[key].fitness < self.parents[key].fitness:
                self.parents[key] = self.children[key]  # NEW:
    
    def Show_Best(self):
        # Find the parent with the lowest fitness.
        bestKey = None
        bestFitness = None
        for key in self.parents:
            fitness = self.parents[key].fitness
            if bestFitness is None or fitness < bestFitness:
                bestFitness = fitness
                bestKey = key
        print("Best solution is at index", bestKey, "with fitness", bestFitness)  # NEW:
        # Re-run the best solution with graphics.
        self.parents[bestKey].Start_Simulation("GUI")  # NEW: