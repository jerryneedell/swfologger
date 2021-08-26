import adafruit_sdcard
import busio
import digitalio
import board
import storage
import sys
import os
# Connect to the card and mount the filesystem.
spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
cs = digitalio.DigitalInOut(board.SD_CS)
sdcard = adafruit_sdcard.SDCard(spi, cs)
vfs = storage.VfsFat(sdcard)
storage.mount(vfs, "/sd")
sys.path.append("/sd")

# Use the filesystem as normal.
with open("/sd/test.txt", "w") as f:
    f.write("Hello world\n")
print(os.listdir("/sd"))

