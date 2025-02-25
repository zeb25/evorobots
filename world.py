import pybullet as p
import time
import pybullet_data
import pyrosim.pyrosim as pyrosim
import numpy as numpy
import random
import math
import constants as c

class WORLD:

    def __init__(self):

        self.physicsClient = p.connect(p.GUI)
        p.setAdditionalSearchPath(pybullet_data.getDataPath())

        p.configureDebugVisualizer(p.COV_ENABLE_GUI, 0)

        p.setGravity(0,0,c.GRAVITY, self.physicsClient)

       # Load environment & robot
        self.planeId = p.loadURDF("plane.urdf")
        p.loadSDF("world.sdf")
