import math

# Simulation parameters
ITERATIONS = 1000 # Number of iterations in the simulation loop	
TIME_STEP = 1/60 # Simulation time step (to maintain real-time sync)	

# Physics parameters
GRAVITY = -9.8  # Keep gravity as is, or reduce it slightly (e.g., -5.0 for a lower-gravity environment)

# Motor control parameters
AMPLITUDE = math.pi / 2  # Increase amplitude for greater leg motion (was math.pi / 3)
AMPLITUDE_2 = math.pi / 2  # Increase amplitude for the second leg (was math.pi / 3)

FREQUENCY = 40  # Slightly increase frequency for faster leg motion (was 35)
FREQUENCY_2 = 40 / 2  # Adjust frequency for the second leg (was 35 / 2)

PHASE_OFFSET = 0 # Phase offset for first leg movement	
PHASE_OFFSET_2 = math.pi / 2 # Phase offset for the second leg movement (out of phase with first leg)	

MAX_FORCE = 100  # Increase maximum force applied by the motors (was 80)

numberOfGenerations = 10 # Number of generations for the genetic algorithm
populationSize = 1 # Size of the population for the genetic algorithm

numSensorNeurons = 4 # Number of sensor neurons in the neural network
numMotorNeurons = 8 # Number of motor neurons in the neural network

motorJointRange = 0.4  # Increase range of motion for motor joints (was 0.3)
# Note: The motorJointRange is set to 0.4 radians, which is approximately 22.9 degrees.