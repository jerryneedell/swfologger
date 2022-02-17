import busio
import time
import os
import board
import storage
import sys
import adafruit_sdcard
import digitalio

DATE_CODE = "20220217-00"
# configure serial port
ser = busio.UART(board.TX, board.RX, baudrate=9600, timeout=1,receiver_buffer_size=128)
# Connect to the card and mount the filesystem.
spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
cs = digitalio.DigitalInOut(board.SD_CS)
found_sdcard = False
try:
    sd = adafruit_sdcard.SDCard(spi, cs)
    found_sdcard = True
    vfs = storage.VfsFat(sd)
    storage.mount(vfs, '/sd')
except OSError as e:
    print("Unable to access SD Card: ",e)
    line="LOGGER NOTOK: " + str(e) +"\n"
    ser.write(bytes(line,"UTF-8"))



dumping_data = False

def get_data():
    global dumping_data
    data = None
    if ser.in_waiting:
        print(ser.in_waiting)
        try:
            data = ser.readline()
        except Exception as e:
            print("Error reading data: ",e)
            line="LOGGER NOTOK: read error: " + str(e) + "\n"
            ser.write(bytes(line,"UTF-8"))
    if data:
        print(ser.in_waiting, len(data))
        if data[len(data)-1] != 0x0a :
            print("missing newline\r\n")
            line="LOGGER NOTOK: missing newline\n"
            ser.write(bytes(line,"UTF-8"))
        if found_sdcard:
            try:
                with open("/sd/swfolog.txt","a") as logfile:
                    logfile.write(data)
            except Exception as e:
                print("Error writing data",e)
                line="LOGGER NOTOK: write error: " + str(e) + "\n"
                ser.write(bytes(line,"UTF-8"))
            if not dumping_data:
                if len(data) == 3 and data[0] == 0x52 and data[1] == 0x50:  # RP
                    print("Playback request\r\n")
                    if "swfoplayback.txt" not in os.listdir("/sd"):
                        os.rename("/sd/swfolog.txt","/sd/swfoplayback.txt")
                        print("Renamed Playback File\r\n")
                        line="LOGGER OK: Log file renamed\n"
                        ser.write(bytes(line,"UTF-8"))
                    line="LOGGER OK: Starting playback\n"
                    ser.write(bytes(line,"UTF-8"))
                    dumping_data = True
                elif len(data) == 3 and data[0] == 0x44 and data[1] == 0x50:  # DP
                    if "swfoplayback.txt" in os.listdir("/sd"):
                        print("Deleted Playback File\r\n")
                        os.remove("/sd/swfoplayback.txt")
                        line="LOGGER OK: Playback file deleted\n"
                        ser.write(bytes(line,"UTF-8"))
                    else:
                        print("No Playback File Found\r\n")
                        line="LOGGER OK: No Playback file found\n"
                        ser.write(bytes(line,"UTF-8"))
                elif len(data) == 5 and data[0] == 0x57 and data[1] == 0x49 and data[2] == 0x50 and data[3] == 0x45:  # WIPE
                    if "swfoplayback.txt" in os.listdir("/sd"):
                        print("Deleted Playback File\r\n")
                        os.remove("/sd/swfoplayback.txt")
                        line="LOGGER OK: Playback file deleted\n"
                        ser.write(bytes(line,"UTF-8"))
                    else:
                        print("No Playback File found\r\n")
                        line="LOGGER OK: No Playback file found\n"
                        ser.write(bytes(line,"UTF-8"))
                    if "swfolog.txt" in os.listdir("/sd"):
                        print("Deleted Log File\r\n")
                        os.remove("/sd/swfolog.txt")
                        line="LOGGER OK: Log file deleted\n"
                        ser.write(bytes(line,"UTF-8"))
                    else:
                        print("No Log File found\r\n")
                        line="LOGGER OK: No Log file found\n"
                        ser.write(bytes(line,"UTF-8"))
                    try:
                        with open("/sd/swfolog.txt","a") as logfile:
                            logfile.write(data)
                    except Exception as e:
                        print("Error writing data",e)
                        line="LOGGER NOTOK: write error: " + str(e) + "\n"
                        ser.write(bytes(line,"UTF-8"))
                if len(data) == 3 and data[0] == 0x53 and data[1] == 0x54:  # ST
                    print("Status request\r\n")
                    line="LOGGER OK: Date Code:"+ DATE_CODE + "\n"
                    ser.write(bytes(line,"UTF-8"))
            else:
                if len(data) == 3 and data[0] == 0x41 and data[1] == 0x42:  # AB
                    print("Abort Playback\r\n")
                    dumping_data = False
                    line="LOGGER OK: Playback Aborted\n"
                    ser.write(bytes(line,"UTF-8"))
        else:
                    line="LOGGER NOTOK: No SDCard\n"
                    ser.write(bytes(line,"UTF-8"))

while True:
    try:
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
                        line="LOGGER OK: Playback Completed\n"
                        ser.write(bytes(line,"UTF-8"))
                    get_data()
    except Exception as e:
        print("some error ocurred",e)
        line="LOGGER NOTOK: unknown error: " + str(e) + "\n"
        ser.write(bytes(line,"UTF-8"))

