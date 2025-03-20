# solution.py
import numpy as np
import os
import pyrosim.pyrosim as pyrosim
import random
import time

class SOLUTION:
    def __init__(self, myID):  # NEW: Accept a unique ID argument.
        self.myID = myID  # NEW:
        self.weights = np.random.rand(3, 2)
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
        pyrosim.Send_Cube(name="Box", pos=[x, y, z], size=[length, width, height])
        pyrosim.End()

    def Create_Body(self):
        length, width, height = 1, 1, 1
        pyrosim.Start_URDF("body.urdf")
        pyrosim.Send_Cube(name="Torso", pos=[0, 0, 1.5], size=[length, width, height])
        pyrosim.Send_Cube(name="BackLeg", pos=[-0.5, 0, -0.5], size=[length, width, height])
        pyrosim.Send_Cube(name="FrontLeg", pos=[0.5, 0, -0.5], size=[length, width, height])
        pyrosim.Send_Joint(name="Torso_BackLeg", parent="Torso", child="BackLeg", type="revolute", position=[-0.5, 0, 1])
        pyrosim.Send_Joint(name="Torso_FrontLeg", parent="Torso", child="FrontLeg", type="revolute", position=[0.5, 0, 1])
        pyrosim.End()

    def Create_Brain(self):
        brainFileName = "brain" + str(self.myID) + ".nndf"  # NEW: Use unique filename
        pyrosim.Start_NeuralNetwork(brainFileName)
        # Sensor neurons
        pyrosim.Send_Sensor_Neuron(name="0", linkName="Torso")
        pyrosim.Send_Sensor_Neuron(name="1", linkName="BackLeg")
        pyrosim.Send_Sensor_Neuron(name="2", linkName="FrontLeg")
        # Motor neurons (names start at 3)
        pyrosim.Send_Motor_Neuron(name="3", jointName="Torso_BackLeg")
        pyrosim.Send_Motor_Neuron(name="4", jointName="Torso_FrontLeg")
        for currentRow in range(3):
            for currentColumn in range(2):
                weight = self.weights[currentRow][currentColumn]
                pyrosim.Send_Synapse(sourceNeuronName=str(currentRow), targetNeuronName=str(currentColumn + 3), weight=weight)
        pyrosim.End()
        print(f"Brain file created: {brainFileName}")


    def Mutate(self):  # NEW:
        randomRow = random.randint(0, 2)
        randomColumn = random.randint(0, 1)
        self.weights[randomRow, randomColumn] = random.random() * 2 - 1