import time
from DFRobot_BMX160 import BMX160
import numpy as np

bmx = BMX160(1)

#begin return True if succeed, otherwise return False
while not bmx.begin():
    time.sleep(2)
  
'''
GyroRange_2000DPS
GyroRange_1000DPS
GyroRange_500DPS
GyroRange_250DPS
GyroRange_125DPS
'''
bmx.set_gyro_range(bmx.GyroRange_250DPS)

time.sleep(0.1)
# avg_val = np.zeros([1000,3])

b = np.array([0.05565643310546875, -0.088714599609375, 0.01113128662109375])

def main():
    # cnt = 0
    # while cnt<1000:
    #     data= bmx.get_all_data()
    #     time.sleep(0.01)
    #     print("gyro  x: {0:.2f} g, y: {1:.2f} g, z: {2:.2f} g".format(data[3],data[4],data[5]))
    #     print(" ")
    #     avg_val[cnt,:] = data[3:6]
    #     cnt+=1
    # print(np.mean(avg_val[:,0]),np.mean(avg_val[:,1]),np.mean(avg_val[:,2]))

    while 1:
        data= bmx.get_all_data()
        print(data[3:6]- b)
        time.sleep(0.1)

if __name__ == "__main__":
    main()