import numpy as np
import csv
import matplotlib.pyplot as plt

filename1 = 'pose_data.txt'
filename2 = 'pose_data_cam.txt'
accx = np.array([])
accy = np.array([])
accz = np.array([])
velx = np.array([])
vely = np.array([])
posx = np.array([])
posy = np.array([])

velx_cam = np.array([])
vely_cam = np.array([])
vfx_cam = np.array([])
vfy_cam = np.array([])
posx_cam = np.array([])
posy_cam = np.array([])

with open(filename1, newline='') as csvfile:
    
    spamreader = csv.reader(csvfile, delimiter=',')
    for row in spamreader:
        
        # accx = np.append(accx,float(row[0]))
        # accy = np.append(accy,float(row[1]))
        # # accz = np.append(accz,float(row[2]))
        # velx = np.append(velx,float(row[2]))
        # vely = np.append(vely,float(row[3]))
        # # posx = np.append(posx,float(row[5]))
        # # posy = np.append(posy,float(row[6]))
        accx = np.append(accx,float(row[0]))
        accy = np.append(accy,float(row[1]))
        accz = np.append(accz,float(row[2]))
        velx = np.append(velx,float(row[3]))
        vely = np.append(vely,float(row[4]))
        posx = np.append(posx,float(row[5]))
        posy = np.append(posy,float(row[6]))

with open(filename2, newline='') as csvfile:
    
    spamreader = csv.reader(csvfile, delimiter=',')
    for row in spamreader:
        
        velx_cam = np.append(velx_cam,float(row[0]))
        vely_cam = np.append(vely_cam,float(row[1]))
        vfx_cam = np.append(vfx_cam,float(row[2]))
        vfy_cam = np.append(vfy_cam,float(row[3]))
        posx_cam = np.append(posx_cam,float(row[4]))
        posy_cam = np.append(posy_cam,float(row[5]))

#plot IMU data     
plt.subplot(3,4,1)
plt.plot(accx)
plt.subplot(3,4,2)
plt.plot(accy)
plt.subplot(3,4,5)
plt.plot(velx)
plt.subplot(3,4,6)
plt.plot(vely)
plt.subplot(3,4,9)
plt.plot(posx)
plt.subplot(3,4,10)
plt.plot(posy)

#plot camera data
plt.subplot(3,4,3)
plt.plot(velx_cam)
plt.subplot(3,4,4)
plt.plot(vely_cam)
plt.subplot(3,4,7)
plt.plot(vfx_cam)
plt.subplot(3,4,8)
plt.plot(vfy_cam)
plt.subplot(3,4,11)
plt.plot(posx_cam)
plt.subplot(3,4,12)
plt.plot(posy_cam)

plt.show()
