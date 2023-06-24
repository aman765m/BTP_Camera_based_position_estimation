import numpy as np
import csv
import matplotlib.pyplot as plt

filename = 'pose_data.txt'
accx = np.array([])
accy = np.array([])
accz = np.array([])
velx = np.array([])
vely = np.array([])
posx = np.array([])
posy = np.array([])

with open(filename, newline='') as csvfile:
    
    spamreader = csv.reader(csvfile, delimiter=',')
    for row in spamreader:
        
        accx = np.append(accx,float(row[0]))
        accy = np.append(accy,float(row[1]))
        accz = np.append(accz,float(row[2]))
        velx = np.append(velx,float(row[3]))
        vely = np.append(vely,float(row[4]))
        posx = np.append(posx,float(row[5]))
        posy = np.append(posy,float(row[6]))
        
# plt.subplot(2,2,1)
# plt.plot(accx)
# plt.subplot(2,2,2)
# plt.plot(accy)
# plt.subplot(2,2,3)
# plt.plot(velx)
# plt.subplot(2,2,4)
# plt.plot(vely)

plt.subplot(2,1,1)
plt.plot(accx)
plt.subplot(2,1,2)
plt.plot(velx)


plt.show()
