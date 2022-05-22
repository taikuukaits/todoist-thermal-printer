import argparse
import json

from JJ_Print.JJ_Button_Config import JJ_Button_Config

class JJ_Button:

    def __init__(self, button_config, GPIO, tap, hold):
        self.GPIO = GPIO
        self.pin = button_config.button_pin
        self.invert_pin = button_config.invert_pin
        self.hold_time = button_config.hold_time
        self.tap_time = button_config.tap_time
        self.debounce_time = button_config.debounce_time

        self.button_state = False
        self.press_time = 0

        self.tap = tap
        self.hold = hold

        self.GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def tick(self, time):
        self.button_state = self.GPIO.input(self.pin)
        if self.invert_pin:
            self.button_state = not self.button_state

        if self.button_state:
            self.press_time += time
        else:
            if self.press_time > self.debounce_time:
                if self.press_time > self.hold_time:
                    self.hold()
                elif self.press_time > self.tap_time:
                    self.tap()
            self.press_time = 0

    def finish(self):
        print("Button finished.")
