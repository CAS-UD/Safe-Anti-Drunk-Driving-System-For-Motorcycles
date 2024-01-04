
# This file is responsible for storing the data 
# of the sencores in the lists, it has functions 
# that allow adding data to each list and returning 
# the complete list with all the data that has been stored

from Bno055 import * 
from Gps_information import *

import machine


class DataManagement:


    def __init__(self, bno055_scl_pinCon, bno055_sda_pinCon,data_number_control, tx_pinCon,time_zone):
        
        self.imu = BNO055(machine.I2C(1,scl=machine.Pin(bno055_scl_pinCon), sda=machine.Pin(bno055_sda_pinCon)))
        self.gps = GpsInformation()

        self.data_control = data_number_control
        self.aux = data_number_control

        # Lists of each data to be obtained are created to individualize them
        self.temperature = []
        self.magnetometer = []
        self.gyroscope = []
        self.accelerometer = []
        self.linear_accelerometer = []
        self.gravity = []
        self.euler = []
        self.latitude = None
        self.longitude = None
        self.local_time = None
        self.date = None
        self.ground_speed = None
        self.satelites_in_view = None
        self.satelites_in_use = None
        self.Antenna_height = None

    # The function is responsible for adding new data to each list
    def recordingData(self): 

        if self.aux != 0:
            self.temperature.append(float(self.imu.temperature())) 
            self.magnetometer.append([float(data) for data in self.imu.mag()])
            self.accelerometer.append([float(data) for data in self.imu.accel()])
            self.gyroscope.append([float(data) for data in self.imu.gyro()])
            self.linear_accelerometer.append([float(data) for data in self.imu.lin_acc()])
            self.gravity.append([float(data) for data in self.imu.gravity()])
            self.euler.append([float(data) for data in self.imu.euler()])
            
            self.aux -= 1
        else:
            self.temperature = []
            self.magnetometer = []
            self.gyroscope = []
            self.accelerometer = []
            self.linear_accelerometer = []
            self.gravity = []
            self.euler = []

            self.aux = self.data_control

    def recordingDataGps(self,nmea_sentence, time_zone):

        self.gps.nmeaSentenceOrganizer(time_zone, nmea_sentence)
        data = self.gps.getGps_information()
        self.latitude = str(data[0])
        self.longitude = str(data[1])
        self.local_time = str(data[2])
        self.date = str(data[3])
        self.ground_speed = str(data[4])
        self.satelites_in_view = str(data[5])
        self.satelites_in_use = str(data[6])
        self.Antenna_height = str(data[7])
    

    # The function is responsible for returning the complete list of each data (type: tuple)
    def getDataIMU(self):
        return (self.temperature, self.accelerometer, self.gyroscope, self.linear_accelerometer, self.gravity, self.euler, self.magnetometer)
    
    def getDataGPS(self):
        return (self.latitude, self.longitude, self.local_time, self.date, self.ground_speed, self.satelites_in_view, self.satelites_in_use, self.Antenna_height)