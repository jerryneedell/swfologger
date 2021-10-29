# swfologger
SWFO data logger


## logger microcontroller
Adafruit Feather M0 Adalogger https://www.adafruit.com/product/2796

## logger software
Bootloader:bootloader-feather_m0_3.13.0.bin
CirCuitPython: V7.0.0
https://github.com/jerryneedell/swfologger/blob/main/circuitpython/adalogger/adafruit-circuitpython-feather_m0_adalogger-en_US-7.0.0.uf2

libraries:
```
    adafruit_busdevice/
        i2c_device.mpy
        __init__.mpy
        spi_device.mpy
    adafruit_sdcard.mpy
```
At boot CircuitPython executes a file name code.py
code.py contains the executable code from adalogger_swfologger.py

any data sent to the logger is logged to the SDCard in a file named `sd/swfolog.txt` 
it is assumed ahat the data will consist only of Telecommands and Simulation Directives and they will newline terminated ASCII strings beginning with

* "TC ...\n" (telecommand)
* "SD ..\n." (simulation directive)

when a playback is requested, the `swfolog.txt` file is renamed to `swfoplayback.txt` so incomming commands may still be logged to `swfolog.txt`

After successful playback `swfoplayback.txt` must be deleted.
If it is not, the rename will not occur and the same `swfoplayback.txt` will be sent again. `swfolog.txt` will continue to accumuate new data.

## Special commands
* "RP\n" would request a replay.
* "DP\n" deletes swfoplayback.txt “HALT” shutdown the Pi
* "WIPE\n" deletes both the swfoplayback.txt and swfolog.txt files


The normal sequence is:
```
Send data
Send RP
after playback complete
Send DP
```

It is OK to send an extra DP before any RP to make sure the `swfoplayback.txt` file has been deleded




# to test from another computer
(may want to use a virtual environment)
the test programs use pyserial
pip3 install pyserial

# test programs
to execute use: `python3 program.py  <UART PORT>`
e.g. `python3 swfotest_rp.py /dev/ttyUSB5`

* `swfotest_receive.py`  -- recives "playback" file from logger - saves as `swfotest.txt`
* `swfotest.py`  -- continually sends  TCs 
* `swfotest_rp.py` -- sends `RP` request playback
* `swfotest_delete` -- sends `DP` to deleted the `swfoplayback.txt` file
* `swfotest_wipe.py` -- send `WIPE` to clear the SDCard
* `swfoscsim_logger.py` -- runs on system with SCSIm and COSMOS - relays all receivd commands (time code messages) to the logger


