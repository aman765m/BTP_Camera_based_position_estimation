import time
# from DFRobot_BMX160 import BMX160
import numpy as np
from scipy import signal
import math
import matplotlib.pyplot as plt

class positionIMU():

    def __init__(self):

        self.rate = 100

        filename = 'pose_data.txt'
        self.txt = open(filename,'w')

        

        self.dataFreq = 0.01
        self.noiseFreq = 1
        self.vel_arr = np.zeros(2)
        self.vel_arr1 = np.zeros(2)
        self.pos_arr = np.zeros(2)

        self.count = 0

        #butterworth filter for imu________________________

        N_imu = 4 #filter order
        fs_sig_imu = 250 #sampling freq (Hz)
        cutoff_imu = 0.1 #cutoff freq (Hz)
        # Wn_imu = cutoff_imu/(fs_sig_imu*0.5)
        Wn_imu = cutoff_imu
        

        self.b_imu, self.a_imu = signal.butter(N_imu, Wn_imu, btype='hp', analog=False, output='ba', fs=fs_sig_imu)
        # self.b_imu, self.a_imu = signal.cheby1(N_imu,0.5, Wn_imu,btype='high',analog=False,output='ba', fs=fs_sig_imu)
        print("HPF coeff = ", self.b_imu, self.a_imu)

        w, h = signal.freqs(self.a_imu, self.b_imu)

        plt.semilogx(w, 20 * np.log10(abs(h)))

        plt.title('Butterworth filter frequency response')

        plt.xlabel('Frequency [radians / second]')

        plt.ylabel('Amplitude [dB]')

        plt.margins(0, 0.1)

        plt.grid(which='both', axis='both')

        plt.axvline(100, color='green') # cutoff frequency

        plt.show()

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


    def estimator(self):

        
        self.vel_arr[:] = np.array([self.count/50 + math.sin(self.noiseFreq*self.count/self.rate),math.cos(self.dataFreq*self.count/self.rate) + math.cos(self.noiseFreq*self.count/self.rate)])
        self.vel_arr1[:] = self.butterworthHPF(self.vel_arr[:])

        self.pos_arr[:] = self.pos_arr[:]+self.vel_arr1[:]
        
            
        self.txt.write(str(self.vel_arr[0])+','+str(self.vel_arr[1])+','+str(0)+','+str(self.vel_arr1[0])+','+str(self.vel_arr1[1])+','+str(self.pos_arr[0])+','+str(self.pos_arr[1])+'\n')
        print(self.count)
        self.count+=1
        
        

if __name__ == "__main__":
    
    pos_est = positionIMU()

    while 1:
        try:
            pos_est.estimator()
            # time.sleep(1/pos_est.rate)

        except KeyboardInterrupt:
            
            pos_est.txt.close()
            print('\n\nclosing...')
            break


