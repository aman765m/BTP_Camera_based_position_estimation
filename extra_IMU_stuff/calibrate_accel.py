import numpy as np
import csv
import matplotlib.pyplot as plt

filename = 'accel_data.csv'
accx = np.array([])
accy = np.array([])
accz = np.array([])

with open(filename, newline='') as csvfile:
    
    spamreader = csv.reader(csvfile, delimiter=',')
    for row in spamreader:
        print(row)
        accx = np.append(accx,float(row[0]))
        accy = np.append(accy,float(row[1]))
        accz = np.append(accz,float(row[2]))
        
# print(accx.shape,accy.shape,accz.shape)

A = np.array([[0.991498,-0.001854,-0.003966],
             [-0.001854,1.00501,0.000467],
             [-0.003966,0.00467,1.001840]])

# A = np.linalg.inv(A)

b = np.array([-0.542398,-0.118015,0.623819])

N = len(accx)
calibData = np.zeros([N,3], dtype='float')

for i in range(N):
    currMeas = np.array([accx[i],accy[i],accz[i]])
    calibData[i,:] = A @ (currMeas-b)

fig = plt.figure(figsize = (10, 7))
ax0 = plt.axes()
ax0.scatter(accx,accy)
ax0.scatter(calibData[:,0],calibData[:,1])
plt.show()
# Creating figure
fig = plt.figure(figsize = (10, 7))
ax = plt.axes(projection ="3d")
ax.scatter3D(accx,accy,accz)
ax.scatter3D(calibData[:,0],calibData[:,1],calibData[:,2])
plt.show()