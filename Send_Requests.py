
# This file is responsible for sending the HTTP 
# request to the server indicated in the configuration 
# file, it also sends the amount of data stipulated in 
# this same file, the request is made through POST, 
# additionally it indicates in the console the time 
# it takes to do this process.The data is sent in 
#the Body of the request in Json format
import Data_management
import urequests
import time

class SendRequest:

    def __init__(self, url, bno055_scl_pinCon, bno055_sda_pinCon, data_number_control, tx_pinCon):

        self.url = url
        self.dat = Data_management.DataManagement(bno055_scl_pinCon, bno055_sda_pinCon, data_number_control, tx_pinCon)    

    # The function is responsible for sending the data
    def send(self):
        inicio = time.ticks_ms()
        try:

            data_imu = self.dat.getDataIMU()
            data_gps = self.dat.getDataGPS()
            json_body = {
            'Temperature' : data_imu[0],
            'Accelerometer' : data_imu[1],
            'Gyroscope' : data_imu[2],
            'LinearAccelerometer' : data_imu[3],
            'Gravity' : data_imu[4],
            'Euler' : data_imu[5],
            'Magnetometer' : data_imu[6],
            'Latitude' : data_gps[0],
            'Longitude' : data_gps[1],
            'LocalTime' : data_gps[2],
            'Date' : data_gps[3],
            'GroundSpeed' : data_gps[4],
            'SatelitesInView' : data_gps[5],
            'SatelitesInUse' : data_gps[6],
            'AntennaHeight' : data_gps[7]
            }
            res = urequests.post(self.url, json=json_body)
            fin = time.ticks_ms()
            print("el tiempo fue: ", fin-inicio)
            return res.text
        except Exception as e:
            print("An error occurred while submitting a request: ", e)
