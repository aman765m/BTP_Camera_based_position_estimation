import time
from DFRobot_BMX160 import BMX160
import numpy as np
from scipy import signal

class positionIMU():

    def __init__(self):

        self.bmx = BMX160(1)

        #begin return True if succeed, otherwise return False
        while not self.bmx.begin():
            time.sleep(2)

        ''' 
        AccelRange_2G
        AccelRange_4G
        AccelRange_8G
        AccelRange_16G
        '''
        self.bmx.set_accel_range(self.bmx.AccelRange_2G)
        time.sleep(0.1)

        self.rate = 100

        filename = 'pose_data.txt'
        self.txt = open(filename,'w')

        self.A = np.array([[0.991498,-0.001854,-0.003966],
                     [-0.001854,1.00501,0.000467],
                     [-0.003966,0.00467,1.001840]])

        # A = np.linalg.inv(A)

        self.b = np.array([-0.542398,-0.118015,0.623819])

        self.vel_arr = np.zeros(2)
        self.pos_arr = np.zeros(2)
        self.count = 0

        #butterworth filter for imu________________________

        N_imu = 2#filter order
        fs_sig_imu = 250 #sampling freq (Hz)
        cutoff_imu = 0.01 #cutoff freq (Hz)
        # Wn_imu = cutoff_imu/(fs_sig_imu*0.5)
        Wn_imu = cutoff_imu
        

        self.b_imu, self.a_imu = signal.butter(N_imu, Wn_imu, btype='hp', analog=False, output='ba', fs=fs_sig_imu)
        # self.b_imu, self.a_imu = signal.cheby1(N_imu,0.5, Wn_imu,btype='high',analog=False,output='ba', fs=fs_sig_imu)
        print("HPF coeff = ", self.b_imu, self.a_imu)

        #for simultaneous x and y axis
        self.b_imu = np.array([self.b_imu, self.b_imu])
        self.a_imu = np.array([self.a_imu, self.a_imu])

        #input and output x and y, not the axes
        self.x_imu = np.zeros(np.shape(self.b_imu))
        self.y_imu = np.zeros(np.shape(self.a_imu))

        # self.bufferHPF = np.zeros(10)


    def butterworthHPF(self, sig):


        self.x_imu[:,1:] = self.x_imu[:,0:-1]

        self.x_imu[0,0] = sig[0]
        self.x_imu[1,0] = sig[1]

        temp1 = np.array([np.sum(self.x_imu[0][:]*self.b_imu[0][:]) - np.sum(self.a_imu[0][1:]*self.y_imu[0][0:-1])])
        temp2 = np.array([np.sum(self.x_imu[1][:]*self.b_imu[1][:]) - np.sum(self.a_imu[1][1:]*self.y_imu[1][0:-1])])

        for i in range(len(self.a_imu[0])-1):
            # print(temp)
            temp1 = np.append(temp1,self.y_imu[0][i])
            temp2 = np.append(temp2,self.y_imu[1][i])
            

        self.y_imu = [temp1,temp2]

        return [self.y_imu[0][0], self.y_imu[1][0]]
    # def BHPF(self,sig):

    #     self.bufferHPF = np.roll(self.bufferHPF,-1)
    #     self.bufferHPF[-1] = sig

    #     out = signal.filtfilt(self.b_imu,self.a_imu,self.bufferHPF)
    #     return(out[-1])

    def imu_bias_est(self):

        data = np.zeros([100,3])
        print("Please wait for imu bias estimation...")
        for i in range(100):
            tempData = self.bmx.get_all_data()
            data[i,:] = tempData[6:9]
            time.sleep(0.01)

        self.b = np.array([np.mean(data[:,0]),np.mean(data[:,1]),np.mean(data[:,2])])
        print("Computed bias = ",self.b)
        time.sleep(0.1)




    def estimator(self):

        data= self.bmx.get_all_data()
        # time.sleep(0.01)
        
        calibData = self.A @ ([data[6],data[7],data[8]]-self.b)

        #applying th HPF to x and y accels
        # accx,accy = self.butterworthHPF(calibData[0:2])
        accx,accy = calibData[0:2]

        self.vel_arr[:] = self.vel_arr[:]+np.array([accx,accy])*1/self.rate
        #self.vel_arr[:] = np.array(self.butterworthHPF(self.vel_arr[:])) #uncomment this line to apply high pass filter

        self.pos_arr[:] = self.pos_arr[:]+self.vel_arr[:]*1/self.rate
        
            
        self.txt.write(str(accx)+','+str(accy)+','+str(calibData[2])+','+str(self.vel_arr[0])+','+str(self.vel_arr[1])+','+str(self.pos_arr[0])+','+str(self.pos_arr[1])+'\n')
        print(self.count, 'imu')
        self.count+=1
        return
        
        

if __name__ == "__main__":
    
    pos_est = positionIMU();pos_est.imu_bias_est()
    while 1:
        try:
            pos_est.estimator()
            time.sleep(1/pos_est.rate)

        except KeyboardInterrupt:
            
            pos_est.txt.close()
            print('\n\nclosing...')
            break


