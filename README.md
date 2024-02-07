# Collection and sending of data through HTTP protocol with ESP32

This project aims to collect and send sensor data using the HTTP protocol and the POST request with the `ESP32` microcontroller. At the moment, an `Inertial Measurement Unit (IMU)` module is being used, which functions as a magnetometer, gyroscope, accelerometer, linear accelerometer, Euler angle meter, gravitational force meter and environmental thermometer. Additionally, the `GY-NEO6MV2` sensor is used, which is a Global Positioning Systems (GPS) sensor which gives us position information, time zone, speed, etc.

# Contents

1. [Sensors used](./README.md#1-sensors-used)
2. [How to work with an esp32 from windows?](./README.md#2-how-to-work-with-an-esp32-from-windows)
3. [Obtaining data from sensors](./README.md#3-obtaining-data-from-sensors)  
  3.1 [PulluHow is data grouped?](./README.md#31-how-is-data-grouped)
4. [Test files](./README.md#4-test-files)
5. [Send HTTP request](./README.md#5-send-http-request)

# 1. Sensors used

- `BNO055` - Inertial Measurement Unit (IMU)
is a compact device that combines sensors such as accelerometers and gyroscopes to measure the orientation and movement of an object. It provides accurate data on acceleration and angular velocity, playing a crucial role in applications like inertial navigation and autonomous vehicles.
This module can return the following data:
  |        Data           |
  |-----------------------|
  | Temperature.          |
  | Magnetometer vector.  |
  | Gyro vector.          |
  | Accelerometer vector. |
  | Acceleration vector   |
  | Gravity vector.       |
  | Euler angles.         |

- `GY-NEO6MV2` - GPS
A GPS module uses signals from satellites to determine the exact location of an object. It's commonly used in navigation, tracking, and mapping applications, providing accurate real-time position data.
This module can retunr following data:

|NMEA Sentence                                    | Data                                                                                                |
|-------------------------------------------------|-----------------------------------------------------------------------------------------------------|
|$GPGLL (Geographic Position - Latitude/Longitude)|Latitude-Longitude-Time-Status-Mode Indicator                                                        |
|$GPRMC (Recommended Minimum Specific GNSS Data)  |Time-Status-Latitude-Longitude-Speed over ground-Course over ground                                  |
|$GPVTG (Track Made Good and Ground Speed)        |True Track-Magnetic Track-Ground Speed                                                               |
|$GPGGA (Global Positioning System Fix Data)      |Time-Latitude-Longitude-Fix Quality-Number of Satellites-HDOP-Altitude                               |
|$GPGSA (GPS DOP and Active Satellites)           |Mode-Fix Mode-Active Satellites-PDOP-HDOP-VDOP                                                       |
|$GPGSV (GPS Satellites in View)                  |Information about satellites in view, including satellite ID, elevation, azimuth, and signal strength|
|$GPGLL (Geographic Position - Latitude/Longitude)|Latitude-Longitude-Time-Status-Mode Indicator                                                        |

# 2. How to work with an esp32 from windows?

Download Python from the official website: [Python.org](https://www.python.org/). You can verify its installation and version in the Windows terminal with the command:

```bash
python --version 
```

To be able to manipulate ESP32 files you must use the ampy library, to use it you must install it following these steps from the Windows console:

```bash
pip install AMPY 
```

- command to view documents within esp32:

```bash
ampy --port "port_esp32" ls
```

- command to upload documents within esp32:

```bash
ampy --port "port_esp32" put "file_name"
```

- command to extract documents within esp32:

```bash
ampy --port "port_esp32" get "file_name"
```

- command to run documents within esp32:

```bash
ampy --port "port_esp32" run "file_name"
```

# 3. Obtaining data from sensors.

To extract data from the Inertial Measurement Unit `(IMU)` module using the ESP32, the I2C (Inter-Integrated Circuit) protocol is used. To use this, it is necessary to use an `SDA` (Serial Data Line) pin and a `SCL` (Serial Clock Line), in the ESP32 that is being used, `GPIO 22 is the SCL` and `GPIO 21 is the SDA`. The [`Bno055.py`](./Bno055.py) and [`Bno055_base.py`](./Bno055_base.py) files are responsible for generating communication under the I2C protocol as well as encoding and delivering the data that one wants to request.

- How to obtain data from the IMU?
```bash
#WThis file allows you to verify the operation of the BNO055 module

import machine
import time
from Bno055 import *

# scl and sda pins of the BNO055 module connected to the () pin of the esp32
scl_pin = 22
sda_pin = 21


i2c = machine.SoftI2C(scl=machine.Pin(scl_pin), sda=machine.Pin(sda_pin), timeout=100_000)

imu = BNO055(i2c)

calibrated = False
while True:
    time.sleep(1)
    if not calibrated:
        calibrated = imu.calibrated()
        print('Calibration required: sys {} gyro {} accel {} mag {}'.format(*imu.cal_status()))
    print('Temperature {}°C'.format(imu.temperature()))
    print('Mag       x {:5.0f}    y {:5.0f}     z {:5.0f}'.format(*imu.mag()))
    print('Gyro      x {:5.0f}    y {:5.0f}     z {:5.0f}'.format(*imu.gyro()))
    print('Accel     x {:5.1f}    y {:5.1f}     z {:5.1f}'.format(*imu.accel()))
    print('Lin acc.  x {:5.1f}    y {:5.1f}     z {:5.1f}'.format(*imu.lin_acc()))
    print('Gravity   x {:5.1f}    y {:5.1f}     z {:5.1f}'.format(*imu.gravity()))
    print('Heading     {:4.0f} roll {:4.0f} pitch {:4.0f}'.format(*imu.euler()))
```
This code is a simple way to start the IMU module and print all its data.

On the other hand, the `GPS` sensor uses serial communication that in this case the Universal Asynchronous Receiver / Transmitter `(UART)` will be used, to use this protocol it is necessary to use the `TX` and `RX` pins of the ESP32, which in this case are `GPIO 17 for TX` and `GPIO 16 for RX` (these pins represent communication for UART 2). The `GPS` sensor used contains a `NEO-6M module`, this is responsible for receiving, manipulating, and transforming the signals received by the satellites captured by the reception antenna, this same module is the one that sends the information received through the `UART` protocol. That is why in this case only `GPIO 16` is used since we are only going to listen to what the module sends.
- how to listen to the `NEO-6M` module?

```bash
from machine import UART

uart = UART(2, baudrate = 9600, rx = 16)

while True:
    if uart.any():
        print(uart.readline().decode('UTC-8'))
```
This code is a simple way to listen to `GPIO 16` and print the data it receives.
In this project for the `GPS` sensor you will find a file called [`Gps_information.py`](./Gps_information.py) which is used to pass the received data to variables with specific data.

## 3.1 How is data grouped?
- IMU module  
Once the IMU module is started, the following functions can be used:
  |Funtion|return|
  |-------|------|
  |.temperature()|Temperatura [°C]|
  |.mag()|Magnetometro vector [µT] - tuple: (x,y,z)|
  |.accel()|Accelerometer vector [m/s²] - tuple: (x,y,z)|
  |.gyro()|Gyro vector [DEG/s] - tuple: (x,y,z)|
  |.lin_acc()|Acceleration vector [m/s²] - tuple(x,y,z)|
  |.gravity()|Gravity vector [m/s²] - tuple: (x,y,z)|
  |.euler()| Euler angles [DEG] - tuple: (yaw, roll, pitch)|

The `NEO-6M` module sends standard sentences from the National Marine Electronics Association `(NMEA)`, these sentences are processed in the [`Gps_information.py`](./Gps_information.py) file. To use it, do it as follows:

```bash
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

```
`.getGps_information()` returns a `tuple` organized as follows:

|position|variable|
|--------|--------|
|0|latitude [dddmm.mmmm]|
|1|longitude [dddmm.mmmm]|
|2|local_time [hh:mm:ss]|
|3|date [dd.mm.yy]|
|4|ground_speed [knots]|
|5|satelites_in_view|
|6|satelites_in_use|
|7|Antenna_height [meters]|

# 4 Test files

In the Test/ street you will find 2 scripts that will help you identify the proper functioning of the sensors without the need to upload and execute all the files on the ESP32.

To use them you should upload the file you want along with the library you use:

|file|library|
|--------|--------|
|Bno055Test.py|Bno055.py|
|GpsTest.py|Gps_information.py|

# 5 Send HTTP request

To guarantee that HTTP requests can be made through the ESP32, it needs to be connected to the Internet. To do this, use the [Conecction.py](./Connection.py) file, which receives as an argument the name and password of the network to connect.

The [Send_Request.py](./Send_Requests.py) file is first responsible for collecting all the data obtained from both the Bno055 and GPS sensor and grouping them into a Json file that will later be sent by the body of the request. For this use, [Send_Request.py](./Send_Requests.py) will only need the url to which it sends the request and its body.

The library is already installed on the ESP32 so it will only be a matter of importing it:

``` bash x
import urequest
```
the instance that allows us to do this is:

``` bash x
urequests.post(self.url, json=json_body)
```

# 6 configurations file

The [Config.py](./Config.py) file stores variables that are constant throughout the program, in this case:

- network name
- password name 
- Url to Send HTPP request 
- SCL and SDA pin to which the Bno055 sensor is connected
- Tx pin to which the gps connects
- Time zone

Univerdiad Distrital Fransico Jose de Caldas
Grupo de investigacion CAS ( Ciruits And Systems ).