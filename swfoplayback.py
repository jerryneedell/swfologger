import serial
import time
import os

ser = serial.Serial('/dev/serial0', 9600, timeout=1)


with open("swfoplayback.txt","r") as playbackfile:
    dumping_data = True
    while dumping_data:
        line=playbackfile.readline()
        if line:
            ser.write(bytes(line,"UTF-8"))
            print(line)
        else:
            dumping_data = False
            print("End of Playback")
