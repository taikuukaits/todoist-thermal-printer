import argparse
import json

from JJ_Print.Python_Thermal_Printer.Adafruit_Thermal import Adafruit_Thermal
from JJ_Print.JJ_Printer_Config import JJ_Printer_Config

class JJ_Printer:

    @staticmethod
    def fromConfig(printer_config):
        printer = Adafruit_Thermal(printer_config.serial, printer_config.baud, timeout=printer_config.timeout)
        return printer