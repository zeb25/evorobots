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

       # Load environment & robot
        self.planeId = p.loadURDF("plane.urdf")
        p.loadSDF("world.sdf")
