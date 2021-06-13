import busio
import time
import os
import board
import sdioio
import storage
import sys

sd = sdioio.SDCard(clock=board.SDIO_CLOCK,command=board.SDIO_COMMAND,data=board.SDIO_DATA,frequency=25000000)
#sd = sdioio.SDCard(clock=board.SDIO_CLOCK,command=board.SDIO_COMMAND,data=board.SDIO_DATA,frequency=5000000)
vfs = storage.VfsFat(sd)
storage.mount(vfs, '/sd')
sys.path.append("/sd")
sys.path.append("/sd/lib")


ser = busio.UART(board.TX, board.RX, baudrate=9600, timeout=1)

dumping_data = False

def get_data():
    global dumping_data
    data = None
    if ser.in_waiting:
        print(ser.in_waiting)
        data = ser.readline()
        print(ser.in_waiting, len(data))
    if data:
        if data[len(data)-1] != 0x0a :
            print("missing newline\r\n")
        try:
            with open("/sd/swfolog.txt","a") as logfile:
                logfile.write(data.decode("UTF-8"))
        except Exception as e:
            print("decode error",e)
        if not dumping_data:
            if data[0] == 0x52 and data[1] == 0x50:  # RP
                print("Playback request\r\n")
                os.rename("/sd/swfolog.txt","/sd/swfoplayback.txt")
                dumping_data = True
        if data[0] == 0x48 and data[1] == 0x41 and data[2] == 0x4C and data[3] == 0x54:  # HALT
            print("Shutdown request not implemented\r\n")

while True:
    get_data()
    if dumping_data:
        with open("/sd/swfoplayback.txt","r") as playbackfile:
            while dumping_data :
                line=playbackfile.readline()
                if line:
                    ser.write(bytes(line,"UTF-8"))
                else:
                    dumping_data = False
                    print("End of Playback")
                    print("Deleted Playback File\r\n")
                    os.remove("/sd/swfoplayback.txt")
                get_data()

