# swfologger
SWFO data logger


##logger computer
Raspberry P zero 
swfologger.local  via ssh — if ethernet connected
install RaspiOS lite
use raspi-config to
    enable UART0 — disable Serial Console
    set local to UTF-8, TZ to UTC

install needed tools
sudo apt-get install python3-pip
sudo pip3 install --upgrade setuptools
sudo apt-get install git


created github repo https://github.com/jerryneedell/swfologger.git

## logger software
*swfologger.py is the logger code
*swfoplayback.py is called by the loggger when required

both are placed in /usr/local/bin
logged data is stored in /home/pi/logger

any data sent to the logger is logged to a file named swfolog.txt
it is assumed ahat the data will consist only of Telecommands and Simulation Directives and they will newline terminated ASCII strings beginning with

*"TC ...\n" (telecommand)
*"SD ..\n." (simulation directive)

when a playback is requested, the swfolog.txt file is renamed to swfoplayback.txt so incomming commands may still be logged to swfolof.txt

After successful playback swfoplayback.txt must be deleted.
If it is not, the rename will not occur and the same swfoplayback.txt will be sent again. (swfologtxt will continue to accumuate new data.

##Special commands
*"RP\n" would request a replay.
*"DP\n" deletes swfoplayback.txt “HALT” shutdown the Pi
*"HALT\n" shuts down the logger - power cycel needed to restart.



The normal sequence is:
Send data
Send RP
after playback complete
Send DP

It is also safe to send a DP before an RP to make sure the swfoplayback.txt file has been deleded




#to test from another computer
(may want to use a virtual environment)
the test programs use pyserial
pip3 install pyserial

#test programs
to execute use: python3 program.py  <UART PORT>
e.g. python3 swfotest_rp.py /dev/ttyUSB5

*swfotest_receive.py  -- recives "playback" file from logger - saves as swfotest.txt
*swfotest.py  -- contiunatlly sends  TCs 
*swfotest_rp.py -- sends RP request playback
*swfotest_delete -- sends DP to deleted the swfoplayback.txt file
*swfotest_halt.py -- send HALT to shutdown the logger
*swfoscsim_logger.py -- runs on system with SCSIm and COSMOS - relays all receivd commands (time code messages) to the logger



#systemd service
on the Raspberry Pi swfologger.py is automatically started on boot vi a systemd service
It was installed as follows
create swfologger.service containing
[Unit]
Description=SWFO Data Logger
After=multi-user.target

[Service]
Type=idle
User=pi
ExecStart=/usr/bin/python3 /usr/local/bin/swfologger.py
Restart=always

[Install]
WantedBy=multi-user.target



to install the service
sudo cp swfologger.service /lib/systemd/system
sudo chmod 644 /lib/systemd/system/swfologger.service 
sudo systemctl daemon-reload
sudo systemctl enable swfologger.service 

either reboot or 
sudo systemctl start swfologger.service

