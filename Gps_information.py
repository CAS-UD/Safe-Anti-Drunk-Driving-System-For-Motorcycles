
# This file receives NMEA sentence lines 
# and returns certain data in an organized manner.
# The Sentence Organizer function receives a time zone 
# parameter, which if not received is interpreted as UTC-0
# Example: 
#   Input: $GPGGA, 123519, 4807.038, N, 01131.000, E, 1, 08, 0.9, 545.4, M, 46.9, M, , , * 47 with time zone = -5
#   Output: time: 07:35:19, latitude: 48.07038, longitude: -11.31000, Antenna height: 545.4, Satellites in use: 8
from machine import UART
import time

class GpsInformation:

    def __init__(self):

        self.latitude = ""
        self.longitude = ""
        self.local_time = ""
        self.date = ""
        self.ground_speed = ""
        self.satelites_in_view = ""
        self.satelites_in_use = ""
        self.Antenna_height = ""

    # The function is responsible for organizing each data of the sentences obtained for each corresponding variable.
    def nmeaSentenceOrganizer(self, time_zone = 0, nmea_sentence = ''):
        if nmea_sentence.startswith('$GPGGA'):
            nmea_sentence = nmea_sentence.split(',')
            if nmea_sentence[3] == 'N':
                self.latitude = ('-' + nmea_sentence[2])
            elif nmea_sentence[3] == 'S':
                self.latitude = (nmea_sentence[2])
            else:
                self.latitude = ('0')
            if nmea_sentence[5] == 'E':
                self.longitude = ('-' + nmea_sentence[4])
            elif nmea_sentence[5] == 'W':
                self.longitude = (nmea_sentence[4])
            else:
                self.longitude = ('0')
            try:
                aux_time = [nmea_sentence[1][i: i +2]for i in range(0, len(nmea_sentence[1]), 2)]
                aux_time[0] = str(int(aux_time[0]) + int(time_zone))
                self.local_time = (''.join(aux_time))
            except Exception as e:
                print("invalid time: ", nmea_sentence[1] )
            self.Antenna_height = (nmea_sentence[9])
            self.satelites_in_use = (nmea_sentence[7])

        elif nmea_sentence.startswith('$GPRMC'):

            nmea_sentence = nmea_sentence.split(',')
            self.date = (nmea_sentence[9])
            self.ground_speed = (nmea_sentence[7])

        elif nmea_sentence.startswith('$GPGSV'):
            nmea_sentence = nmea_sentence.split(',')
            self.satelites_in_view = (nmea_sentence[3])

    # The function returns the values of all the variables (type: tuple)
    def getGps_information(self):
        return (self.latitude, self.longitude, self.local_time, self.date, self.ground_speed, self.satelites_in_view, self.satelites_in_use, self.Antenna_height)

