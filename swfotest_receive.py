import serial
import time
import os
import sys

port = ''

if len(sys.argv) != 2:
    print("Usage:python3 swfotest_receive.py <PORT>")
    exit(0)

port = sys.argv[1]

ser = serial.Serial(port, 9600)

while True:
    #data = ser.read(ser.inWaiting())
    data = ser.read_until(expected=b'\n')
    if data:
        #if data[len(data)-1] != 0 :
        #    print("null terminator missing\rn")
        print([hex(x) for x in data])
        print(data)
        try:
            with open("swfotest.txt","a") as logfile:
                logfile.write(data.decode("UTF-8"))
        except UnicodeDecodeError as e:
            print("decode error",e)
    else:
        print(".",end='',flush=True)
