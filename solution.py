# solution.py
import numpy as np
import os
import pyrosim.pyrosim as pyrosim
import random
import time
import constants as c  # NEW: Import constants for simulation parameters

class SOLUTION:
    def __init__(self, myID):  # NEW: Accept a unique ID argument.
        self.myID = myID  # NEW:
        self.weights = np.random.rand(c.numSensorNeurons, c.numMotorNeurons)
        self.weights = self.weights * 2 - 1

    def Set_ID(self, newID):  # NEW: Update the solution's unique ID.
        self.myID = newID

    def Start_Simulation(self, mode):  # NEW:
        self.Create_World()
        self.Create_Body()
        self.Create_Brain()
        # Build a command string that passes mode and this solution's unique ID to simulate.py.
        cmd = "python simulate.py " + mode + " " + str(self.myID) + " &"  # NEW:
        # print("Command:", cmd)  # (Optional debug)
        os.system(cmd)

    def Wait_For_Simulation_To_End(self):  # NEW:
        fitnessFileName = "fitness" + str(self.myID) + ".txt"  # NEW:
        while not os.path.exists(fitnessFileName):
            time.sleep(0.01)
        with open(fitnessFileName, "r") as fitnessFile:
            fitnessStr = fitnessFile.read().strip()
        self.fitness = float(fitnessStr)
        print("Solution", self.myID, "fitness:", self.fitness)  # NEW: For verification
        os.system("rm " + fitnessFileName)  # NEW: Clean up the fitness file

    def Evaluate(self, mode):  # (Optional convenience method – not used in PHC now)
        self.Start_Simulation(mode)
        self.Wait_For_Simulation_To_End()

    def Create_World(self):
        length, width, height = 1, 1, 1
        x, y, z = -3, 3, 0.5
        pyrosim.Start_SDF("world.sdf")
        # pyrosim.Send_Cube(name="Box", pos=[x, y, z], size=[length, width, height])
        pyrosim.End()

    def Create_Body(self):
        length, width, height = 1, 1, 1
        pyrosim.Start_URDF("body.urdf")
        pyrosim.Send_Cube(name="Torso", pos=[0, 0, 1], size=[length, width, height])
        pyrosim.Send_Cube(name="BackLeg", pos=[0, -0.5, 0], size=[0.2,1,0.2])
        pyrosim.Send_Cube(name="FrontLeg", pos=[0, .5, 0], size=[0.2,1,0.2])
        pyrosim.Send_Cube(name="LeftLeg", pos=[-.5, 0, 0], size=[1,0.2,0.2])
        pyrosim.Send_Cube(name="RightLeg", pos=[.5, 0, 0], size=[1,0.2,0.2])
        pyrosim.Send_Joint(name="Torso_BackLeg", parent="Torso", child="BackLeg", type="revolute", position=[0, -.5, 1], jointAxis = "1 0 0")
        pyrosim.Send_Joint(name="Torso_FrontLeg", parent="Torso", child="FrontLeg", type="revolute", position=[0, .5, 1], jointAxis = "1 0 0")
        pyrosim.Send_Joint(name="Torso_LeftLeg", parent="Torso", child="LeftLeg", type="revolute", position=[-.5, 0, 1], jointAxis = "0 1 0")
        pyrosim.Send_Joint(name="Torso_RightLeg", parent="Torso", child="RightLeg", type="revolute", position=[.5, 0, 1], jointAxis = "0 1 0")
        # --- Lower legs ---

        # Front lower leg (attached to FrontLeg)
        pyrosim.Send_Cube(
            name="FrontLowerLeg", 
            pos=[0, 0, -.5],       # relative to FrontLeg’s frame
            size=[0.2, .2, 1]       # small in x (length), medium in y (width), small in z (height)
        )
        pyrosim.Send_Joint(
            name="FrontLeg_FrontLowerLeg",
            parent="FrontLeg",
            child="FrontLowerLeg",
            type="revolute",
            position=[0, 1, 0],      # joint position at the end of FrontLeg
            jointAxis="1 0 0"        # rotates through the y/z plane
        )

        # Back lower leg (attached to BackLeg)
        pyrosim.Send_Cube(
            name="BackLowerLeg", 
            pos=[0, 0, -.5],      # relative to BackLeg’s frame
            size=[0.2, 0.2, 1]
        )
        pyrosim.Send_Joint(
            name="BackLeg_BackLowerLeg",
            parent="BackLeg",
            child="BackLowerLeg",
            type="revolute",
            position=[0, -1, 0],
            jointAxis="1 0 0"
        )

        # Left lower leg (attached to LeftLeg)
        pyrosim.Send_Cube(
            name="LeftLowerLeg", 
            pos=[0, 0, -.5],      # relative to LeftLeg’s frame
            size=[.2, 0.2, 1]
        )
        pyrosim.Send_Joint(
            name="LeftLeg_LeftLowerLeg",
            parent="LeftLeg",
            child="LeftLowerLeg",
            type="revolute",
            position=[-1, 0, 0],
            jointAxis="0 1 0"
        )

        # Right lower leg (attached to RightLeg)
        pyrosim.Send_Cube(name="RightLowerLeg", pos=[0, 0, -.5], size=[0.2, 0.2, 1])
        pyrosim.Send_Joint(name="RightLeg_RightLowerLeg", parent="RightLeg", child="RightLowerLeg", type="revolute", position=[1, 0, 0], jointAxis="0 1 0")
        pyrosim.End()

    def Create_Brain(self):
        brainFileName = "brain" + str(self.myID) + ".nndf"  # NEW: Use unique filename
        pyrosim.Start_NeuralNetwork(brainFileName)
        # Sensor neurons
        pyrosim.Send_Sensor_Neuron(name="0", linkName="FrontLowerLeg")
        pyrosim.Send_Sensor_Neuron(name="1", linkName="BackLowerLeg")
        pyrosim.Send_Sensor_Neuron(name="2", linkName="LeftLowerLeg")
        pyrosim.Send_Sensor_Neuron(name="3", linkName="RightLowerLeg")


        # Motor neurons (names start at 3)
        pyrosim.Send_Motor_Neuron(name="4", jointName="Torso_BackLeg")
        pyrosim.Send_Motor_Neuron(name="5", jointName="Torso_FrontLeg")
        pyrosim.Send_Motor_Neuron(name="6", jointName="Torso_LeftLeg")
        pyrosim.Send_Motor_Neuron(name="7", jointName="Torso_RightLeg")
        pyrosim.Send_Motor_Neuron(name="8", jointName="FrontLeg_FrontLowerLeg")
        pyrosim.Send_Motor_Neuron(name="9", jointName="BackLeg_BackLowerLeg")
        pyrosim.Send_Motor_Neuron(name="10", jointName="LeftLeg_LeftLowerLeg")
        pyrosim.Send_Motor_Neuron(name="11", jointName="RightLeg_RightLowerLeg")

        for currentRow in range(c.numSensorNeurons):
            for currentColumn in range(c.numMotorNeurons):
                weight = self.weights[currentRow][currentColumn]
                pyrosim.Send_Synapse(sourceNeuronName=str(currentRow), targetNeuronName=str(currentColumn + c.numSensorNeurons), weight=weight)
        pyrosim.End()
        
    def Mutate(self):  # NEW:
        randomRow = random.randint(0, c.numSensorNeurons-1)
        randomColumn = random.randint(0, c.numMotorNeurons-1)
        self.weights[randomRow, randomColumn] = random.random() * 2 - 1