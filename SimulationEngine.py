import numpy as np
import math
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator

#set game length in seconds
GAME_LENGTH = 5 #seconds

#randomizing switches and scales
if np.random.randint(0, 2) == 0:
  red_scale = 'ScaleTop'
  blue_scale = 'ScaleBottom'
else:
  red_scale = 'ScaleBottom'
  blue_scale = 'ScaleTop'

if np.random. randint(0, 2) == 0:
  redside_red_switch = 'RedSwitchTop'
  redside_blue_switch = 'RedSwitchBottom'
else:
  redside_red_switch = 'RedSwitchBottom'
  redside_blue_switch = 'RedSwitchTop'

if np.random.randint(0, 2) == 0:
  blueside_red_switch = 'BlueSwitchTop'
  blueside_blue_switch = 'BlueSwitchBottom'
else:
  blueside_red_switch = 'BlueSwitchBottom'
  blueside_blue_switch = 'BlueSwitchTop'

cube_state = {'RPortal0' : 5, 'RPortal1' : 6, 'RPyramid' : 10, 'RLine' : 6, 'BPortal0': 5, 'BPortal1' : 6, 'BPyramid' : 10, 'BLine' : 6}

#For Switches first 'R' of 'B' is side of field, second 'R' or 'B' is side of switch; they're also variables because they change match to match
obj_state = {'RScale' : 0, 'BScale': 0, 'RSwitchR' : 0, 'RSwitchB' : 0, 'BSwitchR' : 0, 'BSwitchB' : 0}
#Locations are used for both Blue and Red Teams, but for Blue Elements the x coordinate is subtracted from 648 (except for line since either team can take from there)
cube_location = {'Portal0' : [636, 308], 'Portal1' : [8, 636], 'Pyramid' : [88, 160], 'RLine' : [208, 160], 'BLine' : [432, 160]} #0 is Top Portal
obj_location = {'ScaleTop': [320, 248], 'ScaleBottom' : [320, 68], 'RedSwitchTop' : [164, 236], 'RedSwitchBottom' : [164, 80], 'BlueSwitchTop' : [480, 236], 'BlueSwitchBottom' : [480, 80]}
main_starting_locations = [[0, 80], [0, 160], [0, 240]]



class Robot:
  team = '' #name of the robot
  task_timer = 0
  current_task = ''
  current_directions = []
  def __init__(self, RID, robot_speed = 144, scale_speed = 6, switch_speed = 3, pickup_speed = 2, has_cube = False): #contructor, 
    self.RID = RID #RID = Robot ID in form [a,b] where a is team(Blue = 0, Red = 1) and a is bot id(0, 1, or 2)
    self.robot_speed = robot_speed #inches per second
    self.scale_speed = scale_speed #seconds
    self.switch_speed = switch_speed #seconds
    self.pickup_speed = pickup_speed #seconds
    self.has_cube = has_cube #Boolean has cube
    #setting up staring locations
    self.location = [RID[0] * 644 - main_starting_locations[RID[1]][0], main_starting_locations[RID[1]][1]]
    
    if RID[0] == 0:
      self.team ='R'
      self.enemy = 'B'
    elif RID[0] == 1:
      self.team ='B'
      self.enemy = 'R'
    else:
      raise ValueError('Value given for RID[0](team) was out of range')
    if 0 >= RID[1] >= 2:
      raise ValueError('Value given for RID[1](robotID) is out of range')
  
#Convert from polar to cartesian system
def convert_to_rect(r, a): # radius, a = angle (radians) 
  x = r * math.cos(a)
  y = r * math.sin(a)
  return [x,y]

#cube can be any of the keys in cube_location
def get_cube_state(robot, cube): 
  if cube != 'RLine' and cube != 'BLine':
    if robot.RID[0] == 0:
      global_cube = 'R' + cube
    if robot.RID[0] == 1:
      global_cube = 'B' + cube
    return cube_state[global_cube]
  else:
    return cube_state[cube]
#if set_cube_state returns zero this location is out of cubes and the robot did not receive a cube
def set_cube_state(robot, cube):
  if cube != 'Rline' and cube != "BLine":
    if robot.RID[0] == 0:
      global_cube = 'R' + cube
    if robot.RID[0] == 1:
      global_cube = 'B' + cube
    if cube_state[global_cube] - 1 >= 0:
      cube_state[global_cube] -= 1
      return True
    else:
      return False
  else:
    if cube_state[cube] -1 >= 0:
      cube_state[cube] -= 1
      return True
    else:
      return False
#obj can be the string "Scale", ASwitch" for Allied Switch, or "OSwitch" for Opponent Switch; returns - state of allied side, state of opponent side
def get_obj_state(robot, obj): 
  if obj == "Scale":
    return obj_state[robot.team + 'Scale'], obj_state[robot.enemy + 'Scale']
  elif obj == "ASwitch":
    return obj_state[robot.team + 'Switch' + robot.team], obj_state[robot.team + 'Switch' + robot.enemy]
  elif obj == "OSwitch":
    return obj_state[robot.enemy + 'Switch' + robot.team], obj_state[robot.enemy + 'Switch' + robot.enemy]
  else:
    raise ValueError('Value given for obj is out of range(must be "Scale", "ASwitch" or "OSwitch")')

def set_obj_state(robot, obj):
  if obj == "Scale":
    global_obj = obj_state[robot.team + 'Scale']
  elif obj == "ASwitch":
    global_obj = obj_state[robot.team + 'Switch' + robot.team]
  elif obj == "OSwitch":
    global_obj = obj_state[robot.enemy + 'Switch' + robot.team]
  else:
    raise ValueError('Value given for obj is out of range(must be "Scale", "ASwitch" or "OSwitch")')
  obj_state[global_obj] += 1

def get_obj_location(robot, obj):
  if robot.RID[0] == 0:
    if obj == "Scale":
      return obj_location[red_scale]
    elif obj == "ASwitch":
      return obj_location[redside_red_switch]
    elif obj == "OSwitch":
      return obj_location[blueside_red_switch]
    else:
      raise ValueError('Value given for obj is out of range(must be "Scale", "ASwitch" or "OSwitch")')
  else:
    if obj == "Scale":
      return obj_location[blue_scale]
    elif obj == "ASwitch":
      return obj_location[blueside_blue_switch]
    elif obj == "OSwitch":
      return obj_location[redside_blue_switch]
    else:
      raise ValueError('Value given for obj is out of range(must be "Scale", "ASwitch" or "OSwitch")')


def pathfinding(CLocation, TLocation): #CLocation = CurrentLocation, TLocation = TargetLocation
  return [[1, 2]] * int(math.sqrt((TLocation[0] - CLocation[0])**2 + (TLocation[1] - CLocation[1])**2) / 20)


#All strategies should be written from the perspective of the red team
def strategy0(robot): #returns list [d, theta, ObjChange, CubeChange]
  #First convert robot location so that it is representative of the red team
  current_location = [abs(robot.RID[0]*644 - robot.location[0]), robot.location[1]] #Yes, it's supposed to be 644 not 648
  #Now if the robot doesn't have directions or a task give it one

  #If the robot doesn't have a cube find directions to the nearest one
  if robot.has_cube == False and robot.current_directions == [] and robot.current_task == '':
    #testing each cube and finding the closest one
    closest_cube = ''
    for cube in cube_location:
      if get_cube_state(robot, cube) <= 0:
        continue
      steps_list = pathfinding(current_location, cube_location[cube])
      distance = len(steps_list)
      if closest_cube == '':
        closest_cube = cube
      elif distance < len(pathfinding(current_location, cube_location[closest_cube])):
        closest_cube = cube
    robot.current_directions = pathfinding(current_location, cube_location[closest_cube]) + [closest_cube]
    robot.current_task = 'driving'
    print("No cube configured")
  #If the robot has a cube find directions to the Scaler
  elif robot.has_cube and robot.current_directions == [] and robot.current_task == '':
    robot.current_directions = pathfinding(current_location, get_obj_location(robot, 'Scale')) + ['Scale']
    robot.current_task = 'driving'
    print("Cube Configured")

  #Now execute on the current directions or task

  #If the robot doesn't have a cube and is picking it up check if it's done
  if not robot.has_cube and robot.current_task == 'cube':
    robot.task_timer -= 1
    if robot.task_timer <= 0:
      cube_exists = set_cube_state(robot, robot.current_directions[-1])
      robot.current_directions = []
      robot.current_task = ''
      robot.task_timer = 0
      if cube_exists:
        robot.has_cube = True
      else:
        robot.has_cube = False
    drive_directions = []
    print("Picking up")
  #If the robot has a cube and is placing it somewhere check if it's done
  elif robot.has_cube and robot.current_task == 'cube':
    robot.task_timer -= 1
    if robot.task_timer <= 0:
      robot.has_cube = False
      set_obj_state(robot, robot.current_directions[-1])
      robot.current_directions = []
      robot.current_task = ''
      robot.task_timer = 0
    drive_directions = []
    print("Placing")
  #If the robot is driving, check whether it will reach it's detinatino in the next second
  elif robot.current_task == 'driving':
    if len(robot.current_directions) - 1 >= int(robot.robot_speed / 4):
      drive_directions = robot.current_directions[0 : int(robot.robot_speed / 4)]
      robot.current_directions = robot.current_directions[int(robot.robot_speed / 4):]
      robot.current_task = 'driving'
    else:
      return robot.current_directions[0 : len(robot.current_directions) - 1]
      robot.current_directions = robot.current_directions[len(robot.current_directions) - 1:]
      robot.task = 'cube'
      if not robot.has_cube:
        robot.task_timer = robot.pickup_speed
      elif robot.has_cube and robot.current_directions[-1] == 'Scale':
        robot.task_timer = robot.scale_speed
      elif robot.has_cube and robot.current_directions[-1] == 'Switch':
        robot.task_timer = robot.switch_speed
      drive_directions = []
    print("driving")
  
  return drive_directions

#Defining all of the robots and a list of the robots  
R0 = Robot(RID = [0, 0])
R1 = Robot(RID = [0, 1])
R2 = Robot(RID = [0, 2])
B0 = Robot(RID = [1, 0])
B1 = Robot(RID = [1, 1])
B2 = Robot(RID = [1, 2])
robot_list = [R0, R1, R2, B0, B1, B2]

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

for time in range(GAME_LENGTH): #The code that runs each second
  print(" \n \n \n ")
  print([robot.location for robot in robot_list])
  if 'red' in globals(): red.remove()
  if 'blue' in globals(): blue.remove()

  red = ax.scatter([robot.location[0] + 2 for robot in robot_list[:3]], [robot.location[1] + 2 for robot in robot_list[3:]], s = 3, c = 'red')
  blue = ax.scatter([robot.location[0] - 2 for robot in robot_list[3:]], [robot.location[1] - 2 for robot in robot_list[:3]], s = 3, c = 'blue'); plt.pause(1)
  for robot in robot_list:
    directions = strategy0(robot) #get the projected movement vector and projected changes to field elements
    print(robot.team)
    print(len(directions))
    # if robot.RID[0] == 1:
    #   for index in range(len(directions)):
    #     directions[index][0] = 644 - directions[index][0]
    #     print(directions[index][0])
plt.ioff(); plt.show()
    



