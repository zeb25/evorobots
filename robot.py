import pybullet as p
import time
import pybullet_data
import pyrosim.pyrosim as pyrosim
import numpy as numpy
import random
import math
import constants as c
from sensor import SENSOR
from motor import MOTOR
from pyrosim.neuralNetwork import NEURAL_NETWORK
import os

class ROBOT:

    def __init__(self, solutionID):
        self.solutionID = solutionID
        self.motors = {}
        self.sensors = {}
        self.robotID = p.loadURDF("body.urdf")
        pyrosim.Prepare_To_Simulate(self.robotID)
        self.nn = NEURAL_NETWORK("brain" + str(solutionID) + ".nndf")
        self.Prepare_To_Sense()
        self.Prepare_To_Act()

    def Prepare_To_Sense(self):
        for linkName in pyrosim.linkNamesToIndices:
            self.sensors[linkName] = SENSOR(linkName)

    def Sense(self, t):
        for sensor in self.sensors.values():
            sensor.Get_Value(t)

    def Prepare_To_Act(self):
        for jointName in pyrosim.jointNamesToIndices:
            self.motors[jointName] = MOTOR(jointName)

    def Act(self, t):
        for neuronName in self.nn.Get_Neuron_Names():
            if self.nn.Is_Motor_Neuron(neuronName):
                jointName = self.nn.Get_Motor_Neurons_Joint(neuronName).encode("utf-8")
                desiredAngle = self.nn.Get_Value_Of(neuronName) * c.motorJointRange
                if jointName in self.motors:
                    self.motors[jointName].Set_Value(self, desiredAngle)

    def Think(self):
        self.nn.Update()

    def Get_Fitness(self):
        stateOfLinkZero = p.getLinkState(self.robotID, 0)
        positionOfLinkZero = stateOfLinkZero[0]
        xCoordinateOfLinkZero = positionOfLinkZero[0]
        # Write fitness into a temporary file then move it to a unique fitness file.
        tmpFile = "tmp" + str(self.solutionID) + ".txt"  # NEW:
        fitnessFile = "fitness" + str(self.solutionID) + ".txt"  # NEW:
        print(f"Writing fitness to temporary file: {tmpFile}")
        with open(tmpFile, "w") as f:
            f.write(str(xCoordinateOfLinkZero))
        print(f"Moving temporary file to fitness file: {fitnessFile}")
        os.system("mv " + tmpFile + " " + fitnessFile)  # NEW:
        print(f"Fitness file written: {fitnessFile}")
        return xCoordinateOfLinkZero