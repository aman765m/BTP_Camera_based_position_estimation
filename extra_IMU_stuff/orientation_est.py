import numpy as np
import time
import math
from DFRobot_BMX160 import BMX160

class orient_est():

    def __init__(self):

        self.bmx = BMX160(1)

        # orthogonality(A) and bias(b) correction coefficients
        self.A_acc = np.array([[0.991498,-0.001854,-0.003966],
                                [-0.001854,1.00501,0.000467],
                                [-0.003966,0.00467,1.001840]])

        self.b_acc = np.array([-0.542398,-0.118015,0.623819])

        self.A_mag = np.array([[0.197738,-0.000097,-0.001984],
                    [-0.000097,0.190626,0.004093],
                    [-0.001984,0.004093,0.291504]])

        self.b_mag = np.array([-21.738737,27.527433,-34.076678])

        #begin return True if succeed, otherwise return False
        while not self.bmx.begin():
            time.sleep(2)

        self.acc_data = np.zeros(3, dtype='float')
        self.mag_data = np.zeros(3, dtype='float')
        self.euler_ang = np.array([])

    def read_data(self):

        data= self.bmx.get_all_data()

        self.mag_data[:] = self.A_mag @ (data[0:3]-self.b_mag)
        self.acc_data[:] = self.A_acc @ (data[6:9]-self.b_acc)
        # print(self.mag_data,self.acc_data)
        # LHP to RHP
        self.acc_data[2]*=1

    def get_rot(self):

        self.read_data()

        mag_norm = self.mag_data/np.linalg.norm(self.mag_data)
        acc_norm = self.acc_data/np.linalg.norm(self.acc_data)

        west = np.cross(mag_norm,acc_norm)
        north = np.cross(acc_norm,west)
        # print(np.linalg.norm(north))
        west_new = np.cross(north,acc_norm)
        R_mat = np.array([north,west_new,acc_norm])
        # print(R_mat)
        yaw = np.arctan2(R_mat[1,0],R_mat[0,0])
        pitch = np.arctan2(-R_mat[2,0],(R_mat[2,1]**2+R_mat[2,2]**2)**0.5)
        roll = np.arctan2(R_mat[2,1],R_mat[2,2])

        self.euler_ang = np.array([roll,pitch,yaw])
        # print(yaw*180/math.pi,pitch*180/math.pi,roll*180/math.pi)

        return R_mat

if __name__=='__main__':
    orient = orient_est()
    while 1:
        try:
            # orient.get_rot()
            orient.read_data()
            print(orient.mag_data)
            time.sleep(0.1)
        except KeyboardInterrupt:
            break