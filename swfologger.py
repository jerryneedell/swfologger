import serial
import time


ser = serial.Serial('/dev/serial0', 9600, timeout=1)


while True:
    #data = ser.read(ser.inWaiting())
    data = ser.read_until(expected=b'\0')
    if data :
        if data[len(data)-1] != 0 :
            print("null terminator missing\rn")
        print([hex(x) for x in data])
        print(data)
        try:
            with open("swfolog.txt","a") as logfile:
                logfile.write(data[0:len(data)-1].decode("UTF-8")+"\r\n")
        except UnicodeDecodeError as e:
            print("decode error",e)
