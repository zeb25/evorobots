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
    
    def __init__(self, directOrGUI, solutionID):

        self.directOrGUI = directOrGUI
        self.solutionID = solutionID
        if self.directOrGUI=="DIRECT":
            self.physicsClient = p.connect(p.DIRECT)
        else:
            self.physicsClient = p.connect(p.GUI)
        p.setAdditionalSearchPath(pybullet_data.getDataPath())
        p.configureDebugVisualizer(p.COV_ENABLE_GUI, 0)
        p.setGravity(0, 0, c.GRAVITY, self.physicsClient)

        self.world = WORLD()
        self.robot = ROBOT(self.solutionID)

    def Run(self):
        
        for t in range(c.ITERATIONS):
            p.stepSimulation()
            self.robot.Sense(t)
            self.robot.Think()
            self.robot.Act(t)
            if self.directOrGUI=="GUI":
                time.sleep(c.TIME_STEP)

    def __del__(self):
        p.disconnect()

    def Get_Fitness(self):
        self.robot.Get_Fitness()