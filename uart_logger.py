import serial
import time

ser = serial.Serial('/dev/ttyUSB0', 38400)
ser_logger = serial.Serial('/dev/ttyUSB5', 9600)

while True:
    offset = 0
    multipacket = True
    data = ser.read(ser.inWaiting())
    if data :
        print(len(data),ser.inWaiting())
        start=time.monotonic()
        print([hex(x) for x in data])
        while multipacket:
            # Decode primary header
            apid    = (data[offset+0] * 256 + data[offset+1]) & 0x7ff
            seq_cnt = (data[offset+2] * 256 + data[offset+3]) & 0x3fff
            plen    = data[offset+4] * 256 + data[offset+5]
            oldoffset = offset
            offset = offset + plen + 7
            if len(data) < offset: 
                print(">>> incomplete packet received. Looking for remainder")
                print(plen,len(data),offset)
                while not ser.inWaiting():
                    pass
                print(time.monotonic()-start)
                print(ser.inWaiting())
                data = data + ser.read(ser.inWaiting())
                if data :
                    print(len(data),ser.inWaiting())
                    print([hex(x) for x in data])

            logger_string = ''.join('{0:02x}'.format(x) for x in data[oldoffset:oldoffset+plen+7])
            logger_string = "TC" + logger_string + "\n"
            logger_bytestring = bytes(logger_string,"UTF-8")
            ser_logger.write(logger_bytestring)
            if len(data) != offset: 
                print(">>> multiple packets received. Looking for newpacket")
                print(plen,len(data),offset)
            else:
                multipacket = False



