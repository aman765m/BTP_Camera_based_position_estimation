from orientation_est  import orient_est
import numpy as np
import math
import time

class position():

    def __init__(self):
        self.orientation = orient_est()
        self.acc_data = self.orientation.acc_data
        self.rpy = np.zeros(3,dtype='float')
        self.R_mat = np.array([])

        self.V_body = np.zeros(3,dtype='float')
        self.V_world = np.zeros(3,dtype='float')

        self.T_body = np.zeros(3,dtype='float')
        self.T_world = np.zeros(3,dtype='float')

        self.sample_rate = 50

    def get_pos(self):
        self.R_mat = self.orientation.get_rot()

        # self.V_body += (self.acc_data-np.dot(self.R_mat,np.array([0,0,9.81])))*1/self.sample_rate 
        # self.T_body += self.V_body*1/self.sample_rate \

        self.acc_world = np.dot(np.linalg.inv(self.R_mat),self.acc_data) - np.array([0,0,9.81])

        self.V_world = np.dot(self.R_mat,self.V_body)
        self.T_world = np.dot(self.R_mat,self.T_body)
        # print((self.acc_data-np.dot(self.R_mat,np.array([0,0,9.81]))))
        print(self.orientation.euler_ang*180/math.pi)
        

if __name__ == '__main__':
    pose = position()

    while 1:
        try:
            pose.get_pos()
            time.sleep(1/pose.sample_rate)
        except KeyboardInterrupt:
            break