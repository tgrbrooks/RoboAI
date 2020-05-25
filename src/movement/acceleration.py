import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as anim
import numpy as np

import time
import board
import digitalio
import busio
import adafruit_lis3dh

i2c = busio.I2C(board.SCL, board.SDA)
int1 = digitalio.DigitalInOut(board.D6)
lis3dh = adafruit_lis3dh.LIS3DH_I2C(i2c, int1=int1)

lis3dh.range = adafruit_lis3dh.RANGE_2_G

r = [-1,1]
X = np.array([[-1,1],[-1,1]])
Y = np.array([[-1,-1],[1,1]])
Z = np.array([[0,0],[0,0]])

fig = plt.figure()
ax = fig.gca(projection='3d')
ax.plot_surface(X, Y, Z)
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_xlim(-2, 2)
ax.set_ylim(-2, 2)
ax.set_zlim(-2, 2)

def update(i):
    x,y,z = [value/adafruit_lis3dh.STANDARD_GRAVITY for value in lis3dh.acceleration]
    X = np.array([[-1+x, 1+x], [-1+x, 1+x]])
    Y = np.array([[-1+y, -1+y], [1+y, 1+y]])
    Z = np.array([[z, z], [z, z]])
    ax.clear()
    ax.plot_surface(X, Y, Z)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_xlim(-2, 2)
    ax.set_ylim(-2, 2)
    ax.set_zlim(-2, 2)
    
a = anim.FuncAnimation(fig, update)
plt.show()
    
