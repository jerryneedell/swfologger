import serial
import time
import os

ser = serial.Serial('/dev/serial0', 9600, timeout=1)


while True:
    #data = ser.read(ser.inWaiting())
    data = ser.read_until(expected=b'\n')
    if data:
        #if data[len(data)-1] != 0 :
        #    print("null terminator missing\rn")
        print([hex(x) for x in data])
        print(data)
        try:
            with open("swfolog.txt","a") as logfile:
                logfile.write(data.decode("UTF-8"))
        except UnicodeDecodeError as e:
            print("decode error",e)
        if data[0] == 0x52 and data[1] == 0x50:  # RP
            print("Playback request\r\n")
            os.rename("swfolog.txt","swfoplayback.txt")
            with open("swfoplayback.txt","r") as playbackfile:
                dumping_data = True
                while dumping_data:
                    line=playbackfile.readline()
                    if line:
                        print(line)
                    else:
                        dumping_data = False
                        print("End of Playback")
    else:
        print("nothing received - waiting")
