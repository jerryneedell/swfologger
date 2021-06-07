import serial
import time


ser = serial.Serial('/dev/ttyUSB5', 9600)

ascii_packet = "RP" + "\n"
bytestring = bytes(ascii_packet,"UTF-8")
ser.write(bytestring)
print(bytestring)
