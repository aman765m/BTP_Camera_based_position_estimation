
# Camera based position estimation 

This work aims at obtaining 2D position data using monocular camera, using feature detection and tracking. The data is passed through lowpass filter (both online and offline filter implementations are there, however online filtering has some anomalies which needs to be corrected). Data is also collected and stored form Accelerometer of DFRobot_BMX160. But due to implementation limitations, Accelerometer data is not used for the fiinal estimation.




## Deployment

The project is meant to be deployed on a **Raspberry Pi**, running the new Bull's Eye OS.

As the first step, the camera setup needs to be done is not already. The camera used for the project was a native raspicam, whose drivers are already available in Raspberry Pi 3,4. 

**Enable legacy camera**
```bash
  sudo raspi-config
```
![image](https://github.com/aman765m/BTP_Camera_based_position_estimation/assets/91495412/ff65b57d-8e44-4b0e-9185-42e11398444a)


Select `interface Options`, then enable legacy camera (/camera)

**PHOTO**

Then select finish and reboot.

NOTE:- If you are using VNC on a headless raspberrypi, the VNC may stop working after this, follow the steps to restore VNC :-

Connect to your raspberry pi using an SSH connection (PuTTY can be used) then execute the following:-
```bash
sudo nano /boot/config.txt
```
Then uncomment `hdmi_force_hotplug=1`
To save and exit press `Ctrl+x` then `Y` and press Enter.

**Installing openCV in Raspberry Pi using cmake**

Follow the steps given in second page of this documentation :-
https://docs.google.com/document/d/146brPQp42i2ips2L2MH5YpG518-1dR69B-Tu0jQmQiQ/edit

It also includes solution of few common issues in Raspberry Pi.


**Setting up I2C for IMU in Raspberry Pi**
IMU communicates with the Pi through I2C protocol, hence permission is needed for the usage from Raspberry Pi's side. Followin section describes how enable I2C communication in a Raspberry Pi with Bull's Eye OS.

```bash
  sudo raspi-config
```

![image](https://github.com/aman765m/BTP_Camera_based_position_estimation/assets/91495412/d5206497-6b9b-49ce-a566-951d361d31df)


Select `interface Options`, then enable I2C

**PHOTO**

Then select finish and reboot.

The main code exists in `img_vel.py` python file. This file calls all the necesary objects for recording and storing data of both camera and IMU. There is no special dependecy, other than those included in the project. The file ` pose_estimate_IMU.py` is responsible for collecting IMU data. It can be run independently as well if needed.

NOTE:- While using IMU, before running the IMU code, the current bash terminal needs to be granted permission for using the I2C bus by running (this may be needed to run in every new terminal)-
```bash
sudo chmod a+rw /dev/i2c-*

```






## Obtaining Plots

The file `plot_pos.py` can used as a temporary plotting tool, as it plots all the data recieved in `pose_data.txt` and `pose_data_cam.txt`. However these are unprocessed data - meaning not corrected for camera rotation, and also depends on online filtering which has some issue in the implementation.

Inside `post_processed_matlab_plots` folder, there are files related to organised plotting corresponding to each shape in MATLAB. For example the file `offline_filters_pentagon.m` plots the data obtained from camera (saved in .txt as per their name), after offline filtering, and also plots the ground truth using the **feed rate** information from the CNC.

The reason for having separate files for each shape is the creation of ground truth plot which is different for each shape. To use the `plot_pos.py` file for plotting direclty, rotation needs to be corrected as per the camera roation error (for reference the .m files has the implementaiton of rotation error correction).
