import pybullet as p
import time
import pybullet_data
import pyrosim.pyrosim as pyrosim
import numpy as numpy
import random
import math
import constants as c

class SENSOR:

    def __init__(self, linkName):

        self.linkName = linkName  # Store link name in instance variable
        self.values = numpy.zeros(c.ITERATIONS)  # Vector of zeros

    def Get_Value(self, t):

        self.values[t]= pyrosim.Get_Touch_Sensor_Value_For_Link(self.linkName)

    def Save_Values(self):
        numpy.save("data/sensor_values.npy", self.values)