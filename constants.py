import math

# Simulation parameters
ITERATIONS = 1000 # Number of iterations in the simulation loop	
TIME_STEP = 1/60 # Simulation time step (to maintain real-time sync)	

# Physics parameters
GRAVITY = -9.8 # Gravitational acceleration (m/s²)	

# Motor control parameters
AMPLITUDE = math.pi / 4 # Amplitude of sinusoidal motion for motor control	
AMPLITUDE_2 = math.pi / 4 # Amplitude for the second leg	

FREQUENCY = 30 # Frequency of oscillation (how fast the legs move)	
FREQUENCY_2 = 30 / 2 # Frequency for the second leg	

PHASE_OFFSET = 0 # Phase offset for first leg movement	
PHASE_OFFSET_2 = math.pi / 2 # Phase offset for the second leg movement (out of phase with first leg)	

MAX_FORCE = 50 # Maximum force applied by the motors	
