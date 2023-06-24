import numpy as np
import csv
import matplotlib.pyplot as plt

filename = 'mag_data.txt'
magx = np.array([])
magy = np.array([])
magz = np.array([])

with open(filename, newline='') as csvfile:
    
    spamreader = csv.reader(csvfile, delimiter=' ')
    for row in spamreader:
        print(row)
        magx = np.append(magx,float(row[0]))
        magy = np.append(magy,float(row[1]))
        magz = np.append(magz,float(row[2]))
        
# print(magx.shape,magy.shape,magz.shape)

A = np.array([[0.197738,-0.000097,-0.001984],
             [-0.000097,0.190626,0.004093],
             [-0.001984,0.004093,0.291504]])

# A = np.linalg.inv(A)

b = np.array([-21.738737,27.527433,-34.076678])

N = len(magx)
calibData = np.zeros([N,3], dtype='float')

for i in range(N):
    currMeas = np.array([magx[i],magy[i],magz[i]])
    calibData[i,:] = A @ (currMeas-b)

fig = plt.figure(figsize = (10, 7))
ax0 = plt.axes()
ax0.scatter(magx,magy)
ax0.scatter(calibData[:,0],calibData[:,1])
plt.show()

fig = plt.figure(figsize = (10, 7))
ax1 = plt.axes()
ax1.scatter(magx,magz)
ax1.scatter(calibData[:,0],calibData[:,2])
plt.show()

fig = plt.figure(figsize = (10, 7))
ax1 = plt.axes()
ax1.scatter(magy,magz)
ax1.scatter(calibData[:,1],calibData[:,2])
plt.show()
# Creating figure
fig = plt.figure(figsize = (10, 7))
ax = plt.axes(projection ="3d")
ax.scatter3D(magx,magy,magz)
ax.scatter3D(calibData[:,0],calibData[:,1],calibData[:,2])
plt.show()