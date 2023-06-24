'''!
  @file read_accel_data.py
  @brief Through the example, you can get the sensor data by using getAllData:
  @n     get accelerometer data of sensor.
  @n     With the rotation of the sensor, data changes are visible.
  @copyright	Copyright (c) 2010 DFRobot Co.Ltd (http://www.dfrobot.com)
  @license     The MIT License (MIT)
  @author [luoyufeng] (yufeng.luo@dfrobot.com)
  @maintainer [Fary](feng.yang@dfrobot.com)
  @version  V1.0
  @date  2021-10-20
  @url https://github.com/DFRobot/DFRobot_BMX160
'''
import sys
sys.path.append('../../')
import time
from DFRobot_BMX160 import BMX160
import numpy as np

bmx = BMX160(1)

#begin return True if succeed, otherwise return False
while not bmx.begin():
    time.sleep(2)

''' 
AccelRange_2G
AccelRange_4G
AccelRange_8G
AccelRange_16G
'''
bmx.set_accel_range(bmx.AccelRange_4G)
time.sleep(0.1)

filename = 'accel_data_proxy.csv'
csv = open(filename,'w')

accel_arr = np.zeros([25,3])
def main():
    while True:
        try:
#             print("accel x: {0:.2f} m/s^2, y: {1:.2f} m/s^2, z: {2:.2f} m/s^2".format(data[6],data[7],data[8]))
#             print(" ")
#             
            input('\npress enter to record data\n')
            
            for i in range(25):
                data= bmx.get_all_data()
                time.sleep(0.01)
                
                accel_arr[i,0] = data[6]
                accel_arr[i,1] = data[7]
                accel_arr[i,2] = data[8]
                
            csv.write(str(np.mean(accel_arr[:,0]))+','+str(np.mean(accel_arr[:,1]))+','+str(np.mean(accel_arr[:,2]))+'\n')
            print('recorded:- ',np.mean(accel_arr[:,0]),np.mean(accel_arr[:,1]),np.mean(accel_arr[:,2]))
        
        except KeyboardInterrupt:
            
            csv.close()
            print('Saving data...Done')
            break

if __name__ == "__main__":
    main()
