# simulate.py
import sys  # NEW: Import sys
from simulation import SIMULATION

if len(sys.argv) > 1:
    mode = sys.argv[1]
else:
    mode = "DIRECT"

if len(sys.argv) > 2:
    solutionID = sys.argv[2]
else:
    solutionID = "0"  # NEW: Default ID if not provided

simulation = SIMULATION(mode, solutionID)  # NEW: Pass solutionID as well
simulation.Run()
simulation.Get_Fitness()