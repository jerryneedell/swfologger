

last_seq1 = 0
last_seq500 = 0
playbackfile =  open("swfotest.txt","r")
while True:
    line=playbackfile.readline()
    if line:
        if line[0:2] == 'TC':
            apid = (256*int(line[2:4],16) + int(line[4:6],16)) & 0x7ff
            seq =  (256*int(line[6:8],16) + int(line[8:10],16)) & 0x3ff
            if apid == 0x1:
                if seq != last_seq1 + 1:
                    if last_seq1 == 0x3ff and seq == 0:
                        print("seq1 wraparound")
                    else:
                        print("seq error",line)
                        print(hex(last_seq1),hex(seq))
                last_seq1 = seq
            if apid == 0x500:
                if seq != last_seq500 + 1:
                    if last_seq1 == 0x3ff and seq == 0:
                        print("seq500 wraparound")
                    else:
                        print("seq error",line)
                        print(hex(last_seq500),hex(seq))
                last_seq500 = seq
        else:
            print(line)
    else:
        print("End of PLayback")
        break
playbackfile.close()
