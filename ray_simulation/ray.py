import itertools

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

import numpy as np
from numpy.linalg import norm

## Uncomment for IPython Jupyter notebook
#from IPython.display import HTML
#%matplotlib inline

def hexgrid(spacing, ns, height, nz):
    v, w = np.array(([1, 0], [.5, -.5*np.sqrt(3)])) * spacing
    
    # Hex coordinates q, r, s such that || <= ns and q+r+s = 0
    I = range(-ns, ns+1)
    indices = [(q, r) for (q, r, s)
        in itertools.product(I, repeat=3) 
        if q+r+s == 0]
    plane = np.array([i*v + j*w for (i, j) in indices]).T

    xv, yv = np.repeat(plane, nz, axis=1)
    zv = np.tile(np.linspace(0, height, nz), plane.shape[1])

    return xv, yv, zv


xv, yv, zv = hexgrid(1, 4, 10, 10)
points = np.array([xv, yv, zv]).T

fig = plt.figure()
ax = fig.add_subplot(projection='3d')
ax.scatter(xv, yv, zv, c=zv, cmap='hsv', depthshade=False, s=200)
ax.axis("equal")
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')
plt.show()


def ICArray():
    spacing = 125
    height = 1000
    nz = 60
    ns = 5

    v, w = np.array(([1, 0], [.5, -.5*np.sqrt(3)])) * spacing
    
    remove = [(-1, -4), (0, -5), (5, -5), (5, -4), (5, -3), (5, -2),
        (5, -1), (5, 0), (4, 1), (3, 2), (2, 3), (1, 4), (0, 5)]
    # Hex coordinates q, r, s such that || <= ns and q+r+s = 0
    I = range(-ns, ns+1)
    indices = [(q, r) for (q, r, s)
        in itertools.product(I, repeat=3) 
        if q+r+s == 0 and (q, r) not in remove]
    plane = np.array([i*v + j*w for (i, j) in indices]).T

    xv, yv = np.repeat(plane, nz, axis=1)
    zv = np.tile(np.linspace(0, height, nz), plane.shape[1])

    return xv, yv, zv


xv, yv, zv = ICArray()
points = np.array([xv, yv, zv]).T

fig = plt.figure()
ax = fig.add_subplot(projection='3d')
ax.scatter(xv, yv, zv, c=zv, cmap='hsv', depthshade=False, s=200)
ax.axis("equal")
ax.view_init(90, -90) # Camera angle
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')
plt.show()


def normalize(vec):
    return vec / norm(vec)

def in_cylinder(points, base, direction, radius, length):
    d = normalize(direction)
    radial_dist = norm(np.cross(points-base, d), axis=1)
    dist = np.dot(points-base, d)
    return (radial_dist <= radius) & (0 <= dist) & (dist <= length) 

def from_angles(theta, phi):
    x = np.sin(theta)*np.cos(phi)
    y = np.sin(theta)*np.sin(phi)
    z = np.cos(theta)
    return np.array([x, y, z])


# Data from IceCube Website
a = 125
zmax = 1000

xv, yv, zv = ICArray()
points = np.array([xv, yv, zv]).T
direction = from_angles(np.radians(30), np.radians(70))
base = np.array([0, -4*a, 0]) - zmax/2*direction

D = in_cylinder(points, base, direction, 7/4*a, 3*zmax)
color = np.where(D, 'y', 'k')
size = np.where(D, 100, 1)

fig = plt.figure()
ax = fig.add_subplot(projection='3d')
ax.scatter(xv, yv, zv, c=color, s=size)
ax.axis("equal")
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')
plt.show()


def cylinder_path(start, direction, radius, speed, time):

    d = normalize(direction)
    xv, yv, zv = ICArray()
    points = np.array([xv, yv, zv]).T
    dt = 0.01

    D = np.zeros_like(xv, dtype=bool)
    color = np.where(D, "y", "k")
    size = np.where(D, 50, 1)

    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    sc = ax.scatter(xv, yv, zv, c=color, s=size)

    def update(frame):
        L = speed*time
        dx = speed*dt * d
        D = in_cylinder(points, start + frame*dx, direction, radius, L)
        color = np.where(D, "y", "k")
        size = np.where(D, 50, 1)
        sc.set(color=color, sizes=size)
        return sc,

    animation = FuncAnimation(fig, update, blit=True)
    return animation.to_jshtml()
                
# Animation, uncomment only in Jupyter notebook
# HTML(cylinder_path(base, direction, 4, 10, 2))
