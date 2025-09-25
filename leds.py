from gpiozero import LED
import RPi.GPIO as gpio
gpio.cleanup()
led_verte = LED(17)
led_orange = LED(22)
led_rouge = LED(27)

