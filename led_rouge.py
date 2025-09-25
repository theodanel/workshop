# -*- coding: utf-8 -*-
from gpiozero import LED
from leds import led_rouge
import time

led_rouge.on()
time.sleep(1000)
led_rouge.off()

