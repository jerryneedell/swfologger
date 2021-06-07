import serial
import time


ser = serial.Serial('/dev/tty.usbserial-142420', 9600)

packet_length = 20
packet = bytearray(packet_length)
for x  in range(0,packet_length):
    packet[x] =  x
string  = ''.join('{0:02x}'.format(x) for x in packet)
ascii_packet = "TC1" + string + "\n"
bytestring = bytes(ascii_packet,"UTF-8")
ser.write(bytestring)
print(bytestring)
ascii_packet = "SD1" + string + "\n"
bytestring = bytes(ascii_packet,"UTF-8")
ser.write(bytestring)
print(bytestring)
time.sleep(.1)
ascii_packet = "XX1" + string + "\n"
bytestring = bytes(ascii_packet,"UTF-8")
ser.write(bytestring)
print(bytestring)
time.sleep(.1)
ascii_packet = "TC2" + string + "\n"
bytestring = bytes(ascii_packet,"UTF-8")
ser.write(bytestring)
print(bytestring)
time.sleep(.1)
ascii_packet = "SD2" + string + "\n"
bytestring = bytes(ascii_packet,"UTF-8")
ser.write(bytestring)
print(bytestring)
time.sleep(.1)
ascii_packet = "RP" + "\n"
bytestring = bytes(ascii_packet,"UTF-8")
ser.write(bytestring)
print(bytestring)
time.sleep(.1)
ascii_packet = "TC3" + string + "\n"
bytestring = bytes(ascii_packet,"UTF-8")
ser.write(bytestring)
print(bytestring)
time.sleep(.1)
ascii_packet = "TC4" + string + "\n"
bytestring = bytes(ascii_packet,"UTF-8")
ser.write(bytestring)
print(bytestring)
time.sleep(.1)
ascii_packet = "TC5" + string + "\n"
bytestring = bytes(ascii_packet,"UTF-8")
ser.write(bytestring)
print(bytestring)
time.sleep(.1)
ascii_packet = "TC6" + string + "\n"
bytestring = bytes(ascii_packet,"UTF-8")
ser.write(bytestring)
print(bytestring)
time.sleep(.1)
ascii_packet = "TC7" + string + "\n"
bytestring = bytes(ascii_packet,"UTF-8")
ser.write(bytestring)
print(bytestring)
time.sleep(.1)

