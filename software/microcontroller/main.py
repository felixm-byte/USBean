from ST7735 import TFT
from sysfont import sysfont
from machine import SPI,Pin
import sys
import select
import machine

# Setup onboard LED
led = machine.Pin(25, machine.Pin.OUT)
poll_obj = select.poll()
poll_obj.register(sys.stdin, select.POLLIN)
spi = SPI(2, baudrate=20000000, polarity=0, phase=0, sck=Pin(2), mosi=Pin(3), miso=Pin(-1), cs=Pin(5))
tft=TFT(spi,2,3)
tft.initr()
tft.rgb(True)


while True:
    # Check if data is waiting in the USB serial buffer
    if poll_obj.poll(0):
        # Read the incoming message and remove whitespace
        message = sys.stdin.readline().strip().lower()
        
        if message:
            print("Recieved:")
            print(message)
            tft.fill(TFT.BLACK)
            tft.text((0, 30), {message}, TFT.RED, sysfont, 1, nowrap=False)
