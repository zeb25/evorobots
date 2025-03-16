import pybullet as p
import time
import pybullet_data
import pyrosim.pyrosim as pyrosim
import numpy as numpy
import random
import math
import constants as c
from robot import ROBOT
from world import WORLD
from motor import MOTOR

class SIMULATION:
    
    def __init__(self):

        self.world = WORLD()
        self.robot = ROBOT()


    def Run(self):
        
        for t in range(c.ITERATIONS):
            self.robot.Sense(t)
            self.robot.Think()
            self.robot.Act(t)
            p.stepSimulation()
            time.sleep(c.TIME_STEP)

            # print("Iteration: ", t)

        self.Save_Data()

    def Save_Data(self):
        numpy.save("data/back_leg_sensor_values.npy", self.backLegSensorValues)
        numpy.save("data/front_leg_sensor_values.npy", self.frontLegSensorValues)

    def __del__(self):
        p.disconnect()
