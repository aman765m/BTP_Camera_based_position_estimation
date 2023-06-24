import numpy as np
from scipy import signal, ndimage
import cv2
import time
from sys import float_info
import math
#from DFRobot_BMX160 import BMX160
from position_estimate_IMU import *

## File Description__________________________________
# This is the main file, responsible for calling camera and accelerometer based position/velocity
# estimations. The out of camera velocity is saved in file named 'pose_data_cam.txt', and camera feed
# is stored in file named 'drone_vid.avi', whereas IMU output is saved in file named 'pose_data.txt'

# **Data stored in 'pose_data_cam.txt' has the order (column wise) :- 
# Raw velocity x, Raw velocity y, Filtered velocity x, Filtered velocity y, position x, position y

# **Data stored in 'pose_data.txt' (IMU) has the order (column wise) :- 
# Raw acceleration x, Raw acceleration y, Raw acceleration z, velocity x, velocity y, position x, position y
#____________________________________________________



class op_flow():  
    def __init__(self):

#initialisations:

        # params for ShiTomasi corner detection
        self.feature_params = dict( maxCorners = 10,
                            qualityLevel = 0.3,
                            minDistance = 7,
                            blockSize = 7 )
        # Parameters for lucas kanade optical flow
        self.lk_params = dict( winSize  = (15, 15),
                        maxLevel = 2,
                        criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))
        # Create some random colors
        self.color = np.random.randint(0, 255, (100, 3))
        self.mask = np.uint8(np.zeros([100,120]))
        

        #Frequency of operation.
        self.sample_rate = 10.0 #10 Hz (better to keep it around 50)

        self.img = np.empty([])
        self.img_prev = np.empty([])
        self.time_stamp1 = 0
        self.time_stamp2 = 0
        self.count = 0

        self.frame_width = 640
        self.frame_height = 480
           
        size = (self.frame_width, self.frame_height)

        #video write object
        # fourcc= cv2.CV_FOURCC('m', 'p', '4', 'v')
        fourcc= cv2.VideoWriter_fourcc('m','p','4','v')
        self.result = cv2.VideoWriter('drone_vid.avi',fourcc, 10, size,0)

        #object of the imu class
        self.imu_pos = positionIMU()

        # ##Gaussian_____________________________________________________________________________
        # w = 5
        # kernel_size = 2*self.w+1
        # sigma, mu = 0.5, 0.0

        # x, y = np.meshgrid(np.linspace(-1,1,kernel_size), np.linspace(-1,1,kernel_size))
        # d = np.sqrt(x*x+y*y)
        
        # self.gauss = np.exp(-( (d-mu)**2 / ( 2.0 * sigma**2 ) ) )


        #translational vel from camera
        self.vel_x = 0
        self.vel_y = 0
        self.vel_z = 0;self.posx = 0;self.posy = 0

        #constants for velocity calculation from image
        self.focal = 10 #assumption...although acts as a scaling factron only
        self.velx_avg = np.array([0])
        self.vely_avg = np.array([0])

        #butterworth filter parameters for camera_____________________

        N_cam = 2  #filter order
        fs_sig_cam = 50 #sampling freq (Hz)
        Wn_cam = 1 #cutoff freq (Hz)
        

        self.b_cam, self.a_cam = signal.butter(N_cam, Wn_cam, btype='lp', analog=False, output='ba', fs=fs_sig_cam)
        print("coeff = ", self.b_cam, self.a_cam)
        self.b_cam = np.array([self.b_cam, self.b_cam])
        self.a_cam = np.array([self.a_cam, self.a_cam])

        self.x_cam = np.zeros(np.shape(self.b_cam))
        self.y_cam = np.zeros(np.shape(self.a_cam))

        #save data
        filename = 'pose_data_cam.txt'
        self.txt = open(filename,'w')

        self.exit = 0
        #accumulator for 5 point moving average MA filter (higher lenght changes phase more)
        # self.acc_x = np.zeros([5,1])
        # self.acc_y = np.zeros([5,1])

    ## butterworth filter for camera
    def butterworth_filt_cam(self, sig):

        self.x_cam[:,1:] = self.x_cam[:,0:-1]

        self.x_cam[0,0] = sig[0]
        self.x_cam[1,0] = sig[1]

        temp1 = np.array([np.sum(self.x_cam[0][:]*self.b_cam[0][:]) - np.sum(self.a_cam[0][1:]*self.y_cam[0][0:-1])])
        temp2 = np.array([np.sum(self.x_cam[1][:]*self.b_cam[1][:]) - np.sum(self.a_cam[1][1:]*self.y_cam[1][0:-1])])

        for i in range(len(self.a_cam[0])-1):
            # print(temp)
            temp1 = np.append(temp1,self.y_cam[0][i])
            temp2 = np.append(temp2,self.y_cam[1][i])
            

        self.y_cam = [temp1,temp2]

        return [self.y_cam[0][0], self.y_cam[1][0]]   

#algorithm

    def solving_algo(self,img,img_prev):  

        #optical flow
        if len(img.shape) > 0: # assert that images are recieved 

            # Frame obtain
            im1 = img
            im2 = img_prev

            # im1 = cv2.cvtColor(fr1,cv2.COLOR_BGR2GRAY)
            # im1 = cv2.normalize(im1t.astype('float'), None, 0.0, 1.0, cv2.NORM_MINMAX)
            # im1 = ndimage.gaussian_filter(im1, sigma = 5)

            # im2 = cv2.cvtColor(fr2,cv2.COLOR_BGR2GRAY)
            # im2 = cv2.normalize(im2t.astype('float'), None, 0.0, 1.0, cv2.NORM_MINMAX) 
            # im2 = ndimage.gaussian_filter(im2, sigma = 5)

            # Take first frame and find corners in it
            p0 = cv2.goodFeaturesToTrack(im2, mask = None, **self.feature_params)

            # calculate optical flow
            p1, st, err = cv2.calcOpticalFlowPyrLK(im2, im1, p0, None, **self.lk_params)
            # Select good points
            if p1 is not None:
                good_new = p1[st==1]
                good_old = p0[st==1]
            # draw the tracks
            self.mask = np.uint8(np.zeros(im1.shape))
            for i, (new, old) in enumerate(zip(good_new, good_old)):
                a, b = new.ravel()
                c, d = old.ravel()
                self.mask = cv2.line(self.mask, (int(a), int(b)), (int(c), int(d)), self.color[i].tolist(), 2)
                im1 = cv2.circle(im1, (int(a), int(b)), 5, self.color[i].tolist(), -1)
            # print((im1.shape),type(self.mask.shape))
            img = cv2.add(im1, self.mask)

            self.result.write(img)

            # ########################## uncomment to see live camera feed
            # cv2.imshow('frame', img)
            # k = cv2.waitKey(10) & 0xff
            # if k == 27:
            #     self.exit = 1
            # ##########################
            
            # self.velx_avg = self.velx_avg[1:]
            # self.vely_avg = self.vely_avg[1:]
            # print(p0, np.reshape(p0,[p0.shape[0],p0.shape[2]]))
            point_1 = np.reshape(p0,[p0.shape[0],p0.shape[2]])
            point_2 = np.reshape(p1,[p1.shape[0],p1.shape[2]])
            # print(point_1.shape, point_2.shape)
            if point_1.shape[0]>1:
                print(self.count,'cam')
                self.count+=1
                self.vel_x = np.mean(point_2[:][1]-point_1[:][1])/10
                self.vel_y = np.mean(point_2[:][0]-point_1[:][0])/10
                # print(self.vel_x, self.vel_y)
                

            # self.vel_x = (-nu[0]*math.cos(self.theta) + nu[1]*math.sin(self.theta))/self.focal
            # self.vel_y = (-nu[0]*math.sin(self.theta) - nu[1]*math.cos(self.theta))/self.focal

            self.vel_x_filt, self.vel_y_filt = self.butterworth_filt_cam([self.vel_x, self.vel_y])
            self.posx += self.vel_x
            self.posy += self.vel_y 

            #correcting for rotational error
            # self.theta_optical_z = math.atan2(self.vel_y,self.vel_x)
            # self.omega_optical_z = (self.prev_theta_optical_z-self.theta_optical_z)*self.scaling #considering constant discrete time steps

            #restting
            self.velx_avg = [0]
            self.vely_avg = [0]
            
            self.txt.write(str(self.vel_x)+','+str(self.vel_y)+','+str(self.vel_x_filt)+','+str(self.vel_y_filt)+','+str(self.posx)+','+str(self.posy)+'\n')
            return

if __name__ == '__main__':

    solver = op_flow() #Creating solver object

    # constant bias estimation for accelerometer
    solver.imu_pos.imu_bias_est() #**comment this line if not using imu**

    vid = cv2.VideoCapture(0)
    vid.set(cv2.CAP_PROP_FRAME_WIDTH, solver.frame_width)
    vid.set(cv2.CAP_PROP_FRAME_HEIGHT, solver.frame_height)

    ret, old_frame = vid.read()
    old_gray = cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY)
    # p0 = cv2.goodFeaturesToTrack(old_gray, mask = None, **solver.feature_params)

    while(1):
        try:

            solver.imu_pos.estimator() #**comment this line if not using imu**
            ret, frame = vid.read()
            if not ret:
                print('No frames grabbed!')
                break
            frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            solver.solving_algo(frame_gray,old_gray)
            old_gray = frame_gray.copy()
            # print('running in while')
            time.sleep(0.02)
            if solver.exit == 1:
                solver.imu_pos.txt.close() #**comment this line if not using imu**
                solver.txt.close()
                solver.result.release()
                vid.release()
                cv2.destroyAllWindows()
                print('\n\nsaving...\n')
                break


        except KeyboardInterrupt:
            solver.imu_pos.txt.close() #**comment this line if not using imu**
            solver.txt.close()
            solver.result.release()
            vid.release()
            cv2.destroyAllWindows()
            print('\n\nsaving...\n')
            break
