import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import AutoMinorLocator

X_BOUND = [0, 5]

plt.ion()
field = plt.imread('Field.png') #get image
fig, ax = plt.subplots() #make window
ax.imshow(field, extent = [0, 648, 0 , 320]) #show image with dimensions 648 x 320
ax.set_xticks(np.arange(0, 648, 48)) #customize tick intervals
ax.set_yticks(np.arange(0, 320, 48))
ax.yaxis.set_minor_locator(AutoMinorLocator(12)) #customize minor tick intervals
ax.xaxis.set_minor_locator(AutoMinorLocator(12))
ax.grid(color='black', which='both', linestyle='-', linewidth=.05) #add grid


F_values = [2,3,4,5,6,7,8,9]
for i in range(10):
	for j in range(len(F_values)):
		F_values[j] = F_values[j] + i
	if 'sca' in globals(): sca.remove()
	sca = plt.scatter(F_values, F_values, s=3, lw=0, c='red', alpha=0.5); plt.pause(0.05)

plt.ioff(); plt.show()
