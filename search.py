import os

# Run simulation 5 times, each time with new random synaptic weights
for i in range(5):
    print(f"Running simulation {i + 1}...")

    # Generate a new robot with different random weights
    os.system("python generate.py")  
    
    # Run simulation for the generated robot
    os.system("python simulate.py")  
