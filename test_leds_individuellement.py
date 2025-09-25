# -*- coding: utf-8 -*-
from gpiozero import LED
from time import sleep

led_verte = LED(17)
led_orange = LED(22)
led_rouge = LED(27)

def all_on():
    led_verte.off()
    led_orange.off()
    led_rouge.off()
    
def all_off():
    led_verte.on()
    led_orange.on()
    led_rouge.on()

try:
    all_on()
    sleep(2)
    all_off()
    
    print("LED VERTE")
    sleep(2)
    led_verte.off()
    sleep(2)
    all_off()
    
    print("LED orange")
    sleep(2)
    led_orange.off()
    sleep(2)
    all_off()
    
    print("LED rouge")
    sleep(2)
    led_rouge.off()
    sleep(2)
    all_off()
 
   
except KeyboardInterrupt:
    all_off()
