import numpy as np
import math
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator

cubeStateDict = {'BPortal0': 5, 'BPortal1' : 6, 'BPyramid' : 10, 'BLine' : 6, 'RPortal0' : 5, 'RPortal1' : 6, 'RPyramid' : 10, 'RLine' : 6}
objStateDict = {'ScaleB': 0, 'ScaleR' : 0, 'BSwitchB' : 0, 'BSwitchR' : 0, 'RSwitchB' : 0, 'RSwitchR' : 0} #For Switches first 'R' of 'B' is side of field, second 'R' or 'B' is side of switch 
#Locations are used for both Blue and Red Elements, but for Blue Elements the x coordinate i subtracted from 648 (except for line since either team can take from there)
cubeLocationDict = {'Portal0' : [636, 308], 'Portal1' : [8, 636], 'Pyramid' : [88, 160], 'RLine' : [208, 160], 'BLine' : [432, 160]} #0 is Top Portal
objLocationDict = {'ScaleTop': 0, 'ScaleBottom' : 0, 'CloseSwitchTop' : 0, 'CloseSwitchTop' : 0, 'FarSwitchTop' : 0, 'FarSwitchBottom' : 0}
mainStartingLocations = [[0, 80], [0, 160], [0, 240]]
gameLength = 10 #seconds


class Robot:
  name = "" #name of the robot
  
  def __init__(self, RID, robotSpeed = 120, scaleSpeed = 6, switchSpeed = 3, pickUpSpeed = 2, hasCube = False): #contructor, 
    self.RID = RID #RID = Robot ID in form [a,b] where a is team(Blue = 0, Red = 1) and a is bot id(0, 1, or 2)
    self.robotSpeed = robotSpeed #inches per second
    self.scaleSpeed = scaleSpeed #seconds
    self.switchSpeed = switchSpeed #seconds
    self.pickUpSpeed = pickUpSpeed #seconds
    self.hasCube = hasCube #Boolean has cube
    if RID[0] == 0:
      self.location = [648 - mainStartingLocations[RID[1]][0], mainStartingLocations[RID[1]][1]]
    else:
      self.location = mainStartingLocations[RID[1]]
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
  return [0, 0] * abs(TLocation - CLocation)

  
def Strategy0(robot): #returns list [d, theta, ObjChange, CubeChange]
  if robot.hasCube != True:
    closestCube = None
    #testing each cube and finding the closest one
    for cubeLocation in cubeLocationDict:
      stepsList = pathfinding(robot.location, cubeLocation.values)
      distance = len(stepsList)
      if distance > closestCube.values:
        closestCube = cubeLocation
    directions = pathfinding(robot.location, closestCube.values)
  else:
    print("I have a cube")
  coordinateChange = [robot.robotSpeed, 0]
  objChange = 'ScaleR'
  cubeChange = ''
  fieldChange = [objChange, cubeChange]
  return coordinateChange, fieldChange

#Defining all of the robots and a list of the robots  
B0 = Robot(RID = [0, 0])
B1 = Robot(RID = [0, 1])
B2 = Robot(RID = [0, 2])
R0 = Robot(RID = [1, 0])
R1 = Robot(RID = [1, 1])
R2 = Robot(RID = [1, 2])
RobotList = [B0, B1, B2, R0, R1, R2]

#Making the field plot
plt.ion()
field = plt.imread('Field.png') #get image
fig, ax = plt.subplots() #make window
ax.imshow(field, extent = [0, 648, 0 , 320]) #show image with dimensions 648 x 320
ax.set_xticks(np.arange(0, 648, 48)) #customize tick intervals
ax.set_yticks(np.arange(0, 320, 48))
ax.yaxis.set_minor_locator(AutoMinorLocator(12)) #customize minor tick intervals
ax.xaxis.set_minor_locator(AutoMinorLocator(12))
ax.grid(color='black', which='both', linestyle='-', linewidth=.05) #add grid
#minor ticks are every 18" and major ticks are every 72"

for time in range(gameLength): #The code that runs each second
  print([robot.location for robot in RobotList])
  if 'red' in globals(): red.remove()
  if 'blue' in globals(): blue.remove()

  red = ax.scatter([robot.location[0] + 2 for robot in RobotList[3:]], [robot.location[1] + 2 for robot in RobotList[3:]], s = 3, c = 'red')
  blue = ax.scatter([robot.location[0] - 2 for robot in RobotList[:3]], [robot.location[1] - 2 for robot in RobotList[:3]], s = 3, c = 'blue'); plt.pause(0.01)
  for robot in RobotList:
    vector, fieldChange = Strategy0(robot) #get the projected movement vector and projected changes to field elements
    coordinates = convertToRect(vector[0], vector[1]) #covert polar vector to rectangular
    print(coordinates) #print for debugging
    for index in range(len(robot.location)): #Changes robot location
      if robot.RID[0] == 1:
        robot.location[index] = robot.location[index] + coordinates[index]
      if robot.RID[0] == 0:
        robot.location[index] = robot.location[index] - coordinates[index]
    if fieldChange[0] != '': #Changes field element dictionaries
      objStateDict[fieldChange[0]] += 1
    if fieldChange[1] != '':
      cubeStateDict[fieldChange[1]]
  
plt.ioff(); plt.show()
    



