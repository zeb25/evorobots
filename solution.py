import random
import numpy as np
import pyrosim.pyrosim as pyrosim
import os


class SOLUTION:
    def __init__(self):
        self.weights = np.random.rand(3, 2)  # Generate values in range [0,1]
        self.weights = self.weights * 2 - 1  # Scale to range [-1, +1]

    def Evaluate(self, directOrGUI):
        self.Create_World()
        self.Create_Body()
        self.Create_Brain()
        os.system("python simulate.py " + str(directOrGUI))
        fitnessFile=open("data/fitness.txt","r")
        self.fitness=float(fitnessFile.read())
        fitnessFile.close()

    def Create_World(self):
        pyrosim.Start_SDF("world.sdf")
        pyrosim.End()

    def Create_Body(self):

        length, width, height = 1, 1, 1  # NEW:
        pyrosim.Start_URDF("body.urdf")  # NEW:
        pyrosim.Send_Cube(name="Torso", pos=[0, 0, 1.5], size=[length, width, height])  # NEW:
        pyrosim.Send_Cube(name="BackLeg", pos=[-0.5, 0, -0.5], size=[length, width, height])  # NEW:
        pyrosim.Send_Cube(name="FrontLeg", pos=[0.5, 0, -0.5], size=[length, width, height])  # NEW:
        pyrosim.Send_Joint(name="Torso_BackLeg", parent="Torso", child="BackLeg", type="revolute", position=[-0.5, 0, 1])  # NEW:
        pyrosim.Send_Joint(name="Torso_FrontLeg", parent="Torso", child="FrontLeg", type="revolute", position=[0.5, 0, 1])  # NEW:
        pyrosim.End()  # NEW:
    

    def Create_Brain(self):
        pyrosim.Start_NeuralNetwork("brain.nndf")
        
        pyrosim.Send_Sensor_Neuron(name = 0 , linkName = "Torso")
        pyrosim.Send_Sensor_Neuron(name = 1 , linkName = "BackLeg")
        pyrosim.Send_Sensor_Neuron(name = 2 , linkName = "FrontLeg")
        pyrosim.Send_Motor_Neuron( name = 3 , jointName = "Torso_BackLeg")
        pyrosim.Send_Motor_Neuron( name = 4 , jointName = "Torso_FrontLeg")

        for currentRow in range(3):
            for currentColumn in range(2):
                pyrosim.Send_Synapse(sourceNeuronName=currentRow, targetNeuronName=currentColumn+3, weight=self.weights[currentRow][currentColumn])

        pyrosim.End()

    def Mutate(self):
            randomRow=random.randint(0,2)
            randomColumn=random.randint(0,1)
            self.weights[randomRow,randomColumn]=random.random()*2-1