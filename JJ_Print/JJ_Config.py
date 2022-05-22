import argparse
import json

from JJ_Print.JJ_Printer_Config import JJ_Printer_Config
from JJ_Print.JJ_Button_Config import JJ_Button_Config
from JJ_Print.JJ_LED_Config import JJ_LED_Config
from JJ_Print.JJ_Todoist_Config import JJ_Todoist_Config
from JJ_Print.JJ_Application_Config import JJ_Application_Config

class JJ_Config:

    @staticmethod
    def fromArgs():
        parser = argparse.ArgumentParser(description='Process some integers.')
        parser.add_argument('--config', dest='config', required=True, help='File path with config settings in YAML.')
        args = parser.parse_args()
        return JJ_Config.fromFile(args.config)

    @staticmethod
    def fromFile(file):
        print("loading printer settings from: " + file)
        config_dict = json.load(open(file))
        return JJ_Config(config_dict)

    def __init__(self, config_dict):
        self.printer_config = JJ_Printer_Config(config_dict["printer"])
        self.button_config = JJ_Button_Config(config_dict["button"])
        self.led_config = JJ_LED_Config(config_dict["led"])
        self.application_config = JJ_Application_Config(config_dict["application"])
        self.todoist_config = JJ_Todoist_Config(config_dict["todoist"])
        

