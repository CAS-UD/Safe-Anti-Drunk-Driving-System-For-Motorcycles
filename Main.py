
# This is the main file which imports the configuration 
# variables and executes the calls of each function of 
# the rest of the project
import Connection
import Send_Requests
from Bno055 import *

import uasyncio
import machine
import time



try:                                                        
    import Config
    # Connection variables are configured
    sddi_config = Config.configuration['connection']['Sddi']
    password_config = Config.configuration['connection']['Password']
    url_config = Config.configuration['requests']['Url']
    data_number_config = int(Config.configuration['requests']['Datanumber'])

    # The BNO055 sensor variables are configured
    bno055_scl_pin_config = int(Config.configuration['bno055']['scl_pin'])
    bno055_sda_pin_config = int(Config.configuration['bno055']['sda_pin'])

    # The NEO-6mv2 (gps) sensor variables are configured
    tx_pin_config = int(Config.configuration['gps']['tx_pin'])
    time_zone_config = int(Config.configuration['gps']['time_zone'])
except ImportError as e:
    print('error to open or read the configuration file: ', e)

# Timer are created to execute the code without affecting the main flow                       
timer = machine.Timer(1)

loadin_led = machine.Pin(2, machine.Pin.OUT)

# The uart is initialized to receive the data from the GPS
uart = machine.UART(2, baudrate = 9600, rx = tx_pin_config)

# Classes are initialized that generate the Internet connection and the sending of HTTP requests and control variables.
con = Connection.Connection(wifi_name=sddi_config, password=password_config)    
req = Send_Requests.SendRequest(url_config, bno055_scl_pin_config, bno055_sda_pin_config, data_number_config, tx_pin_config, time_zone_config) 
data_number_control = data_number_config
loadin_led = machine.Pin(2, machine.Pin.OUT)
   

# Calls the createConnection function which establishes the internet connection
con.createConnection()

# The function is responsible for saving a certain
# amount of data which is established by data_number_control, 
# when the amount is fulfilled is sent using the SendRequest class, 
# at that moment the information is sent, an LED lights up indicating this process.
# the function argument is used by the timer making the function callable
def sendData(timer_event):

    if con.coneectionIsSuccessful():               
        global data_number_control
        global loadin_led
        data_number_control -= 1
        req.dat.recordingData()                     
        if data_number_control == 0:      
            loadin_led.value(1)                     
            print(req.send())                         
            loadin_led.value(0)                     
            data_number_control = data_number_config + 1
    else:                                           
        if time.time() % 30 == 0:
            con.createConnection()

# the timer is initialized (period is in miliseconds)
timer.init(period = 200, mode = machine.Timer.PERIODIC, callback = sendData)             

# This function is executed in parallel to the rest 
# of the code, it is responsible for listening to the 
# RX2 pin to determine the moment in which the GPS 
# sends information sequences. The function waits 
# until the re-read information is sent
async def gpsListening():
    global data_number_control
    global uart
    while True:
        try:
            if uart.any():
                nmea = uart.readline().decode('UTF-8')
                req.dat.recordingDataGps(nmea, time_zone_config)
        except Exception as e:
            print('error to read the gps: ', e)

# Run the gpsListening() function in parallel
uasyncio.run(gpsListening())

# Ensures that the code inside the ESP32 will not end
while True:   
    pass