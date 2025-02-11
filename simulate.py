import pybullet as p
import time
import pybullet_data
import pyrosim.pyrosim as pyrosim
import numpy as numpy

physicsClient = p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())

p.configureDebugVisualizer(p.COV_ENABLE_GUI, 0)

p.setGravity(0,0,-9.8,physicsClient)

planeId = p.loadURDF("plane.urdf")
robotId = p.loadURDF("body.urdf")

p.loadSDF("world.sdf")

pyrosim.Prepare_To_Simulate(robotId)

backLegSensorValues = numpy.zeros(1000)
frontLegSensorValues = numpy.zeros(1000)

for i in range(1000):
	p.stepSimulation()
	backLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("BackLeg")
	print("backleg sensor value: ")
	print(backLegSensorValues[i])
	
	frontLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("FrontLeg")
	print("frontleg sensor value: ")
	print(frontLegSensorValues[i])
	time.sleep(1/60)

p.disconnect()
numpy.save("data/back_leg_sensor_values.npy", backLegSensorValues)
numpy.save("data/front_leg_sensor_values.npy", frontLegSensorValues)
