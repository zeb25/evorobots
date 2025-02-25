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
            self.robot.Act(t)
            p.stepSimulation()
            '''
            self.backLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("BackLeg")
            print("Back leg sensor value:", self.backLegSensorValues[i])

            self.frontLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("FrontLeg")
            print("Front leg sensor value:", self.frontLegSensorValues[i])

            # Set motor controls
            pyrosim.Set_Motor_For_Joint(
                bodyIndex=self.robotId,
                jointName=b'Torso_BackLeg',
                controlMode=p.POSITION_CONTROL,
                targetPosition=self.targetAngles[i],
                maxForce=c.MAX_FORCE
            )

            pyrosim.Set_Motor_For_Joint(
                bodyIndex=self.robotId,
                jointName=b'Torso_FrontLeg',
                controlMode=p.POSITION_CONTROL,
                targetPosition=self.targetAngles2[i],
                maxForce=c.MAX_FORCE
            )
            '''
            time.sleep(c.TIME_STEP)

            print("Iteration: ", t)

        self.Save_Data()

    def Save_Data(self):
        numpy.save("data/back_leg_sensor_values.npy", self.backLegSensorValues)
        numpy.save("data/front_leg_sensor_values.npy", self.frontLegSensorValues)

    def __del__(self):
        p.disconnect()
