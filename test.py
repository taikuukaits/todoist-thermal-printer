from __future__ import print_function
import time
from JJ_Print.JJ_Todoist import JJ_Todoist
from JJ_Print.JJ_Todoist_Config import JJ_Todoist_Config

class MockPrinter:
    def println(self, msg):
        return print("printer: " + msg)
    def printImage(self, img, lat):
        return print("(Image Printed)")
    def feed(self, amt):
        return print("(Feed)")

config = {
  "refresh_time": 5,
  "token": "<REDACTED>",
  "morning_image": "M:\\Repositories\\thermal-printer\\JJ_Print\\Python_Thermal_Printer\\gfx\\coffee.png"
} 

todoist = JJ_Todoist(JJ_Todoist_Config(config), MockPrinter())


prevTime = 0
while(True):
    nextTime = time.time()
    tickTime = nextTime - prevTime
    if tickTime > 0.0:
        prevTime = nextTime
        todoist.tick(tickTime)