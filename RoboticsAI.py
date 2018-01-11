import numpy as np
import math

cubeDict = {'BPortal0': 5, 'BPortal1' : 6, 'BPyramid' : 10, 'BLine' : 6, 'RPortal0' : 5, 'RPortal1' : 6, 'RPyramid' : 10, 'RLine' : 6}
objDict = {'ScaleB': 0, 'ScaleR' : 0, 'BSwitchB' : 0, 'BSwitchR' : 0, 'RSwitchB' : 0, 'RSwitchR' : 0} #For Switches first 'R' of 'B' is side of field, second 'R' or 'B' is side of switch 
gameLength = 10 #seconds


class Robot:
  RID = None #RID = Robot ID in form [a,b] where a is team(Blue = 0, Red = 1) and a is bot id(0, 1, or 2)
  robotSpeed = None #inches per second
  scaleSpeed = None #seconds
  switchSpeed = None #seconds
  pickUpSpeed = None #seconds
  location = None #Cartesian Coordinate System
  hasCube = None #Boolean has cube
  name = "" #name of the robot
  
  def __init__(self, RID, robotSpeed = 120, scaleSpeed = 6, switchSpeed = 3, pickUpSpeed = 2, hasCube = False): #contructor, 
    self.RID = RID
    self.robotSpeed = robotSpeed
    self.scaleSpeed = scaleSpeed
    self.switchSpeed = switchSpeed
    self.pickUpSpeed = pickUpSpeed
    self.hasCube = hasCube
    self.location = [np.random.randint(0,10), np.random.randint(0,10)]
    if RID[0] == 0:
      self.name = self.name + 'B'
    elif RID[0] == 1:
      self.name = self.name + 'R'
    else:
      raise ValueError('Value given for RID[0]() was out of range')
    if 0 <= RID[1] <= 2:
      self.name = self.name + str(RID[1])
    else:
      raise ValueError('Value given for RID[1] is out of range')
  
#Convert from polar to cartesian system
def convertToRect(r, a): # radius, a = angle (radians) 
  x = r * math.cos(a)
  y = r * math.sin(a)
  return [x,y]


def pathfinding(CLocation, TLocation): #CLocation = CurrentLocation, TLocation = TargetLocation
  slope = (TLocation[1] - CLocation[1]) / (TLocation[0] - CLocation[0])
  angle = math.tan()

  
def Strategy0(robot): #returns list [d, theta, ObjChange, CubeChange]
#  if robot.HasCube != True:
#    for cubelocation in CubeDict:
#      robotlocation = robot.location
#      while robotlocation != cubelocation:
#        vector = pathfinding(robotlocation, cubelocation)
#        for i in len(robotlocation):
#          robotlocation[i] = robotlocation[i] + vector[i]  
#  else:
#    print("I have a cube")
  coordinateChange = [10, math.pi]
  objChange = 'ScaleR'
  cubeChange = ''
  fieldChange = [objChange, cubeChange]
  return coordinateChange, fieldChange

    
B0 = Robot(RID = [0, 0])
B1 = Robot(RID = [0, 1])
B2 = Robot(RID = [0, 2])
R0 = Robot(RID = [1, 0])
R1 = Robot(RID = [1, 1])
R2 = Robot(RID = [1, 2])
RobotList = [B0, B1, B2, R0, R1, R2]

if __name__ == "__main__": # Start Here
  for time in range(gameLength): #The code that runs each second
    for robot in RobotList: 
      vector, fieldChange = Strategy0(robot)
      coordinates = convertToRect(vector[0], vector[1])
      for index in range(len(robot.location)): #Changes robot location
        robot.location[index] = robot.location[index] + coordinates[index]
      if fieldChange[0] != '': #Changes field element dictionaries
        objDict[fieldChange[0]] += 1
      if fieldChange[1] != '':
        cubeDict[fieldChange[1]]
  
  print('Done')
    
