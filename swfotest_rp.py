import serial
import time


ser = serial.Serial('/dev/tty.usbserial-142420', 9600)

packet_length = 20
packet = bytearray(packet_length)
for x  in range(0,packet_length):
    packet[x] =  x
string  = ''.join('{0:02x}'.format(x) for x in packet)
ascii_packet = "TC" + string + "\n"
bytestring = bytes(ascii_packet,"UTF-8")
ser.write(bytestring)
print(bytestring)
ascii_packet = "SD" + string + "\n"
bytestring = bytes(ascii_packet,"UTF-8")
ser.write(bytestring)
print(bytestring)
ascii_packet = "XX" + string + "\n"
bytestring = bytes(ascii_packet,"UTF-8")
ser.write(bytestring)
print(bytestring)
ascii_packet = "TC" + string + "\n"
bytestring = bytes(ascii_packet,"UTF-8")
ser.write(bytestring)
print(bytestring)
ascii_packet = "SD" + string + "\n"
bytestring = bytes(ascii_packet,"UTF-8")
ser.write(bytestring)
print(bytestring)
ascii_packet = "RP" + "\n"
bytestring = bytes(ascii_packet,"UTF-8")
ser.write(bytestring)
print(bytestring)

