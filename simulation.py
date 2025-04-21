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

    def __init__(self, directOrGUI, solutionID):
        """
        Initializes the simulation environment.

        Args:
            directOrGUI (str): Specifies whether the simulation runs in GUI mode ("GUI") or headless mode ("DIRECT").
            solutionID (int): A unique identifier for the solution being simulated.
        """
        self.directOrGUI = directOrGUI
        self.solutionID = solutionID

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

    def Run(self):
        """
        Runs the simulation loop for a specified number of iterations.

        The robot senses, thinks, and acts in each iteration.
        """
        for t in range(self.num_time_steps):
            p.stepSimulation()  # Advance the simulation by one time step
            self.robot.Sense(t)  # Collect sensor data from the robot
            self.robot.Think()  # Process the sensor data using the robot's neural network
            self.robot.Act(t)  # Actuate the robot's motors based on the neural network's output

            # Record touch sensor values for this time step
            for i, sensor in enumerate(self.robot.sensors.values()):
                # Here we use -1 when a sensor is NOT in contact (i.e. off the ground) and 1 when it IS contacting.
                self.sensor_matrix[t, i] = -1 if sensor.values[t] <= 0 else 1
        

            # If in GUI mode, pause briefly to allow visualization
            if self.directOrGUI == "GUI":
                time.sleep(c.TIME_STEP)

        # Save touch sensor data to a file after the simulation loop
        self.Save_Touch_Sensor_Data()

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

    def __del__(self):
        """
        Cleans up the simulation environment by disconnecting from PyBullet.
        This is called automatically when the SIMULATION object is deleted.
        """
        p.disconnect()

    def Get_Fitness(self):
        """
        Retrieves the fitness of the robot by calling its Get_Fitness method.
        This method is typically called at the end of the simulation to evaluate the robot's performance.
        """
        self.robot.Get_Fitness()