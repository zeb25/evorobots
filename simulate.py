import pybullet as p
import time
import pybullet_data
import pyrosim.pyrosim as pyrosim
import numpy as numpy
import random
import math
import constants as c

physicsClient = p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())

p.configureDebugVisualizer(p.COV_ENABLE_GUI, 0)

p.setGravity(0,0,c.GRAVITY,physicsClient)

planeId = p.loadURDF("plane.urdf")
robotId = p.loadURDF("body.urdf")

p.loadSDF("world.sdf")
pyrosim.Prepare_To_Simulate(robotId)

backLegSensorValues = numpy.zeros(c.ITERATIONS)
frontLegSensorValues = numpy.zeros(c.ITERATIONS)

# Create a sinusoidal wave ranging from [0, 2π]
time_steps = numpy.linspace(0, 2 * math.pi, c.ITERATIONS)


# Generate sinusoidal values mapped to [-π/2, π/2]
targetAngles = c.AMPLITUDE * numpy.sin(c.FREQUENCY * time_steps + c.PHASE_OFFSET)
targetAngles2 = c.AMPLITUDE_2 * numpy.sin(c.FREQUENCY_2 * time_steps + c.PHASE_OFFSET_2)

for i in range(c.ITERATIONS):
	p.stepSimulation()

	backLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("BackLeg")
	print("backleg sensor value: ", backLegSensorValues[i])
	
	frontLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("FrontLeg")
	print("frontleg sensor value: ", frontLegSensorValues[i])
	
	targetPositionBack = targetAngles[i]
	targetPositionFront = -targetAngles[i]
    
	pyrosim.Set_Motor_For_Joint(
			bodyIndex = robotId,
			jointName = b'Torso_BackLeg',
			controlMode = p.POSITION_CONTROL,
			targetPosition = targetAngles[i],
			maxForce = c.MAX_FORCE)
	
	pyrosim.Set_Motor_For_Joint(
			bodyIndex = robotId,
			jointName = b'Torso_FrontLeg',
			controlMode = p.POSITION_CONTROL,
			targetPosition = targetAngles2[i],
			maxForce = c.MAX_FORCE)

	time.sleep(c.TIME_STEP)

p.disconnect()
numpy.save("data/back_leg_sensor_values.npy", backLegSensorValues)
numpy.save("data/front_leg_sensor_values.npy", frontLegSensorValues)
