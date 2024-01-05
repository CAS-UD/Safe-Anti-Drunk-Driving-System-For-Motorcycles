# Collection and sending of data through HTTP protocol with ESP32

This project aims to collect and send sensor data using the HTTP protocol and the POST request with the ESP32 microcontroller. At the moment, an Inertial Measurement Unit (IMU) module is being used, which functions as a magnetometer, gyroscope, accelerometer, linear accelerometer, Euler angle meter, gravitational force meter and environmental thermometer. Additionally, the GY-NEO6MV2 sensor is used, which is a Global Positioning Systems (GPS) sensor which gives us position information, time zone, speed, etc.

# Contents

1. [Sensors used](./README.md#1-sensors-used)
 2. [How to work with an esp32 from windows?](./README.md#2-how-to-work-with-an-esp32-from-windows)
 3. [Obtaining data from sensors](./README.md#3-obtaining-data-from-sensors)  
  3.1 [PulluHow is data grouped?](./README.md#31-how-is-data-grouped)



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
import machine
import time
from Bno055 import *

i2c = machine.SoftI2C(scl=machine.Pin(22), sda=machine.Pin(21), timeout=100_000)
imu = BNO055(i2c)
while True:
    time.sleep(1)
    print("temperature: ", imu.temperature())
    print("magnetometer: ", imu.mag())
    print("accelerometer: ", imu.accel())
    print("gyroscope: ", imu.gyro())
    print("linear_accelerometer: ", imu.lin_acc())
    print("gravity: ", imu.gravity())
    print("euler angles: ", imu.euler())
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
from Gps_information import *

gps = Gps_information()

gps.nmeaSentenceOrganizer(time_zone, nmea_sentence)

print(gps.getGps_information())

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
