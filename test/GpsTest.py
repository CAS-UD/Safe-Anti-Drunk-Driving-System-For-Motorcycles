# This file allows you to verify the operation of the GPS sensor

from machine import *
from Gps_information import  *

# tx and rx pin of the gps connected to the () pin of the esp32
tx_pin = 16
rx_pin = 17

gps = machine.UART(2, tx=rx_pin, rx=tx_pin, baudrate=9600)

while True:

    if gps.any():
        nmea = gps.decode('UTF-8')
        GpsInformation.nmeaSentenceOrganizer(time_zone= -5, nmea_sentence=nmea)
        gps_info = GpsInformation.getGps_information()
        print(gps_info)

    pass