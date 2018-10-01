import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

plt.ion()
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

for k in xrange(0,X_range):
    ax.plot(x_input, y_input, z_input)
    plt.draw()
    plt.pause(0.02)
    ax.cla()