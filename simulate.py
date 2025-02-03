import pybullet as p
import time
import pybullet_data

physicsClient = p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())

p.setGravity(0,0,-9.8,physicsClient)
planeId = p.loadURDF("plane.urdf")
p.loadSDF("boxes.sdf")

for i in range(1000):
	print(f"Step: {i}")
	p.stepSimulation()
	time.sleep(1/60)

p.disconnect()
