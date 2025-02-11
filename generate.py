import pyrosim.pyrosim as pyrosim

def Create_World():
    pyrosim.Start_SDF("world.sdf")

    length = 1
    width = 1
    height = 1

    x = -2
    y = 2
    z = 0.5

    pyrosim.Send_Cube(name="Box", pos=[x,y,z] , size=[length, width, height])

    pyrosim.End()

def Create_Robot():
    pyrosim.Start_URDF("body.urdf")

    pyrosim.Send_Cube(name="Torso", pos=[1.5,0,1.5] , size=[1, 1, 1]) # send Torso

    pyrosim.Send_Joint( name = "Torso_FrontLeg" , parent= "Torso" , child = "FrontLeg" , type = "revolute", position = [2,0,1]) # connect FrontLeg to Torso

    pyrosim.Send_Cube(name="FrontLeg", pos=[.5,0,-.5] , size=[1, 1, 1]) # send FrontLeg

    pyrosim.Send_Joint( name = "Torso_BackLeg" , parent= "Torso" , child = "BackLeg" , type = "revolute", position = [1,0,1]) # connect BackLeg to Torso

    pyrosim.Send_Cube(name="BackLeg", pos=[-.5,0,-.5] , size=[1, 1, 1]) # send BackLeg

    pyrosim.End()

Create_World()
Create_Robot()
