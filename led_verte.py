# -*- coding: utf-8 -*-
from gpiozero import LED
from leds import led_verte
import time


led_verte.on()
time.sleep(1000)
led_verte.off()

