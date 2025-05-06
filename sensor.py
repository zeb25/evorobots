import pybullet as p
import time
import pybullet_data
import pyrosim.pyrosim as pyrosim
import numpy as numpy
import random
import math
import constants as c

class SENSOR:
    """
    The SENSOR class manages touch sensors for specific robot links.
    It collects sensor values during the simulation and saves them for later use.
    """

    def __init__(self, linkName):
        """
        Initializes the SENSOR object.

        Args:
            linkName (str): The name of the link to which the sensor is attached.
        """
        self.linkName = linkName  # Store the name of the link associated with this sensor
        self.values = numpy.zeros(c.ITERATIONS)  # Initialize a vector of zeros to store sensor values for each time step

    def Get_Value(self, t):
        """
        Collects the touch sensor value for the current time step.

        Args:
            t (int): The current time step in the simulation.
        """
        self.values[t] = pyrosim.Get_Touch_Sensor_Value_For_Link(self.linkName)  
        # print("Sensor value for link", self.linkName, "at time", t, ":", self.values[t])
        self.Save_Values()  # Save the sensor values after each time step

    def Save_Values(self):
        """
        Saves the collected sensor values to a file for analysis.

        The values are saved as a NumPy array in the "data/sensor_values.npy" file.
        """
        numpy.save("data/sensor_values.txt", self.values)