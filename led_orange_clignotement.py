# -*- coding: utf-8 -*-
from gpiozero import LED
from time import sleep
from leds import led_orange


try:
    while True:
        led_orange.on()
        sleep(0.4)
        led_orange.off()
        sleep(0.4)
    
 
   
except KeyboardInterrupt:
    led_orange.on()
