from machine import UART


x = UART(2, baudrate = 9600, rx = 16)

while True:
    if x.any():
        print(x.readline().decode('UTF-8'))
