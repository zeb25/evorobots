# This file defines the SIMULATION class, which manages the PyBullet simulation environment.
# It handles the initialization of the simulation, running the simulation loop, and cleaning up resources.

import pybullet as p
import time
import pybullet_data
import pyrosim.pyrosim as pyrosim
import numpy
import random
import math
import constants as c
from robot import ROBOT
from world import WORLD
from motor import MOTOR

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

    def Run(self):
        """
        Runs the simulation loop for a specified number of iterations.

        The robot senses, thinks, and acts in each iteration.
        """
        for t in range(c.ITERATIONS):
            p.stepSimulation()  # Advance the simulation by one time step
            self.robot.Sense(t)  # Collect sensor data from the robot
            self.robot.Think()  # Process the sensor data using the robot's neural network
            self.robot.Act(t)  # Actuate the robot's motors based on the neural network's output

            # If in GUI mode, pause briefly to allow visualization
            if self.directOrGUI == "GUI":
                time.sleep(c.TIME_STEP)

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