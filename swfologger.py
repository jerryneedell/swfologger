import serial
import time
import os

ser = serial.Serial('/dev/serial0', 9600, timeout=1)
dumping_data = False

def get_data():
    global dumping_data
    data = None
    if ser.in_waiting:
        #print(ser.in_waiting)
        data = ser.read_until(expected=b'\n')
        #print(ser.in_waiting, len(data))
    if data:
        if data[len(data)-1] != 0x0a :
            print("missing newline\r\n")
        try:
            with open("/home/pi/logger/swfolog.txt","a") as logfile:
                logfile.write(data.decode("UTF-8"))
        except UnicodeDecodeError as e:
            print("decode error",e)
        if not dumping_data:
            if data[0] == 0x52 and data[1] == 0x50:  # RP
                print("Playback request\r\n")
                if not os.path.exists("/home/pi/logger/swfoplayback.txt"):
                    os.rename("/home/pi/logger/swfolog.txt","/home/pi/logger/swfoplayback.txt")
                dumping_data = True
            elif data[0] == 0x44 and data[1] == 0x50:  # DP
                if os.path.exists("/home/pi/logger/swfoplayback.txt"):
                    print("Deleted Playback File\r\n")
                    os.remove("/home/pi/logger/swfoplayback.txt")
                else:
                    print("No Playback File found\r\n")
        if data[0] == 0x48 and data[1] == 0x41 and data[2] == 0x4C and data[3] == 0x54:  # HALT
            print("Shutdown request\r\n")
            os.system("sudo shutdown -h now ")

while True:
    get_data()
    if dumping_data:
        with open("/home/pi/logger/swfoplayback.txt","r") as playbackfile:
            while dumping_data :
                line=playbackfile.readline()
                if line:
                    ser.write(bytes(line,"UTF-8"))
                else:
                    dumping_data = False
                    print("End of Playback")
                get_data()

