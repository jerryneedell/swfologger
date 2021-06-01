import serial
import time


ser = serial.Serial('/dev/serial0', 9600)


while True:
    #data = ser.read(ser.inWaiting())
    data = ser.read_until(expected=b'\0')
    if data :
        print([hex(x) for x in data])
        print(data)
