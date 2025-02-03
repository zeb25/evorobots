import pyrosim.pyrosim as pyrosim
pyrosim.Start_SDF("boxes.sdf")

length = 1
width = 1
height = 1

x_start = 0
y_start = 0
z_start = height / 2

rows = 5
columns = 5
tower_height = 10

for row in range(rows):
	for column in range(columns):
		z = z_start
		curr_length = length
		curr_width = width 
		curr_height = height

		for level in range(tower_height):
			x = x_start + row * length
			y = y_start + column * length
		
			pyrosim.Send_Cube(name=f"Box_{row}_{column}_{level}", pos=[x,y,z] , size=[curr_length,curr_width,curr_height])
			z += height
			curr_length *= 0.9
			curr_width *= 0.9
			curr_height *= 0.9

pyrosim.End()
