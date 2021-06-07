import serial
import time


ser = serial.Serial('/dev/tty.usbserial-142420', 9600)

ascii_packet = "DP" + "\n"
bytestring = bytes(ascii_packet,"UTF-8")
ser.write(bytestring)
print(bytestring)

