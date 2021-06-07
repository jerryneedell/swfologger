import serial
import time
import os

ser = serial.Serial('/dev/serial0', 9600, timeout=.1)


while True:
    #data = ser.read(ser.inWaiting())
    data = ser.read_until(expected=b'\n')
    if data:
        if data[len(data)-1] != 0x0a :
            print("newline terminator missing\rn")
        print([hex(x) for x in data])
        print(data)
        try:
            with open("swfolog.txt","a") as logfile:
                logfile.write(data.decode("UTF-8"))
        except UnicodeDecodeError as e:
            print("decode error",e)
        if data[0] == 0x52 and data[1] == 0x50:  # RP
            print("Playback request\r\n")
            if not os.path.exists("swfoplayback.txt"):
                os.rename("swfolog.txt","swfoplayback.txt")
            os.system("python3 swfoplayback.py &")
        elif data[0] == 0x44 and data[1] == 0x50:  # DP
            print("Deleted Playback File\r\n")
            os.remove("swfoplayback.txt")
    else:
        print(".",end = '', flush = True)
