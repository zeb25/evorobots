import pybullet as p
import time

physicsClient = p.connect(p.GUI)
p.loadSDF("box.sdf")

for i in range(1000):
	print(f"Step: {i}")
	p.stepSimulation()
	time.sleep(1/60)

p.disconnect()
