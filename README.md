# swfologger: SWFO Data Logger


## logger microcontroller hardware
* Adafruit Feather M0 Adalogger https://www.adafruit.com/product/2796
* Sandisk 4Gbyte SD Card MicroSD HC Class 4

## logger software
The SWFO logger software is written in Python for execution under CircuitPython https://github.com/adafruit/circuitpython

CircuitPython is Python implmentation for use with Microcontrollers.

The Adalogger board has the following firmware installed:

* Bootloader:bootloader-feather_m0_3.13.0.ino (installed via Arduino IDE)
https://github.com/jerryneedell/swfologger/blob/main/circuitpython/adalogger/bootloader-feather_m0_3.13.0.ino
* CircuitPython: V7.1.1
https://github.com/jerryneedell/swfologger/blob/main/circuitpython/adalogger/adafruit-circuitpython-feather_m0_adalogger-en_US-7.1.1.uf2

### CircuitPython libraries installed
```
adafruit_busdevice/
    i2c_device.mpy
    __init__.mpy
    spi_device.mpy
adafruit_sdcard.mpy
```
### operation
At boot CircuitPython executes a file named `code.py`.

The installed `code.py` contains the code from `circuitpython/adalogger/adalogger_swfologger.py`

All data sent to the logger is logged to the SDCard in a file named `sd/swfolog.txt` 
it is assumed that the data will consist only of Telecommands and Simulation Directives and they will be newline terminated ASCII strings beginning with

* "TC ...\n" (telecommand)
* "SD ..\n" (simulation directive)


### Special commands to playback data
* "RP\n" would request a replay.
* "DP\n" deletes swfoplayback.txt
* "WIPE\n" deletes both the swfoplayback.txt and swfolog.txt files

Commands reveived are also written to the log file.

when a playback is requested, the `swfolog.txt` file is renamed to `swfoplayback.txt` so incomming commands may still be logged to `swfolog.txt`

After successful playback `swfoplayback.txt` must be deleted.
If it is not, the rename will not occur and the same `swfoplayback.txt` will be sent again. `swfolog.txt` will continue to accumuate new data.


The normal sequence is:
```
Send data
Send RP
after playback complete
Send DP
```

It is OK to send an extra DP before any RP to make sure the `swfoplayback.txt` file has been deleded


### to test from another computer
(may want to use a virtual environment)
the test programs use pyserial
pip3 install pyserial

### test programs
to execute use: `python3 program.py  <UART PORT>`
e.g. `python3 swfotest_rp.py /dev/ttyUSB5`

* `swfotest_receive.py`  -- recives "playback" file from logger - saves as `swfotest.txt`
* `swfotest.py`  -- continually sends  TCs 
* `swfotest_rp.py` -- sends `RP` request playback
* `swfotest_delete` -- sends `DP` to delete the `swfoplayback.txt` file
* `swfotest_wipe.py` -- send `WIPE` to clear the SDCard
* `uart_logger.py` -- runs on system with SCSim and COSMOS -  relays all received commands (time code messages) to the logger
* `swfoscsim_logger.py` -- runs on system with SCSim and COSMOS - relays all received commands (time code messages) to the logger and generates fake HK and Mag packets (used in early testing)
* `swfoparse.py` -- scans a captured log playback file for sequence count errors (only looks at ApID 1 and ApID 500)

### updating the swfologger program
If changes are made to the `adalogger_swfologger.py` code, then it can be installed as follows:
* copy the updated `adalogger_swfologger.py` to a file name `code.py`
* connect the computer wit the updated `code.py` file to the adalogger microUSB socket
* The computer will mount a USB Fash Drive named `CIRCUITPY`
* copy the new `code.py` to the `CIRCUITPY` drive -- use command line copy or drag/drop - and overwrite the existing `code.py` file.
* The logger will reboot automatically. 
* Eject the `CIRCUITPY` drive - waitf for it to confirm that it has been properly ejected and is save to remove.
* Disconnect the microUSB cable.
* RESET or power cycle the swfologger- there is a RESET button on the top of the board.
* Confirm normal operation.

