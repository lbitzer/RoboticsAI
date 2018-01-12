import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator
import matplotlib.animation as animation
import time

#Making the field plot
plt.ion()
fig, ax = plt.subplots() #make window
ax.set_xticks(np.arange(0, 648, 48)) #customize tick intervals
ax.set_yticks(np.arange(0, 320, 48))
ax.yaxis.set_minor_locator(AutoMinorLocator(6)) #customize minor tick intervals
ax.xaxis.set_minor_locator(AutoMinorLocator(6))
ax.grid(color='black', which='both', linestyle='-', linewidth=.05) #add grid
x = [10, 20, 30]
y = [10, 20, 30]



for i in range(4):
	for j in range(len(x)):
		x[j] = x[j] * (i + 1)
	time.sleep(1)
	fig.canvas.draw()
plt.show()
#minor ticks are every 18" and major ticks are every 72"