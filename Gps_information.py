
# This file receives NMEA sentence lines 
# and returns certain data in an organized manner.
# The Sentence Organizer function receives a time zone 
# parameter, which if not received is interpreted as UTC-0
# Example: 
#   Input: $GPGGA, 123519, 4807.038, N, 01131.000, E, 1, 08, 0.9, 545.4, M, 46.9, M, , , * 47 with time zone = -5
#   Output: time: 07:35:19, latitude: 48.07038, longitude: -11.31000, Antenna height: 545.4, Satellites in use: 8
#
#   Input: $GPRMC, 123519, A, 4807.038, N, 01131.000, E, 022.4, 084.4, 230394, 003.1, W, * 6A
#   Output: date: 230394, ground speed: 41.3688

from machine import UART
import time

class GpsInformation:

    def __init__(self):

        self.latitude = [0]
        self.longitude = [0]
        self.local_time = [0]
        self.date = [0]
        self.ground_speed = [0]
        self.satelites_in_view = [0]
        self.satelites_in_use = [0]
        self.Antenna_height = [0]

    # The function is responsible for converting the minutes and seconds of the latitude and longitude to degrees
    @staticmethod
    def mmToDeg(value):
        auxValue = value
        auxValue = auxValue.split('.')
        auxValue[1] = auxValue[0][len(auxValue[0]) - 2:len(auxValue[0])] + '.' + auxValue[1]
        auxValue[0] = auxValue[0][0:len(auxValue[0]) - 2]
        auxValue[1] = str(float(auxValue[1]) / 60)
        auxValue = [str(float(auxValue[0]) + round(float(auxValue[1]),5))]
        return auxValue

    # The function is responsible for organizing each data of the sentences obtained for each corresponding variable.
    def nmeaSentenceOrganizer(self, time_zone = 0, nmea_sentence = ''):
        if nmea_sentence.startswith('$GPGGA'):
            nmea_sentence = nmea_sentence.split(',')
            if nmea_sentence[3] == 'N':
                self.latitude = self.mmToDeg(nmea_sentence[2])
            elif nmea_sentence[3] == 'S':
                self.latitude = ['-' + self.mmToDeg(nmea_sentence[2])[0]]
            else:
                self.latitude = ('0')
            if nmea_sentence[5] == 'E':
                self.longitude = self.mmToDeg(nmea_sentence[4])
                print(self.longitude)
            elif nmea_sentence[5] == 'W':
                self.longitude =  ['-' + self.mmToDeg(nmea_sentence[4])[0]]
            else:
                self.longitude = ('0')
            try:
                aux_time = [nmea_sentence[1][i: i +2]for i in range(0, len(nmea_sentence[1]), 2)]
                if (aux_time[0] == '00'):
                    aux_time[0] = '24'
                aux_time[0] = str(int(aux_time[0]) + int(time_zone))
                self.local_time = [':'.join(aux_time[:3])]
            except Exception as e:
                print("invalid time: ", nmea_sentence[1] )
            self.Antenna_height = [0] if nmea_sentence[9] == '' else [nmea_sentence[9]]
            self.satelites_in_use = [0] if nmea_sentence[7] == '' else [nmea_sentence[7]] 

        elif nmea_sentence.startswith('$GPRMC'):

            nmea_sentence = nmea_sentence.split(',')
            self.date = [0] if nmea_sentence[9] == '' else [nmea_sentence[9]]
            self.ground_speed = [0] if nmea_sentence[7] == '' else (float([nmea_sentence[7]]) * 1.852)

        elif nmea_sentence.startswith('$GPGSV'):
            nmea_sentence = nmea_sentence.split(',')
            self.satelites_in_view = [0] if nmea_sentence[3] == '00*79' else [nmea_sentence[3]]

    # The function returns the values of all the variables (type: tuple)
    def getGps_information(self):
        return (self.latitude, self.longitude, self.local_time, self.date, self.ground_speed, self.satelites_in_view, self.satelites_in_use, self.Antenna_height)

