import numpy as np
import math
TLocation = [0, 2]

CLocation = [10, 20]

x = [0, 0] * int(math.sqrt((TLocation[0] - CLocation[0])**2 + (TLocation[1] - CLocation[1])**2))

print(x)