class Robot:
  name = "" #name of the robot
  
  def __init__(self, RID, robotSpeed = 120, scaleSpeed = 6, switchSpeed = 3, pickUpSpeed = 2, hasCube = False): #contructor, 
    self.RID = RID #RID = Robot ID in form [a,b] where a is team(Blue = 0, Red = 1) and a is bot id(0, 1, or 2)
    self.robotSpeed = robotSpeed #inches per second
    self.scaleSpeed = scaleSpeed #seconds
    self.switchSpeed = switchSpeed #seconds
    self.pickUpSpeed = pickUpSpeed #seconds
    self.hasCube = hasCube #Boolean has cube

B0 = Robot(RID = [0, 0])
B1 = Robot(RID = [0, 1])
B2 = Robot(RID = [0, 2])
R0 = Robot(RID = [1, 0])
R1 = Robot(RID = [1, 1])
R2 = Robot(RID = [1, 2])

print(B0.__name__)