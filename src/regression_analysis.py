import pandas as pd
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

#read a pixel text file into pandas dataframe and change the file name to the one you want to look at
df = pd.read_csv('./16REU955570.txt', header = None, names = ['x', 'y', 'z', 'c'])

#inspect first 5 records in the df to make sure schema is what we expect it to be
df.head()

#calculate center of the pixel
pixel_center = [df.x.mean(), df.y.mean()]
print(pixel_center)

#calculate sw point (lower left) and localize coordinates
x0 = df.x.min()
y0 = df.y.min()

df.x = df.x - x0
df.y = df.y - y0

# show all of the unique LAS classifications present in the 'c' column
df.c.unique()

# extract the ground points LAS class 2 into a new dataframe
ground_points = df[df.c == 2].reset_index(drop=True)

# check the last 5 records
ground_points.tail()

# extract the non-ground points LAS class anything except 2 into a new dataframe
ng_points = df[df.c != 2].reset_index(drop=True)

# compute ground point roughness (square root of variance)
# using ordinary least squares regression plane
# this is essentially 'by hand', I'm sure there is a python module for this

A = np.array([[sum([1 for i in ground_points.z]), sum(ground_points.x), sum(ground_points.y)],
              [sum(ground_points.x), sum(ground_points.x**2), sum(ground_points.x*ground_points.y)],
              [sum(ground_points.y), sum(ground_points.x*ground_points.y), sum(ground_points.y**2)]])

b = np.array([sum(ground_points.z), sum(ground_points.x*ground_points.z), sum(ground_points.y*ground_points.z)])

beta_g = np.linalg.solve(A,b)

print(beta_g)

n = len(ground_points)
summation = 0.0

for i in range(n):
    actual = ground_points.z[i]
    estimated = beta_g[0] + beta_g[1]*ground_points.x[i] + beta_g[2]*ground_points.y[i]
    residual = actual - estimated
    residual_squared = residual**2
    summation += residual_squared
    
sigma_g = np.sqrt(1/n*summation)

print(sigma_g)

A = np.array([[sum([1 for i in ng_points.z]), sum(ng_points.x), sum(ng_points.y)],
              [sum(ng_points.x), sum(ng_points.x**2), sum(ng_points.x*ng_points.y)],
              [sum(ng_points.y), sum(ng_points.x*ng_points.y), sum(ng_points.y**2)]])

b = np.array([sum(ng_points.z), sum(ng_points.x*ng_points.z), sum(ng_points.y*ng_points.z)])

beta_ng = np.linalg.solve(A,b)

print(beta_ng)

n = len(ng_points)
summation = 0.0


for i in range(n):
    actual = ng_points.z[i]
    estimated = beta_ng[0] + beta_ng[1]*ng_points.x[i] + beta_ng[2]*ng_points.y[i]
    residual = actual - estimated
    residual_squared = residual**2
    summation += residual_squared
    
sigma_ng = np.sqrt(1/n*summation)

print(sigma_ng)

# compute height of non-ground regression plane at pixel center
# note, this must be at local coordinates now
x = pixel_center[0] - x0
y = pixel_center[1] - y0
print(x,y)

ground_elev_center = beta_g[0] + beta_g[1]*x + beta_g[2]*y
print(ground_elev_center)
ng_elev_center = beta_ng[0] + beta_ng[1]*x + beta_ng[2]*y
print(ng_elev_center)
height_ng = ng_elev_center - ground_elev_center
print(height_ng)

# here is a plot of the points in the pixel

fig = plt.figure(figsize=(10,10))
ax = fig.add_subplot(111, projection='3d')

ax.scatter(ground_points.x, ground_points.y, ground_points.z, marker='.',color='sienna')
ax.scatter(ng_points.x, ng_points.y, ng_points.z, marker='.', color='darkolivegreen')


# here is a plot of the points in the pixel
# along with the regression planes

fig = plt.figure(figsize=(10,10))
ax = fig.add_subplot(111, projection='3d')

ax.scatter(ground_points.x, ground_points.y, ground_points.z, marker='.',color='sienna')
ax.scatter(ng_points.x, ng_points.y, ng_points.z, marker='.', color='darkolivegreen')

xlim = df.x.max()
ylim = df.y.max()

xx, yy = np.meshgrid(np.linspace(0,xlim,5), np.linspace(0,ylim,5))
z_ngplane = beta_ng[0] + beta_ng[1]*xx + beta_ng[2]*yy
z_gplane = beta_g[0] + beta_g[1]*xx + beta_g[2]*yy
# z_zero = 0 + 0*xx + 0*yy

ax.plot_wireframe(xx, yy, z_ngplane, color='green')
ax.plot_wireframe(xx, yy, z_gplane, color='brown')
# ax.plot_wireframe(xx, yy, z_zero, color='navy')

plt.show()


# and here is the line you would write to the output file
print('northing,easting,sigma_g,sigma_ng,ngh') # header for file
print(f'{pixel_center[1]},{pixel_center[0]},{sigma_g},{sigma_ng},{height_ng}')
