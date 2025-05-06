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
    """
    The ROBOT class represents the robot in the simulation.
    It manages the robot's sensors, motors, neural network, and fitness evaluation.
    """

    def __init__(self, solutionID, x=1.0):
        """
        Initializes the robot.

        Args:
            solutionID (int): A unique identifier for the solution being simulated.
            x (float): A parameter to control the frequency of the sine wave for the touch sensor.
        """
        self.solutionID = solutionID  # Store the solution ID
        self.x = x  # Store the frequency parameter for the sine wave
        self.motors = {}  # Dictionary to store motor objects
        self.sensors = {}  # Dictionary to store sensor objects

        # Load the robot's URDF file into the simulation
        self.robotID = p.loadURDF("body.urdf")

        # Prepare the robot for simulation using Pyrosim
        pyrosim.Prepare_To_Simulate(self.robotID)

        # Load the neural network for the robot using the solution ID
        brainFile = "brain" + str(solutionID) + ".nndf"
        self.nn = NEURAL_NETWORK(brainFile)

        # Delete the brain file after it is loaded
        os.system("rm " + brainFile)

        # Prepare the robot's sensors and motors
        self.Prepare_To_Sense()
        self.Prepare_To_Act()

    def Prepare_To_Sense(self):
        """
        Initializes the robot's sensors by associating them with the robot's links.
        """
        for linkName in pyrosim.linkNamesToIndices:
            self.sensors[linkName] = SENSOR(linkName)  # Create a SENSOR object for each link

    def Sense(self, t):
        """
        Collects sensor data for the current time step.
        """
        for sensor in self.sensors.values():
            sensor.Get_Value(t)  # Retrieve and store sensor values

        # Overwrite the value of one touch sensor with sin(xt)
        if self.sensors:  # Ensure there are sensors available
            first_sensor = next(iter(self.sensors.values()))  # Get the first sensor
            first_sensor.values[t] = math.sin(self.x * t)  # Overwrite with sin(xt)
            
    def Get_Sensor_Values(self, t):
        """
        Returns the values of all sensors as a dictionary.
        """
        sensorValues = {}
        for sensorName in self.sensors:
            sensorValues[sensorName] = self.sensors[sensorName].Get_Value(t)
        return sensorValues  # Return the dictionary of sensor values

    def Prepare_To_Act(self):
        """
        Initializes the robot's motors by associating them with the robot's joints.
        """
        for jointName in pyrosim.jointNamesToIndices:
            self.motors[jointName] = MOTOR(jointName)  # Create a MOTOR object for each joint

    def Act(self, t):
        """
        Actuates the robot's motors based on the neural network's output.
        """
        for neuronName in self.nn.Get_Neuron_Names():
            if self.nn.Is_Motor_Neuron(neuronName):  # Check if the neuron is a motor neuron
                jointName = self.nn.Get_Motor_Neurons_Joint(neuronName)  # Get the joint controlled by the neuron
                if isinstance(jointName, str):  # Ensure the joint name is encoded properly
                    jointName = jointName.encode("utf-8")
                desiredAngle = self.nn.Get_Value_Of(neuronName)  # Get the desired angle for the joint
                self.motors[jointName].Set_Value(self.robotID, desiredAngle)  # Set the motor value

    def Think(self):
        """
        Updates the robot's neural network to process sensor data and compute motor outputs.
        """
        self.nn.Update()