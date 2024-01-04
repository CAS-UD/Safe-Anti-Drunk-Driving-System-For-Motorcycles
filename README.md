# Collection and sending of data through HTTP protocol with ESP32

This project aims to collect and send sensor data using the HTTP protocol and the POST request with the ESP32 microcontroller. At the moment, an Inertial Measurement Unit (IMU) module is being used, which functions as a magnetometer, gyroscope, accelerometer, linear accelerometer, Euler angle meter, gravitational force meter and environmental thermometer. Additionally, the GY-NEO6MV2 sensor is used, which is a Global Positioning Systems (GPS) sensor which gives us position information, time zone, speed, etc.

## content

1. [1. Sensors used](./README.md#1-sensors-used)
2. [2. How to work with an esp32 from windows?](./README.md#2-how-to-work-with-an-esp32-from-windows)

## 1. Sensors used

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

## 2. How to work with an esp32 from windows?

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
