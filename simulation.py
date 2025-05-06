# This file defines the SIMULATION class, which manages the PyBullet simulation environment.
# It handles the initialization of the simulation, running the simulation loop, and cleaning up resources.

import pybullet as p
import time
import pybullet_data
import pyrosim.pyrosim as pyrosim
import numpy as np
import random
import math
import constants as c
from robot import ROBOT
from world import WORLD
from motor import MOTOR
import os

class SIMULATION:
    """
    The SIMULATION class manages the PyBullet simulation environment.
    It initializes the simulation, runs the simulation loop, and handles cleanup.
    """

    def __init__(self, directOrGUI, solutionID, fitness_type="long_jump"):
        """
        Initializes the simulation environment.

        Args:
            directOrGUI (str): Specifies whether the simulation runs in GUI mode ("GUI") or headless mode ("DIRECT").
            solutionID (int): A unique identifier for the solution being simulated.
            fitness_type (str): The type of fitness to calculate ("long_jump" or "high_jump").
        """
        self.directOrGUI = directOrGUI
        self.solutionID = solutionID
        self.fitness_type = fitness_type  # Store the fitness type

        # Connect to PyBullet in the specified mode (GUI or DIRECT)
        if self.directOrGUI == "DIRECT":
            self.physicsClient = p.connect(p.DIRECT)
        else:
            self.physicsClient = p.connect(p.GUI)

        # Set up PyBullet search paths and visualization settings
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        p.configureDebugVisualizer(p.COV_ENABLE_GUI, 0)  # Disable the default PyBullet GUI

        # Set gravity for the simulation
        p.setGravity(0, 0, c.GRAVITY, self.physicsClient)

        # Initialize the world and robot
        self.world = WORLD()  # Create the simulation world
        self.robot = ROBOT(self.solutionID)  # Create the robot with the given solution ID

        self.num_time_steps = c.ITERATIONS  # Number of time steps
        self.num_sensors = len(self.robot.sensors)  # Dynamically determine the number of sensors
        self.sensor_matrix = np.zeros((self.num_time_steps, self.num_sensors), dtype=int)  # Binary matrix for sensor states
        self.horizontal_displacement = 0  # Track horizontal displacement
        self.time_airborne = 0  # Track time spent airborne

    def Run(self):
        """
        Runs the simulation loop for a specified number of iterations.

        The robot senses, thinks, and acts in each iteration.
        """
        print(f"Starting simulation for solution ID: {self.solutionID}")
        # Remove all relevant files at the start of the simulation
        self.Cleanup_Output_Files()

        initial_position, _ = p.getBasePositionAndOrientation(self.robot.robotID)  # Get initial position

        for t in range(self.num_time_steps):
            if t % 100 == 0:  # Print progress every 100 time steps
                print(f"Simulation time step: {t}/{self.num_time_steps}")
            p.stepSimulation()  # Advance the simulation by one time step
            self.robot.Sense(t)  # Collect sensor data from the robot
            self.robot.Think()  # Process the sensor data using the robot's neural network
            self.robot.Act(t)  # Actuate the robot's motors based on the neural network's output

            # Record touch sensor values for this time step
            all_off_ground = True
            for i, sensor in enumerate(self.robot.sensors.values()):
                self.sensor_matrix[t, i] = -1 if sensor.values[t] <= 0 else 1 # if touching ground, set to 1
                if self.sensor_matrix[t, i] == 1:
                    all_off_ground = False

            # Increment time airborne if all sensors are off the ground
            if all_off_ground:
                self.time_airborne += 1

            # If in GUI mode, pause briefly to allow visualization
            if self.directOrGUI == "GUI":
                time.sleep(c.TIME_STEP)
    

        # Calculate horizontal displacement
        final_position, _ = p.getBasePositionAndOrientation(self.robot.robotID)
        self.horizontal_displacement = final_position[0] - initial_position[0]  # Displacement along x-axis
       
        # Save touch sensor data and fitness results
        self.Save_Touch_Sensor_Data()
        self.Save_Displacement_And_Time()
        fitness = self.Calculate_Fitness()
        self.Save_Fitness(fitness)
        print(f"Simulation for solution ID {self.solutionID} completed with fitness: {fitness}")

    def Cleanup_Output_Files(self):
        """
        Removes all relevant output files at the start of a new simulation run.
        """
        print("Cleaning up output files...")
        output_dir = "/Users/zoebell/evorobots/output"  # Specify the directory
        if os.path.exists(output_dir):
            for file_name in os.listdir(output_dir):
                if file_name.startswith("sensor_matrix_") or file_name.startswith("displacement_time_") or file_name.startswith("fitness_"):
                    os.remove(os.path.join(output_dir, file_name))
        print("Output files cleaned up.")

    def Save_Touch_Sensor_Data(self):
        """
        Saves the touch sensor data to a .txt file for later evaluation.
        Each row contains binary touch sensor values for each time step.
        """
        output_dir = "/Users/zoebell/evorobots/output"  # Specify the directory
        os.makedirs(output_dir, exist_ok=True)  # Ensure the directory exists

        # Remove any pre-existing sensor_matrix files
        for file_name in os.listdir(output_dir):
            if file_name.startswith("sensor_matrix_") and file_name.endswith(".txt"):
                os.remove(os.path.join(output_dir, file_name))

        file_path = os.path.join(output_dir, f"sensor_matrix_{self.solutionID}.txt")
        np.savetxt(file_path, self.sensor_matrix, fmt='%d')  # Save the binary matrix
        print(f"Sensor matrix saved to {file_path}")

    def Save_Displacement_And_Time(self):
        """
        Saves the horizontal displacement and time airborne to a file.
        """
        output_dir = "/Users/zoebell/evorobots/output"  # Specify the directory
        os.makedirs(output_dir, exist_ok=True)  # Ensure the directory exists

        file_path = os.path.join(output_dir, f"displacement_time_{self.solutionID}.txt")
        with open(file_path, "w") as f:
            f.write(f"Horizontal Displacement (d): {self.horizontal_displacement}\n")
            f.write(f"Time Airborne (t): {self.time_airborne}\n")
        print(f"Displacement and time saved to {file_path}")

    def Save_Fitness(self, fitness):
        """
        Saves the calculated fitness to a file.
        """
        output_dir = "/Users/zoebell/evorobots/output"  # Specify the directory
        os.makedirs(output_dir, exist_ok=True)  # Ensure the directory exists

        file_path = os.path.join(output_dir, f"fitness{self.solutionID}.txt")
        with open(file_path, "w") as f:
            f.write(str(fitness))
        print(f"Fitness saved to {file_path}")

    def __del__(self):
        """
        Cleans up the simulation environment by disconnecting from PyBullet.
        This is called automatically when the SIMULATION object is deleted.
        """
        p.disconnect()

    def Calculate_Fitness(self):
        """
        Calculates the fitness of the robot based on the specified fitness type.
        """
        if self.fitness_type == "long_jump":
            # Fitness is based on horizontal displacement multiplied by time airborne
            fitness = self.horizontal_displacement * self.time_airborne
            print(f"Calculated fitness (long_jump): {fitness}")
        elif self.fitness_type == "high_jump":
            # Fitness is based on the maximum height achieved
            max_height = max(p.getBasePositionAndOrientation(self.robot.robotID)[0][2] for _ in range(self.num_time_steps))
            fitness = max_height
            print(f"Calculated fitness (high_jump): {fitness}")
        else:
            raise ValueError(f"Unknown fitness type: {self.fitness_type}")
        return fitness