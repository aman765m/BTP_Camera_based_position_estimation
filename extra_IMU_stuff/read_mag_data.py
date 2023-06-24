import time
from DFRobot_BMX160 import BMX160
import numpy as np

bmx = BMX160(1)

#begin return True if succeed, otherwise return False
while not bmx.begin():
    time.sleep(2)

filename = 'mag_data.txt'
txt_file = open(filename,'w')

mag_arr = np.zeros([25,3])

def main():

    input('press enter to start collecting data...\n')
    
    while True:
        try:
            # input('\npress enter to record data\n')
            
            for i in range(25):
                data= bmx.get_all_data()
                time.sleep(0.001)
                
                mag_arr[i,0] = data[0]
                mag_arr[i,1] = data[1]
                mag_arr[i,2] = data[2]
                
            txt_file.write(str(np.mean(mag_arr[:,0]))+' '+str(np.mean(mag_arr[:,1]))+' '+str(np.mean(mag_arr[:,2]))+'\n')
            print('recorded:- ',np.mean(mag_arr[:,0]),np.mean(mag_arr[:,1]),np.mean(mag_arr[:,2]))
        
        except KeyboardInterrupt:
            
            txt_file.close()
            print('\nSaving data...Done')
            break

if __name__ == "__main__":
    main()