import pybullet as p
import time
import pybullet_data
import pyrosim.pyrosim as pyrosim
import numpy as numpy
import random
import math
import constants as c

class MOTOR:

    def __init__(self, jointName):

        self.jointName = jointName  # Store link name in instance variable
        self.motorValues = numpy.zeros(c.ITERATIONS)  # Vector of zeros
        self.Prepare_To_Act()

    def Set_Value(self, robotId, desiredAngle):

        pyrosim.Set_Motor_For_Joint(
            bodyIndex=robotId,
            jointName=self.jointName,
            controlMode=p.POSITION_CONTROL,
            targetPosition=desiredAngle,
            maxForce=c.MAX_FORCE)