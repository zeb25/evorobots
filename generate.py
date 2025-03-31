import pyrosim.pyrosim as pyrosim  # Import the Pyrosim library for simulation file generation
import random  # Import the random library for generating random synapse weights

def Create_World():
    """
    Creates the simulation world.
    """
    pyrosim.Start_SDF("world.sdf")  # Start defining the world file
    pyrosim.End()  # End the world file definition

def Generate_Body():
    """
    Creates the robot's body.

    This function generates a URDF file (`body.urdf`) that defines the robot's structure.
    The robot consists of a torso and two legs (front and back) connected by revolute joints.
    """
    pyrosim.Start_URDF("body.urdf")  # Start defining the robot's body file

    # Define the torso of the robot
    pyrosim.Send_Cube(name="Torso", pos=[1.5, 0, 1.5], size=[1, 1, 1])  # Add the torso cube

    # Define the front leg and its joint
    pyrosim.Send_Joint(name="Torso_FrontLeg", parent="Torso", child="FrontLeg", 
                       type="revolute", position=[2, 0, 1])  # Connect the front leg to the torso
    pyrosim.Send_Cube(name="FrontLeg", pos=[0.5, 0, -0.5], size=[1, 1, 1])  # Add the front leg cube

    # Define the back leg and its joint
    pyrosim.Send_Joint(name="Torso_BackLeg", parent="Torso", child="BackLeg", 
                       type="revolute", position=[1, 0, 1])  # Connect the back leg to the torso
    pyrosim.Send_Cube(name="BackLeg", pos=[-0.5, 0, -0.5], size=[1, 1, 1])  # Add the back leg cube

    pyrosim.End()  # End the robot body file definition

def Generate_Brain():
    """
    Creates the robot's neural network (brain).

    This function generates a neural network file (`brain.nndf`) that defines the robot's control system.
    The brain consists of sensor neurons, motor neurons, and synapses connecting them.
    """
    pyrosim.Start_NeuralNetwork("brain.nndf")  # Start defining the neural network file

    # Define sensor neurons for the robot's links
    pyrosim.Send_Sensor_Neuron(name=0, linkName="Torso")  # Sensor neuron for the torso
    pyrosim.Send_Sensor_Neuron(name=1, linkName="BackLeg")  # Sensor neuron for the back leg
    pyrosim.Send_Sensor_Neuron(name=2, linkName="FrontLeg")  # Sensor neuron for the front leg

    # Define motor neurons for the robot's joints
    pyrosim.Send_Motor_Neuron(name=3, jointName="Torso_BackLeg")  # Motor neuron for the back leg joint
    pyrosim.Send_Motor_Neuron(name=4, jointName="Torso_FrontLeg")  # Motor neuron for the front leg joint

    # Define synapses connecting sensor neurons to motor neurons with predefined weights
    pyrosim.Send_Synapse(sourceNeuronName=0, targetNeuronName=3, weight=-1.0)  # Torso -> BackLeg
    pyrosim.Send_Synapse(sourceNeuronName=1, targetNeuronName=3, weight=-0.9996)  # BackLeg -> BackLeg
    pyrosim.Send_Synapse(sourceNeuronName=0, targetNeuronName=4, weight=-1.0)  # Torso -> FrontLeg
    pyrosim.Send_Synapse(sourceNeuronName=2, targetNeuronName=4, weight=-1.0)  # FrontLeg -> FrontLeg

    # Add random synapses between all sensor and motor neurons
    for i in range(0, 3):  # Iterate over sensor neurons
        for j in range(0, 5):  # Iterate over motor neurons
            pyrosim.Send_Synapse(sourceNeuronName=i, targetNeuronName=j, weight=random.uniform(-1, 1))  # Random weight

    pyrosim.End()  # End the neural network file definition

Create_World()  # Create the world file
Generate_Body()  # Create the robot body file
Generate_Brain()  # Create the robot brain file