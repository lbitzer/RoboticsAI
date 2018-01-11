import numpy as np
import matplotlib.pyplot as plt


field = plt.imread('Field.png')
fig, ax = plt.subplots()
ax.imshow(field, extent = [0, 648, 0 , 320])
ax.grid(color='black', which='both', linestyle='-', linewidth=.1)
plt.show()