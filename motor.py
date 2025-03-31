import pybullet as p
import time
import pybullet_data
import pyrosim.pyrosim as pyrosim
import numpy as numpy
import random
import math
import constants as c

class MOTOR:
    """
    The MOTOR class represents a motor controlling a specific joint in the robot.
    It manages motor actuation, including setting target positions and preparing motor values.
    """

    def __init__(self, jointName):
        """
        Initializes the motor for a specific joint.

        Args:
            jointName (str): The name of the joint controlled by this motor.
        """
        self.jointName = jointName  # Store the joint name
        self.motorValues = numpy.zeros(c.ITERATIONS)  # Initialize a vector of zeros for motor values
        self.Prepare_To_Act()  # Prepare the motor for actuation

    def Set_Value(self, robotId, desiredAngle):
        """
        Sets the motor's target position for a specific joint.

        Args:
            robotId (int): The ID of the robot in the simulation.
            desiredAngle (float): The desired angle for the joint.
        """
        pyrosim.Set_Motor_For_Joint(
            bodyIndex=robotId,  # The ID of the robot
            jointName=self.jointName,  # The name of the joint
            controlMode=p.POSITION_CONTROL,  # Use position control mode
            targetPosition=desiredAngle,  # Set the target position for the joint
            maxForce=c.MAX_FORCE  # Maximum force the motor can apply
        )

    def Prepare_To_Act(self):
        """
        Prepares the motor for actuation by calculating motor values based on a sinusoidal function.
        """
        self.amplitude = c.AMPLITUDE  # Set the amplitude of the motor's motion
        if self.jointName == b"Torso_FrontLeg":  # Check if the joint is the front leg
            self.frequency = c.FREQUENCY  # Use the primary frequency for the front leg
        else:
            self.frequency = c.FREQUENCY_2  # Use a secondary frequency for other joints

        self.offset = c.PHASE_OFFSET  # Set the phase offset for the motor's motion
        self.time_steps = numpy.linspace(0, 2 * numpy.pi, c.ITERATIONS)  # Generate time steps for the simulation
        # Calculate motor values using a sinusoidal function
        self.motorValues = self.amplitude * numpy.sin(self.frequency * self.time_steps + self.offset)

    def Save_Values(self):
        """
        Saves the motor values to a file for analysis.

        The values are saved as a NumPy array in the "data/motors" directory.
        """
        numpy.save(f"data/motors/{self.jointName}_values", self.motorValues)  # Save motor values to a file