# simulate.py initializes a SIMULATION object and runs the simulation loop
import sys
from simulation import SIMULATION

# Check if a mode (GUI or DIRECT) is provided as a command-line argument
if len(sys.argv) > 1:
    mode = sys.argv[1]  # Use the provided mode (e.g., "GUI" or "DIRECT")
else:
    mode = "DIRECT"  # Default to "DIRECT" mode if no mode is provided

# Check if a solution ID is provided as a command-line argument
if len(sys.argv) > 2:
    solutionID = sys.argv[2]  # Use the provided solution ID
else:
    solutionID = "0"  # Default to solution ID "0" if none is provided

# Create a SIMULATION object with the specified mode and solution ID
simulation = SIMULATION(mode, solutionID)

# Run the simulation loop
simulation.Run()

# Retrieve and save the fitness of the robot after the simulation ends
simulation.Get_Fitness()