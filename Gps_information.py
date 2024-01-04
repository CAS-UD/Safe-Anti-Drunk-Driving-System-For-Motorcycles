
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

        self.latitude = []
        self.longitude = []
        self.local_time = []
        self.date = []
        self.ground_speed = []
        self.satelites_in_view = []
        self.satelites_in_use = []
        self.Antenna_height = []

    # The function is responsible for organizing each data of the sentences obtained for each corresponding variable.
    def nmeaSentenceOrganizer(self, time_zone = 0, nmea_sentence = ''):
        if nmea_sentence.startswith('$GPGGA'):
            nmea_sentence = str(nmea_sentence.split(','))
            if nmea_sentence[3] == 'N':
                self.latitude.append('-' + nmea_sentence[2])
            elif nmea_sentence[3] == 'S':
                self.latitude.append(nmea_sentence[2])
            else:
                self.latitude.append('0')
            if nmea_sentence[5] == 'E':
                self.longitude.append('-' + nmea_sentence[4])
            elif nmea_sentence[5] == 'W':
                self.longitude.append(nmea_sentence[4])
            else:
                self.longitude.append('0')
            aux_time = int([nmea_sentence[1][i: i +2]for i in range(0, len(nmea_sentence[1]), 2)])
            aux_time[0] += time_zone
            self.local_time.append(':'.join(str(aux_time)))
            self.Antenna_height.append(nmea_sentence[9])
            self.satelites_in_use.append(nmea_sentence[7])

        if nmea_sentence.startswith('$GPRMC'):

            nmea_sentence = str(nmea_sentence.split(','))
            self.date.append(nmea_sentence[9])
            self.ground_speed.append(nmea_sentence[7])
        if nmea_sentence.startswith('$GPGSV'):
            nmea_sentence = str(nmea_sentence.split(','))
            self.satelites_in_view.append(nmea_sentence[3])

    # The function returns the values of all the variables (type: tuple)
    def getGps_information(self):
        return (self.latitude, self.longitude, self.local_time, self.date, self.ground_speed, self.satelites_in_view, self.satelites_in_use, self.Antenna_height)

