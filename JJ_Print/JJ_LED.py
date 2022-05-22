import argparse
import json

from JJ_Print.JJ_LED_Config import JJ_LED_Config

class JJ_LED:

    def __init__(self, led_config, GPIO):
        self.GPIO = GPIO
        self.pin = led_config.led_pin

        self.led_state = False

        self.freq = 0
        self.freq_change = 10 # per second
        
        GPIO.setup(self.pin, GPIO.OUT)
        self.pwm = GPIO.PWM(self.pin, 1000)
        self.pwm.start(self.freq)

    def finish(self):
        print("LED finished.")
        self.pwm.stop()

    def tick(self, time):
        self.freq += self.freq_change * time
        if self.freq > 100:
            self.freq = 100
            self.freq_change = -self.freq_change
        if self.freq < 0:
            self.freq = 0
            self.freq_change = -self.freq_change
        self.pwm.ChangeDutyCycle(self.freq)
        
                   
