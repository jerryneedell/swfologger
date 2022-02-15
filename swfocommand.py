import serial
import time
import sys

port = ''

if len(sys.argv) != 2:
    print("Usage:python3 swfotest.py <PORT>")
    exit(0)

port = sys.argv[1]

ser = serial.Serial(port, 9600)


bytestring =  b'\x00\x01\x02\x0a'

while True:
    c = input("next byte")
    if c == 'x':
        ser.write(b'\x0a')
    else:
        ser.write(bytes(c,"UTF-8"))

