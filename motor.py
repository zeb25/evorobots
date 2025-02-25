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
        self.values = numpy.zeros(c.ITERATIONS)  # Vector of zeros
        self.Prepare_To_Act()

    def Prepare_To_Act(self):
        self.amplitude = c.AMPLITUDE
        self.offset = c.PHASE_OFFSET

        if self.jointName == b"Torso_FrontLeg":
            self.frequency = c.FREQUENCY
        else:
            self.frequency = c.FREQUENCY_2
        
        # Generate sinusoidal values mapped to [-π/2, π/2]
        time_steps = numpy.linspace(0, 2 * math.pi, c.ITERATIONS)
        self.motorValues = self.amplitude * numpy.sin(self.frequency * time_steps + self.offset)

    def Set_Value(self, robot, t):

        targetPosition = self.motorValues[t]  

        pyrosim.Set_Motor_For_Joint(
                bodyIndex=robot.robotId,
                jointName=self.jointName,
                controlMode=p.POSITION_CONTROL,
                targetPosition=targetPosition,
                maxForce=c.MAX_FORCE
            )
        
    def Save_Values(self):
        numpy.save("data/motor_values.npy", self.values)