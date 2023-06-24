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
bmx.set_accel_range(bmx.AccelRange_2G)
time.sleep(0.1)

filename = 'accel_data_proxy.csv'
csv = open(filename,'w')

A = np.array([[0.991498,-0.001854,-0.003966],
             [-0.001854,1.00501,0.000467],
             [-0.003966,0.00467,1.001840]])

# A = np.linalg.inv(A)

b = np.array([-0.542398,-0.118015,0.623819])

def main():
    while True:
        try:

            data= bmx.get_all_data()
            time.sleep(0.01)
            
            calibData = A @ ([data[6],data[7],data[8]]-b)
            print(calibData)
            print(" ")
            
                
#             csv.write(str(np.mean(accel_arr[:,0]))+','+str(np.mean(accel_arr[:,1]))+','+str(np.mean(accel_arr[:,2]))+'\n')
#             print('recorded:- ',np.mean(accel_arr[:,0]),np.mean(accel_arr[:,1]),np.mean(accel_arr[:,2]))
        
        except KeyboardInterrupt:
            
            csv.close()
            print('closing')
            break

if __name__ == "__main__":
    main()

