from __future__ import print_function
import subprocess
import time
import socket
from PIL import Image

#from JJ_Print.JJ_GPIO import JJ_GPIO
from JJ_Print.JJ_Config import JJ_Config
from JJ_Print.JJ_Printer import JJ_Printer
from JJ_Print.JJ_Button import JJ_Button
from JJ_Print.JJ_LED import JJ_LED
from JJ_Print.JJ_Todoist import JJ_Todoist
from JJ_Print.JJ_Application_Config import JJ_Application_Config

class JJ_Application:

    def __init__(self, GPIO):
        self.GPIO = GPIO

    def boot(self):
        self.config = JJ_Config.fromArgs()
        self.application_config = self.config.application_config
        self.printer = JJ_Printer.fromConfig(self.config.printer_config)
        self.led = JJ_LED(self.config.led_config, self.GPIO)
        self.todoist = JJ_Todoist(self.config.todoist_config, self.printer)

        self.button = JJ_Button(self.config.button_config, self.GPIO, self.tap, self.hold)
        self.stop_next_tick = False
        self.shutdown_next_tick = False

        #self.printer.printImage(Image.open(self.application_config.welcome_image), True)
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(('8.8.8.8', 0))
            self.printer.print('My IP address is ' + s.getsockname()[0])
            self.printer.feed(3)
        except:
            self.printer.boldOn()
            self.printer.println('Network is unreachable.')
            self.printer.boldOff()
            self.printer.feed(3)
        
    def run(self):
        prevTime = time.time()
        while(True):
            nextTime = time.time()
            tickTime = nextTime - prevTime
            if tickTime > 0.0:
                prevTime = nextTime
                self.tick(tickTime)
            if self.stop_next_tick:
                return "finish"
            if self.shutdown_next_tick:
                return "shutdown"

    def finish(self):
        self.printer.printImage(Image.open(self.application_config.goodbye_image), True)
        self.printer.feed(3)

        self.button.finish()
        self.led.finish()

    def tap(self):
        self.todoist.print_tasks()

    def hold(self):
        self.printer.print("hold")
        self.printer.feed(1)
        self.stop_next_tick = True

    def tick(self, tickTime):
        self.button.tick(tickTime)
        self.led.tick(tickTime)
        self.todoist.tick(tickTime)

    def shutdown(self):
        self.shutdown_next_tick = True
