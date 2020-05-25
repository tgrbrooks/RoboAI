import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as anim
import numpy as np
import math

import time
import board
import digitalio
import busio
import adafruit_lis3dh

def dist(a, b):
    return math.sqrt((a*a) + (b*b))

def get_y_rotation(x, y, z):
    return -math.atan2(x, dist(y, z))

def get_x_rotation(x, y, z):
    return math.atan2(y, dist(x, z))

i2c = busio.I2C(board.SCL, board.SDA)
int1 = digitalio.DigitalInOut(board.D6)
lis3dh = adafruit_lis3dh.LIS3DH_I2C(i2c, int1=int1)

lis3dh.range = adafruit_lis3dh.RANGE_2_G

x_arr = np.array([-1,1,-1,1])
y_arr = np.array([-1,-1,1,1])
z_arr = np.zeros(4)
all_arr = np.array([x_arr, y_arr, z_arr])
X = x_arr.reshape(2, 2)
Y = y_arr.reshape(2, 2)
Z = z_arr.reshape(2, 2)

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
    x_rot = get_x_rotation(x, y, z)
    y_rot = get_y_rotation(x, y, z)
    Rx = np.array([[1, 0, 0],
                   [0, math.cos(x_rot), -math.sin(x_rot)],
                   [0, math.sin(x_rot), math.cos(x_rot)]])
    Ry = np.array([[math.cos(y_rot), 0, math.sin(y_rot)],
                   [0, 1, 0],
                   [-math.sin(y_rot), 0, math.cos(y_rot)]])
    R = Ry.dot(Rx)
    rotated = R.dot(all_arr)
    X = rotated[0].reshape(2, 2)
    Y = rotated[1].reshape(2, 2)
    Z = rotated[2].reshape(2, 2)
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
    
