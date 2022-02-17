import serial
import time
import sys

port = ''

if len(sys.argv) != 2:
    print("Usage:python3 swfotest_status.py <PORT>")
    exit(0)

port = sys.argv[1]

ser = serial.Serial(port, 9600)
ascii_packet = "ST" + "\n"
bytestring = bytes(ascii_packet,"UTF-8")
ser.write(bytestring)
print(bytestring)
