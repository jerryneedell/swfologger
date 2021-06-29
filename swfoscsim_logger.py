import serial
import time


ser = serial.Serial('/dev/ttyUSB0', 38400)
ser_logger = serial.Serial('/dev/ttyUSB5', 9600)
# Set up byte array for housekeeping packet
hk_apid = 0x4e4
hk_pktlen = 68 - 7
hk_seqcnt = 0
hk_packet = bytearray(( (hk_apid//256) | 0x08, hk_apid & 0xff, 
                      0, 0,   # seqcnt
                      hk_pktlen//256, hk_pktlen & 0xff, 
                      0,0,0, # day
                      0,0,0,0, # ms of day
                      0,0, # usec
                      0,   # spare
                      0,0,0,0, # wd 0: cmd_acc (8), scb0 status (24)
                      0,0,0,0, # wd 1: cmd_rej (8), scb1 status (24)
                      0,0,0,0, # wd 2: acc fc (8), misc (24)
                      0,0,0,0, # wd 3: rej fc (8), misc (24)
                      0,0,0,0, # wd 4
                      0,0,0,0, # wd 5
                      0,0,0,0, # wd 6
                      0,0,0,0, # wd 7
                      0,0,0,0, # wd 8
                      0,0,0,0, # wd 9
                      0,0,0,0, # wd 10
                      0,0,0,0, # wd 11
                      0,0,0,0)) # wd 12

# Set up byte array for mag vector packet
vec_apid = 0x4e5
vec_seqcnt = 0
vec_packet = bytearray(( (vec_apid//256) | 0x08, vec_apid & 0xff,
                       0,0,     # seqcnt
                       0,0,     # packet length field
                       0,0,0,   # day
                       0,0,0,0, # ms of day
                       0,0,     # usec
                       0,       # spare
                       0,0,0,0, # flags
                       0,0,0,0,0,0,0,0,0, # SCB-0 X
                       0,0,0,0,0,0,0,0,0, # SCB-0 Y
                       0,0,0,0,0,0,0,0,0, # SCB-0 Z
                       0,0,0,0,0,0,0,0,0, # SCB-1 X
                       0,0,0,0,0,0,0,0,0, # SCB-1 Y
                       0,0,0,0,0,0,0,0,0)) # SCB-1 Z

mag_cadence = 1
#mag_cadence = 0
hk_cadence = 8
tmsg_days=0
tmsg_msecs=0
tmsg_usecs=0
time_tag = 0
last_hk = 0
last_mag = 0
hk_seqcnt = 0
vec_seqcnt = 0
time_msg_apid = 1
while True:
    offset = 0
    multipacket = True
    data = ser.read(ser.inWaiting())
    if data :
        print([hex(x) for x in data])
        while multipacket:
            # Decode primary header
            apid    = (data[offset+0] * 256 + data[offset+1]) & 0x7ff
            seq_cnt = (data[offset+2] * 256 + data[offset+3]) & 0x3fff
            plen    = data[offset+4] * 256 + data[offset+5]

            if apid == time_msg_apid: # Time message
                tmsg_days  = (data[offset+6] * 256 + data[offset+7]) * 256 + data[offset+8]
                tmsg_msecs = ((data[offset+9] * 256 + data[offset+10]) * 256 + data[offset+11]) * 256 + data[offset+12]
                tmsg_usecs = data[offset+13] * 256 + data[offset+14]
                print("Received Time Message: days = %06x  msecs = %08x  usecs = %04x" % (tmsg_days, tmsg_msecs, tmsg_usecs))
            logger_string = ''.join('{0:02x}'.format(x) for x in data[offset:offset+plen+7])
            logger_string = "TC" + logger_string + "\n"
            logger_bytestring = bytes(logger_string,"UTF-8")
            ser_logger.write(logger_bytestring)
            offset = offset + plen + 7
            if len(data) != offset: 
                print(">>> multiple packets received. Looking for new packet")
                print(plen,len(data),offset)
            else:
                multipacket = False
    if (hk_cadence > 0) and ((time.monotonic() - last_hk) > hk_cadence) :
        last_hk=time.monotonic()

        # Update sequence count in primary header
        hk_seqcnt = (hk_seqcnt + 1) & 0x3fff # 14 bits
        hk_packet[2] = 0xC0 | (hk_seqcnt >> 8)
        hk_packet[3] = hk_seqcnt & 0xff

        # Update time code in secondary header
        hk_packet[6] = (tmsg_days >> 16) & 0xff
        hk_packet[7] = (tmsg_days >> 8) & 0xff
        hk_packet[8] = tmsg_days & 0xff

        hk_packet[9]  = (tmsg_msecs >> 24) & 0xff
        hk_packet[10] = (tmsg_msecs >> 16) & 0xff
        hk_packet[11] = (tmsg_msecs >> 8) & 0xff
        hk_packet[12] = tmsg_msecs & 0xff


        # Update telemetry items
        for i in range(hk_pktlen + 7 - 16):
           hk_packet[16 + i] = i

        ser.write(hk_packet[0:hk_pktlen+7])


    if (mag_cadence > 0)   and ((time.monotonic() - last_mag) > mag_cadence) :
        last_mag=time.monotonic()
        # Mag vector packet: once per second
        vec_seqcnt = (vec_seqcnt + 1) & 0x3fff # 14 bits

        # packet length:
        # 16 bytes header, 4 bytes flags, 6*9 bytes components
        plen = 16 + 4 + 6*9 - 7

        # Update primary header
        vec_packet[2] = 0xC0 | (vec_seqcnt >> 8)
        vec_packet[3] = vec_seqcnt & 0xff
        vec_packet[4] = (plen >> 8) & 0xff
        vec_packet[5] = plen & 0xff

        # Update time code in secondary header
        vec_packet[6] = (tmsg_days >> 16) & 0xff
        vec_packet[7] = (tmsg_days >> 8) & 0xff
        vec_packet[8] = tmsg_days & 0xff

        vec_packet[9]  = (tmsg_msecs >> 24) & 0xff
        vec_packet[10] = (tmsg_msecs >> 16) & 0xff
        vec_packet[11] = (tmsg_msecs >> 8) & 0xff
        vec_packet[12] = tmsg_msecs & 0xff

        # Update telemetry items
        vec_packet[16] = 0xaa # flags
        vec_packet[17] = 0xbb # flags
        vec_packet[18] = 0xcc # flags
        vec_packet[19] = 0xdd # flags
        for i in range(6*9):
            vec_packet[20+i] = 0x00 + i

        ser.write(vec_packet[0:plen+7])
